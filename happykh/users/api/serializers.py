"""Custom serializers for users app"""
# pylint: disable = logging-fstring-interpolation
import base64
import logging
import os
import uuid
import six

from django.conf import settings
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.validators import validate_email
from rest_framework import exceptions
from rest_framework import serializers

from ..models import User

LOGGER = logging.getLogger('happy_logger')


class Base64ImageField(serializers.ImageField):
    """
    Class which converts a base64 string to a file when input and converts image
    by path to it into base64 string
    """

    def to_internal_value(self, data):

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

                # Try to decode the file. Return validation error if it fails.
                try:
                    decoded_file = base64.b64decode(data)
                except TypeError:
                    self.fail('invalid_image')

                # Get the file name extension:
                file_extension = header.split('/')[-1]

                # Generate file name:
                file_name = uuid.uuid4()

                complete_file_name = "%s.%s" % (file_name, file_extension,)

                data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def to_representation(self, value):
        if value:
            image_file = value.path
            if not os.path.isfile(image_file):
                return None

            encoded_string = ''
            with open(image_file, 'rb') as img_f:
                encoded_string = base64.b64encode(img_f.read())
                encoded_string = encoded_string.decode()
            extension = value.path.split('.')[-1]
            return f'data:image/{extension};base64,{encoded_string}'
        return ''


class UserSerializer(serializers.ModelSerializer):
    """Serializer for custom user model"""

    profile_image = Base64ImageField(
        max_length=None, use_url=True,
    )

    class Meta:
        # pylint: disable=too-few-public-methods, missing-docstring
        model = User
        fields = '__all__'

    def update(self, instance, validated_data):

        if instance.profile_image:
            # delete old image
            os.remove(
                os.path.join(settings.MEDIA_ROOT, str(instance.profile_image)))

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


# pylint: disable = abstract-method
class LoginSerializer(serializers.Serializer):
    """
    Serializer for user credentials
    """
    user_email = serializers.CharField()
    user_password = serializers.CharField()

    def validate(self, attrs):
        user_email = attrs.get('user_email', '')
        user_password = attrs.get('user_password', '')

        try:
            validate_email(user_email)
        except ValidationError:
            email_validation_error = exceptions.ValidationError

            email_validation_error.default_detail = \
                'Invalid user email format.'
            LOGGER.error(
                f'Serializer:Validation error '
                f'{email_validation_error.default_detail}'
                f'invalid email format, Email: {user_email}'
            )
            raise email_validation_error

        if user_email and user_password:
            user = authenticate(user_email=user_email,
                                user_password=user_password)
            if user:
                if user.is_active:
                    attrs['user'] = user
                else:
                    account_activation_error = exceptions.ValidationError
                    account_activation_error.default_detail = \
                        'Please, check you mailbox in order ' \
                        'to activate your account'
                    LOGGER.warning(
                        'Serializer: Validation warning,'
                        ' need to activate account'
                    )
                    raise account_activation_error
            else:
                account_exists_error = exceptions.ValidationError
                account_exists_error.default_detail = \
                    'Account with such credentials does not exist'

                LOGGER.warning(
                    f'Serializer: Validation warning, '
                    f'{account_exists_error.default_detail},'
                    f' user_email: {user_email}'
                )
                raise account_exists_error
        else:
            authorization_error = exceptions.ValidationError
            authorization_error.default_detail = \
                'Must provide user email and password'
            LOGGER.warning(
                f'Serializer: Validation warning, '
                f'{authorization_error.default_detail}'
            )
            raise authorization_error
        return attrs


class PasswordSerializer(serializers.ModelSerializer):
    """
    Serializer for password change.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        # pylint: disable=too-few-public-methods, missing-docstring
        model = User
        fields = ('old_password', 'new_password')

    def update(self, instance, validated_data):
        password = validated_data.pop("new_password")
        instance.__dict__.update(validated_data)

        if password:
            instance.set_password(password)
        instance.save()

        return instance
