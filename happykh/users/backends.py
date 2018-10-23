""" Support class for user authentication """
# pylint: disable=unused-argument, no-self-use
import logging

import hashids
from happykh.settings import HASHID_FIELD_SALT
from rest_framework import serializers
from users.models import User

LOGGER = logging.getLogger('happy_logger')
HASH_IDS = hashids.Hashids(salt=HASHID_FIELD_SALT)


class UserHashedIdField(serializers.Field):
    """
    Field for foreign key to user model for serializer
    """

    def to_representation(self, data):
        return HASH_IDS.encode(data.pk)

    def to_internal_value(self, data):
        user_id = HASH_IDS.decode(data)[0]
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            raise User.DoesNotExist


class UserAuthentication:
    """ Performes user authentication """

    def authenticate(self, request, user_email=None,
                     user_password=None, user_token=None):
        """
        User credentials are being processed on the valid format.
        If User credentials are valid then will be returned User instance.
        If No then None.
        :param request: HttpRequest
        :param user_email: String
        :param user_password: String
        :param user_token: String
        :return: User object or None
        """

        try:
            user = User.objects.get(email=user_email)
            if user.check_password(user_password):
                LOGGER.info('User authenticated')
                return user
        except User.DoesNotExist:  # pylint: disable = no-member
            LOGGER.error('User does not exist while authentication')
        return None

    @staticmethod
    def get_user(user_id):
        """
        Return user object by id
        :param user_id: Number
        :return: User object or None
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:  # pylint: disable = no-member
            LOGGER.error(
                f'Can`t get user profile because of invalid id,'
                f' user_id: {id}'
            )
            return None
