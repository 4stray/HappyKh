"""Custom serializers for users app"""
import logging

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import exceptions
from rest_framework import serializers

from ..models import User

LOGGER = logging.getLogger('happy_logger')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user credentials
    """
    user_email = serializers.CharField()
    user_password = serializers.CharField()

    def validate(self, data):
        user_email = data.get('user_email', '')
        user_password = data.get('user_password', '')

        try:
            validate_email(user_email)
        except ValidationError:
            email_format_error = exceptions.ValidationError
            email_format_error.default_detail = 'Invalid user email format.'
            LOGGER.error(
                f'Serializer:'
                f' Validation error {email_format_error.default_detail}'
                f'invalid email format, Email: {user_email}')
            raise email_format_error

        if user_email and user_password:
            user = authenticate(user_email=user_email,
                                user_password=user_password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    activation_error = exceptions.PermissionDenied
                    activation_error.default_detail = \
                        'Please, check you mailbox in order ' \
                        'to activate your account'
                    LOGGER.warning(
                        'Serializer: Validation warning,'
                        ' need to activate account')
                    raise activation_error
            else:
                not_found_error = exceptions.NotFound
                not_found_error.default_detail = \
                    'Account with such credentials does not exists'
                LOGGER.warning(
                    f'Serializer: Validation warning,'
                    f' {not_found_error.default_detail},'
                    f' user_email: {user_email}')
                raise not_found_error
        else:
            credentials_error = exceptions.AuthenticationFailed
            credentials_error.default_detail = \
                'Must provide user email and password'
            LOGGER.warning(f'Serializer:  Validation warning,'
                           f' {credentials_error.default_detail}')
            raise credentials_error
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
