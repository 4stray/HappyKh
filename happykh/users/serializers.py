from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers, exceptions


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    user_email = serializers.EmailField()
    user_password = serializers.CharField()

    def validate(self, data):
        user_email = data.get('user_email', '')
        user_password = data.get('user_password', '')

        try:
            validate_email(user_email)
        except ValidationError:
            raise exceptions.ValidationError('Invalid email format')

        if user_email and user_password:
            user = authenticate(user_email=user_email,
                                user_password=user_password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    msg = "Please, check you mailbox in order " \
                          "to activate your account"
                    raise exceptions.ValidationError(msg)
            else:
                msg = 'Account with such an email does not exist'
                raise exceptions.ValidationError(msg)
        else:
            msg = 'Must provide user email and password'
            raise exceptions.ValidationError(msg)
        return data
