"""Test users api views"""
from rest_framework.test import APITestCase
from rest_framework import status
from tests.utils import BaseTestCase
from users.models import User

CORRECT_DATA = {'user_email': 'test@mail.com',
                'user_password': 'testpassword'}


class LoginViewTestCase(BaseTestCase, APITestCase):
    """Test user api login view /api/users/login/"""
    def setUp(self):
        """Create user objects"""
        User.objects.create_user(email='test@mail.com',
                                 password='testpassword')

    def test_invalid_email(self):
        """Test view response for invalid email"""
        data = CORRECT_DATA.copy()
        data['user_email'] = 'invalidmail.com'
        response = self.client.post('/api/users/login/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Incorrect authentication credentials.')

    def test_nonexisting_email(self):
        """Test view response for nonexisting email"""
        data = CORRECT_DATA.copy()
        data['user_email'] = 'fake@mail.com'
        response = self.client.post('/api/users/login/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Not found.')

    def test_wrong_password(self):
        """Test view response for incorrect password"""
        data = CORRECT_DATA.copy()
        data['user_password'] = 'wrongpassword'
        response = self.client.post('/api/users/login/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Not found.')

    def test_successful_response(self):
        """Test view response for correct data"""
        response = self.client.post('/api/users/login/', CORRECT_DATA)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
