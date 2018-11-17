"""Test users api views"""
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from tests.utils import BaseTestCase
from users.api.views import token_life_duration
from users.models import User

CORRECT_EMAIL = 'test_mail@mail.com'
CORRECT_PASSWORD = 'testPassword'
LOGIN_URL = '/api/users/login'

CORRECT_DATA = {'user_email': CORRECT_EMAIL,
                'user_password': CORRECT_PASSWORD}

ACTIVATED_USER_EMAIL = 'active@gmail.com'
ACTIVATED_USER_PASSWORD = 'activePassword'
ACTIVATED_USER_DATA = {'user_email': ACTIVATED_USER_EMAIL,
                       'user_password': ACTIVATED_USER_PASSWORD}


class LoginViewTestCase(BaseTestCase, APITestCase):
    """Test user api login view /api/users/login/"""

    def setUp(self):
        """Create user objects"""
        self.test_user = User.objects.create_user(email=CORRECT_EMAIL,
                                                  password=CORRECT_PASSWORD)
        self.active_user = User.objects.create_user(
            email=ACTIVATED_USER_EMAIL,
            password=ACTIVATED_USER_PASSWORD,
            is_active=True
        )

    def test_invalid_email(self):
        """Test view response for invalid email"""
        data = CORRECT_DATA.copy()
        data['user_email'] = 'fakemail.com'
        response = self.client.post(LOGIN_URL, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Your email or password is not valid.',
                         response.data['message'])

    def test_incorrect_email(self):
        """Test view response for incorrect email"""
        data = CORRECT_DATA.copy()
        data['user_email'] = 'fake@mail.com'
        response = self.client.post(LOGIN_URL, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Your email or password is not valid.',
                         response.data['message'])

    def test_incorrect_password(self):
        """Test view response for incorrect password"""
        data = CORRECT_DATA.copy()
        data['user_password'] = 'fakepassword'
        response = self.client.post(LOGIN_URL, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Your email or password is not valid.',
                         response.data['message'])

    def test_inactive_logging(self):
        """Test view response for inactive user"""
        data = CORRECT_DATA.copy()
        response = self.client.post(LOGIN_URL, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Your email or password is not valid.',
                         response.data['message'])

    def test_token_login(self):
        """
        If user's token in database expired, he can still login successfully
        and token in database will be changed for a new one.
        """
        token = Token.objects.create(user=self.active_user)
        token.created = timezone.now() - timezone.timedelta(
            days=token_life_duration * 2)
        token.save()
        response = self.client.post(LOGIN_URL, ACTIVATED_USER_DATA)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(0, Token.objects.filter(key=token.key).count())

    def test_successful_response(self):
        """Test view response for correct data"""
        response = self.client.post(LOGIN_URL, ACTIVATED_USER_DATA)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
