"""Test activation email view"""
import pytest
from rest_framework import status
from rest_framework.test import APITestCase
from tests.utils import BaseTestCase
from users.api.tokens import account_activation_token
from users.cryptography import encode
from users.models import User

CORRECT_EMAIL = 'test@mail.com'
SEND_EMAIL_URL = '/api/users/activate/send-email/'
ACTIVATION_URL = '/api/users/activate/%s/%s/'

CORRECT_DATA = {'user_email': CORRECT_EMAIL}


@pytest.mark.django_db
class ActivationEmailViewTestCase(BaseTestCase, APITestCase):
    """ Test email activation """

    def setUp(self):
        self.test_user = User.objects.create_user(email=CORRECT_EMAIL,
                                                  password='test123')
        self.token = account_activation_token.make_token(self.test_user)
        self.encoded_email = encode(CORRECT_EMAIL)

    def test_invalid_email(self):
        """Test view response for invalid email"""
        data = CORRECT_DATA.copy()
        data['user_email'] = 'fake_mail.com'
        response = self.client.post(SEND_EMAIL_URL, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Invalid email', response.data['message'])

    def test_is_user_in_db(self):
        """Test if user with such email exists in db"""
        data = CORRECT_DATA.copy()
        data['user_email'] = 'fake@mail.com'
        response = self.client.post(SEND_EMAIL_URL, data)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_is_active(self):
        """Test is user already activated"""
        self.test_user.is_active = True
        self.test_user.save()
        response = self.client.post(SEND_EMAIL_URL, CORRECT_DATA)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('User already activated',
                         response.data['message'])

    def test_successful_response(self):
        """Test successful response case"""
        self.test_user.is_active = False
        self.test_user.save()
        response = self.client.post(SEND_EMAIL_URL, CORRECT_DATA)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('Confirmation email has been sent',
                         response.data['message'])

    def test_invalid_token(self):
        """Test view response for invalid token"""
        token = '123'
        response = self.client.get(
            ACTIVATION_URL % (self.encoded_email, token)
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Invalid token', response.data['message'])

    def test_activation_request(self):
        """Test user account activation"""
        response = self.client.get(
            ACTIVATION_URL % (self.encoded_email, self.token)
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual("User's account has been activated",
                         response.data['message'])

    def test_activation_request_for_activated_user(self):
        """Test user account activation for already activated user"""
        self.test_user.is_active = True
        self.test_user.save()
        response = self.client.get(
            ACTIVATION_URL % (self.encoded_email, self.token)
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual("User is already exists and activated",
                         response.data['message'])
