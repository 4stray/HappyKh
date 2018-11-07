"""Custom serializers for users app"""
# pylint: disable = logging-fstring-interpolation
import logging

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from happykh.settings import HASH_IDS
from rest_framework import exceptions
from rest_framework import serializers
from utils import UploadedImageField
from utils import delete_std_images_from_media
from utils import HashIdField

from ..models import User, CommentAbstract

LOGGER = logging.getLogger('happy_logger')


class UserSerializer(serializers.ModelSerializer):
    """Serializer for custom user model"""
    id = HashIdField()
    profile_image = UploadedImageField(max_length=None, )

    class Meta:
        # pylint: disable=too-few-public-methods, missing-docstring
        model = User
        exclude = ('email', 'password')

    def update(self, instance, validated_data):
        new_image = validated_data.get('profile_image')
        old_image = instance.profile_image
        if new_image is not None and old_image:
            # delete old images
            delete_std_images_from_media(
                old_image,
                User.VARIATIONS_PROFILE_IMAGE
            )

        for attr, value in validated_data.items():
            if attr != 'profile_image' or value is not None:
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


class EmailSerializer(serializers.ModelSerializer):
    """
    Serializer for email change
    """

    class Meta:
        # pylint: disable=too-few-public-methods, missing-docstring
        model = User
        fields = ('email',)

    def validate(self, attrs):
        new_email = attrs.get('email')

        try:
            validate_email(new_email)
        except ValidationError:
            email_validation_error = exceptions.ValidationError

            email_validation_error.default_detail = \
                'Invalid user email format.'
            LOGGER.error(
                f'Serializer:Validation error '
                f'{email_validation_error.default_detail}'
                f'invalid email format, Email: {new_email}'
            )
            raise email_validation_error
        return attrs

    def update(self, instance, validated_data):
        new_email = validated_data.get('email')

        if new_email:
            instance.is_active = False
            instance.email = new_email
            instance.save()

        return instance


class CommentAbstractSerializer(serializers.ModelSerializer):
    """
    Full ModelSerializer for model CommentAbstract.
    Represents with creator's data.
    """

    class Meta:
        model = CommentAbstract
        fields = '__all__'

    def to_representation(self, instance):
        """Representation data of comment and extended data of user"""
        ret = super().to_representation(instance)
        user_context = {
            'variation': User.thumbnail,
            'domain': self.context['domain']
        }
        comment_creator = User.objects.get(pk=instance.creator_id)
        creator_serializer = UserSerializer(comment_creator,
                                            context=user_context)
        ret['creator_image'] = creator_serializer.data['profile_image']
        ret['creator_fullname'] = comment_creator.get_full_name()
        ret['creator'] = HASH_IDS.encode(ret['creator'])
        return ret
