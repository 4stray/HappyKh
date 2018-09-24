"""Custom serializers for users app"""
import logging

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import exceptions
from rest_framework import serializers
from rest_framework import status

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
            error_message = 'Invalid user email format.'
            LOGGER.error(
                f'Serializer:Validation error {error_message}'
                f'invalid email format, Email: {user_email}')
            raise exceptions.ValidationError(error_message,
                                             code=status.HTTP_400_BAD_REQUEST)

        if user_email and user_password:
            user = authenticate(user_email=user_email,
                                user_password=user_password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    error_message = 'Please, check you mailbox in order ' \
                                    'to activate your account'
                    LOGGER.warning(
                        'Serializer: Validation warning,'
                        ' need to activate account')
                    raise exceptions.ValidationError(
                        error_message,
                        code=status.HTTP_400_BAD_REQUEST)
            else:
                error_message = 'Account with such credentials does not exist'
                LOGGER.warning(
                    f'Serializer: Validation warning, {error_message},'
                    f' user_email: {user_email}')
            raise exceptions.ValidationError(error_message,
                                             code=status.HTTP_400_BAD_REQUEST)
        else:
            error_message = 'Must provide user email and password'
            LOGGER.warning(f'Serializer: Validation warning, {error_message}')
            raise exceptions.ValidationError(error_message,
                                             code=status.HTTP_400_BAD_REQUEST)


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
