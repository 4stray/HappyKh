"""Test users api views"""
from rest_framework.test import APITestCase
from rest_framework import status
from tests.utils import BaseTestCase
from users.models import User

correct_email = 'test@mail.com'
correct_password = 'testPassword'
login_url = '/api/users/login/'

CORRECT_DATA = {'user_email': correct_email,
                'user_password': correct_password}


class LoginViewTestCase(BaseTestCase, APITestCase):
    """Test user api login view /api/users/login/"""
    def setUp(self):
        """Create user objects"""
        self.test_user = User.objects.create_user(email=correct_email,
                                                  password=correct_password)

    def test_invalid_email(self):
        """Test view response for invalid email"""
        data = CORRECT_DATA.copy()
        data['user_email'] = 'fakemail.com'
        response = self.client.post(login_url, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Your email or password is not valid.',
                         response.data['message'])

    def test_incorrect_email(self):
        """Test view response for incorrect email"""
        data = CORRECT_DATA.copy()
        data['user_email'] = 'fake@mail.com'
        response = self.client.post(login_url, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Account with such an email does not exist.',
                         response.data['message'])

    def test_incorrect_password(self):
        """Test view response for incorrect password"""
        data = CORRECT_DATA.copy()
        data['user_password'] = 'fakepassword'
        response = self.client.post(login_url, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Your email or password is not valid.',
                         response.data['message'])

    def test_successful_response(self):
        """Test view response for correct data"""
        self.test_user.is_active = True
        response = self.client.post(login_url, CORRECT_DATA)
        print(response.data['message'])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
