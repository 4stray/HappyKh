from rest_framework.test import APITestCase
from rest_framework import status
from tests.utils import BaseTestCase
from users.models import User

correct_data = {'user_email': 'test@mail.com',
                'user_password': 'testpassword'}


class LoginViewTestCase(BaseTestCase, APITestCase):
    def setUp(self):
        """Create user objects"""
        User.objects.create_user(email='test@mail.com', password='testpassword')

    def test_incorrect_email(self):
        data = correct_data.copy()
        data['user_email'] = 'fake@mail.com'
        response = self.client.post('/api/users/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], False)
        self.assertEqual(response.data['message'], "No user with such email.")

    def test_incorrect_password(self):
        data = correct_data.copy()
        data['user_password'] = 'fakepassword'
        response = self.client.post('/api/users/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], False)
        self.assertEqual(response.data['message'], "Incorrect password.")

    def test_successful_response(self):
        response = self.client.post('/api/users/login/', correct_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], True)
