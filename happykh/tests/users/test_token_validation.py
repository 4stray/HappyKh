"""Test users api views"""
import datetime
# pylint: disable = no-member
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from utils import delete_std_images_from_media
from ..utils import BaseTestCase
from .test_profile import CORRECT_DATA

USERS_TEST_TOKEN_VALIDATION_URL = '/api/users/token-validation'


class TestTokenValidation(BaseTestCase, APITestCase):
    """Test token relevance"""

    def setUp(self):
        self.test_user = User.objects.create_user(**CORRECT_DATA)
        self.test_user_token = Token.objects.create(user=self.test_user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.test_user_token.key
        )

    def tearDown(self):
        """ teardown any state that were previously setup with a call of
        setup.
        """
        instance = self.test_user
        if instance.profile_image:
            # delete images that were created in test
            delete_std_images_from_media(
                instance.profile_image,
                User.VARIATIONS_PROFILE_IMAGE
            )

    def test_valid_token_after_expiration_date(self):
        self.test_user_token.created = (self.test_user_token.created -
                                        datetime.timedelta(days=5))
        self.test_user_token.save()
        response = self.client.get(USERS_TEST_TOKEN_VALIDATION_URL)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_valid_token_before_expiration_date(self):
        response = self.client.get(USERS_TEST_TOKEN_VALIDATION_URL)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalid token')
        response = self.client.get(USERS_TEST_TOKEN_VALIDATION_URL)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
