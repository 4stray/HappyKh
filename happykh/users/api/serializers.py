"""Custom serializers for users app"""
import logging

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import exceptions
from rest_framework import serializers

from happykh.users.models import User

LOGGER = logging.getLogger('happy_logger')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user credentials
    """
    user_email = serializers.EmailField()
    user_password = serializers.CharField()

    def validate(self, data):
        user_email = data.get('user_email', '')
        user_password = data.get('user_password', '')

        try:
            validate_email(user_email)
        except ValidationError as error:
            LOGGER.error(
                "Serializer: Validation error %s"
                "invalid email format, Email: %s" % (error, user_email))
            raise exceptions.ValidationError("Invalid email format")

        if user_email and user_password:
            user = authenticate(user_email=user_email,
                                user_password=user_password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    msg = "Please, check you mailbox in order " \
                          "to activate your account"
                    LOGGER.warning(
                        "Serializer: Validation warning,"
                        " need to activate account")
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Account with such an email does not exists"
                LOGGER.warning(
                    "Serializer: Validation warning, %s, user_email: %s" % (
                        msg, user_email))
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide user email and password"
            LOGGER.warning("Serializer:  Validation warning, %s", msg)
            raise exceptions.ValidationError(msg)
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
