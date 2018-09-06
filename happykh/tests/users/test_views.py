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
        User.objects.create_user(email='test@mail.com', password='testpassword')

    def tets_invalid_email(self):
        """Test view response for invalid email"""
        data = CORRECT_DATA.copy()
        data['user_email'] = 'fakemail.com'
        response = self.client.post('/api/users/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], False)
        self.assertEqual(response.data['message'], 'Invalid email data.')

    def test_incorrect_email(self):
        """Test view response for incorrect email"""
        data = CORRECT_DATA.copy()
        data['user_email'] = 'fake@mail.com'
        response = self.client.post('/api/users/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], False)
        self.assertEqual(response.data['message'], 'No user with such email.')

    def test_incorrect_password(self):
        """Test view response for incorrect password"""
        data = CORRECT_DATA.copy()
        data['user_password'] = 'fakepassword'
        response = self.client.post('/api/users/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], False)
        self.assertEqual(response.data['message'], 'Incorrect password.')

    def test_successful_response(self):
        """Test view response for correct data"""
        response = self.client.post('/api/users/login/', CORRECT_DATA)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], True)
