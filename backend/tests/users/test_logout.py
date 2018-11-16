"""Test logout view"""
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from users.models import User

from .test_profile import CORRECT_DATA
from ..utils import BaseTestCase

USERS_LOGOUT_URL = '/api/users/logout'


class TestLogout(BaseTestCase, APITestCase):
    """Test logout view"""

    def setUp(self):
        self.test_user = User.objects.create_user(**CORRECT_DATA)
        test_user_token = Token.objects.create(user=self.test_user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + test_user_token.key
        )

    def test_logout(self):
        """Test logout from user account"""
        response = self.client.post(USERS_LOGOUT_URL)
        expected = {'message': 'User has been logged out'}
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected, response.data)
