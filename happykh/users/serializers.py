from django.contrib.auth import authenticate
from django.core import exceptions
from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.exceptions import (AuthenticationFailed, ValidationError,
    NotAuthenticated, NotFound)
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    user_email = serializers.CharField()
    user_password = serializers.CharField()

    def validate(self, data):
        user_email = data.get('user_email', '')
        user_password = data.get('user_password', '')

        try:
            validate_email(user_email)
        except exceptions.ValidationError:
            raise AuthenticationFailed()

        if user_email and user_password:
            user = authenticate(user_email=user_email,
                                user_password=user_password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    deactivated_user_error = ValidationError()

                    deactivated_user_error.default_detail = (
                        "Please, check you mailbox in order "
                        "to activate your account",
                    )

                    raise deactivated_user_error
            else:
                raise NotFound()
        else:
            raise NotAuthenticated()
        return data


class PasswordSerializer(serializers.ModelSerializer):
    """
    Serializer for password change.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password')

    def update(self, instance, validated_data):
        password = validated_data.pop("new_password")
        instance.__dict__.update(validated_data)

        if password:
            instance.set_password(password)
        instance.save()

        return instance
