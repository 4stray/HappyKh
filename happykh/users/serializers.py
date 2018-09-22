import logging
from django.contrib.auth import authenticate
from django.core import exceptions
from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.exceptions import (AuthenticationFailed, ValidationError,
    NotFound, PermissionDenied)
from users.models import User

logger = logging.getLogger('happy_logger')


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
        except exceptions.ValidationError as error:
            logger.error(f'Validation error {error}, invalid email format,'
                         f' Email: {user_email}')

            email_format_error = ValidationError
            email_format_error.default_detail = 'Invalid user email format.'

            raise email_format_error

        if not user_email is None and not user_password is None:
            user = authenticate(user_email=user_email,
                                user_password=user_password)
            if not user is None:
                if user.is_active:
                    data['user'] = user
                else:
                    logger.warning('Validation warning, need to activate '
                                   'account')

                    activation_required_error = PermissionDenied
                    activation_required_error.default_detail = \
                        'Please, click the link in the mail we sent you' \
                        'in order to activate your account'

                    raise activation_required_error
            else:
                account_exists_error = NotFound
                account_exists_error.default_detail = \
                    'User with such credentials was not found.'

                logger.warning(f'Validation warning, '
                               f'{account_exists_error.default_detail},'
                               f' user_email: {user_email}')

                raise account_exists_error
        else:
            authorization_error = AuthenticationFailed
            authorization_error.default_detail = 'Must provide user ' \
                                                 'email and password'

            logger.warning(f'Validation warning, '
                           f'{authorization_error.default_detail}')
            raise authorization_error

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
