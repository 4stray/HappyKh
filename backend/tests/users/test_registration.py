"""Test users api views"""
from rest_framework import status
from rest_framework.test import APITestCase

from users.api.tokens import account_activation_token
from users.cryptography import encode
from users.models import User
from tests.utils import BaseTestCase

TEST_USER_DATA = {
    'user_email': 'test@mail.com',
    'user_password': 'testpassword',
    'first_name': 'User'
}

REGISTRATION_URL = '/api/users/registration'


class RegistrationViewTestCase(BaseTestCase, APITestCase):
    """Test user api registration view /api/users/registration/"""

    def test_create_deactivated_user(self):
        """test new user creation"""
        data = TEST_USER_DATA.copy()
        response = self.client.post(REGISTRATION_URL, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_email(self):
        """test user registration with invalid email"""
        data = TEST_USER_DATA.copy()
        data['user_email'] = 'invalidemail.com'
        response = self.client.post(REGISTRATION_URL, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_activate_valid_account(self):
        """test activation valid user account"""
        data = TEST_USER_DATA.copy()
        user = User.objects.create_user(email=data['user_email'],
                                        password=data['user_password'],
                                        is_active=False)
        email_token = account_activation_token.make_token(user)

        crypted_email = encode(user.email)
        response = self.client.get(
            f'/api/users/activate/{crypted_email}/{email_token}/'
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_empty_credentials(self):
        """Test user registration without some fields"""
        empty_data = {
            'user_email': '',
            'user_password': '',
            'first_name': ''
        }
        expected = {'message': 'Some credentials were not provided'}
        response = self.client.post(REGISTRATION_URL, empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(expected, response.data)

        empty_data['first_name'] = 'user'
        response = self.client.post(REGISTRATION_URL, empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(expected, response.data)

        empty_data['user_email'] = 'user@email.com'
        response = self.client.post(REGISTRATION_URL, empty_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(expected, response.data)
