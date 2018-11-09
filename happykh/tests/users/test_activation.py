"""Test activation email view"""
import pytest
from rest_framework.test import APITestCase
from rest_framework import status
from tests.utils import BaseTestCase
from users.models import User

CORRECT_EMAIL = 'test@mail.com'
LOGIN_URL = '/api/users/activate/send-email/'

CORRECT_DATA = {'user_email': CORRECT_EMAIL}


@pytest.mark.django_db
class ActivationEmailViewTestCase(BaseTestCase, APITestCase):
    """ Test email activation """
    def setUp(self):
        self.test_user = User.objects.create_user(email=CORRECT_EMAIL,
                                                  password='test123')

    def test_invalid_email(self):
        """Test view response for invalid email"""
        data = CORRECT_DATA.copy()
        data['user_email'] = 'fakemail.com'
        response = self.client.post(LOGIN_URL, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Invalid email', response.data['message'])

    def test_is_user_in_db(self):
        """Test is user with such email in db"""
        data = CORRECT_DATA.copy()
        data['user_email'] = 'fake@mail.com'
        response = self.client.post(LOGIN_URL, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('There is no user with such email',
                         response.data['message'])

    def test_is_active(self):
        """Test is user already activated"""
        self.test_user.is_active = True
        self.test_user.save()
        response = self.client.post(LOGIN_URL, CORRECT_DATA)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('User already activated',
                         response.data['message'])

    def test_successful_response(self):
        """Test successful response case"""
        self.test_user.is_active = False
        self.test_user.save()
        response = self.client.post(LOGIN_URL, CORRECT_DATA)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('Confirmation email has been sent',
                         response.data['message'])
