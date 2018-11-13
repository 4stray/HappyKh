"""Custom serializers for users app"""
import logging

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from happykh.settings import HASH_IDS
from rest_framework import exceptions, serializers

from utils import HashIdField
from utils import UploadedImageField
from utils import delete_std_images_from_media
from ..models import User, CommentAbstract

LOGGER = logging.getLogger('happy_logger')


class UserSerializer(serializers.ModelSerializer):
    """Serializer for custom user model"""
    id = HashIdField()
    profile_image = UploadedImageField(max_length=None, )
    age = serializers.IntegerField(max_value=140,
                                   min_value=0,
                                   allow_null=True,
                                   default=None)

    class Meta:
        model = User
        exclude = ('email', 'password')

    def update(self, instance, validated_data):
        new_image = validated_data.get('profile_image')
        old_image = instance.profile_image
        if new_image and old_image:
            # delete old images
            delete_std_images_from_media(
                old_image,
                User.VARIATIONS_PROFILE_IMAGE
            )

        for attr, value in validated_data.items():
            if attr != 'profile_image' or value:
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

        if not user_email and user_password:
            authorization_error = exceptions.ValidationError
            authorization_error.default_detail = \
                'Must provide user email and password'
            LOGGER.warning(
                f'Serializer: Validation warning, '
                f'{authorization_error.default_detail}'
            )
            raise authorization_error

        user = authenticate(user_email=user_email,
                            user_password=user_password)
        if not user:
            account_exists_error = exceptions.ValidationError
            account_exists_error.default_detail = \
                'Account with such credentials does not exist'
            LOGGER.warning(
                f'Serializer: Validation warning, '
                f'{account_exists_error.default_detail},'
                f' user_email: {user_email}'
            )
            raise account_exists_error

        if not user.is_active:
            account_activation_error = exceptions.ValidationError
            account_activation_error.default_detail = \
                'Please, check you mailbox in order ' \
                'to activate your account'
            LOGGER.warning(
                'Serializer: Validation warning,'
                ' need to activate account'
            )
            raise account_activation_error

        attrs['user'] = user
        return attrs


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
        instance.set_password(validated_data.get('new_password'))
        instance.save()
        return instance


class EmailSerializer(serializers.ModelSerializer):
    """
    Serializer for email change
    """

    class Meta:
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
