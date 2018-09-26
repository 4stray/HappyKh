"""Test users api views"""
from rest_framework.test import APITestCase
from rest_framework import status
from tests.utils import BaseTestCase
from users.models import User
from users.api.tokens import account_activation_token


TEST_USER_DATA = {
    'user_email': 'test@mail.com',
    'user_password': 'testpassword'
}


class RegistrationViewTestCase(BaseTestCase, APITestCase):
    """Test user api registration view /api/users/registration/"""
    def setUp(self):
        pass

    def test_create_deactivated_user(self):
        data = TEST_USER_DATA.copy()
        response = self.client.post('/api/users/registration/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_email(self):
        data = TEST_USER_DATA.copy()
        data['user_email'] = 'invalidemail.com'
        response = self.client.post('/api/users/registration/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_activate_valid_account(self):
        data = TEST_USER_DATA.copy()
        user = User.objects.create_user(email=data['user_email'],
                                        password=data['user_password'],
                                        is_active=False)
        email_token = account_activation_token.make_token(user)

        response = self.client.post(
            f'/api/users/activate/{user.id}/{email_token}/'
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
