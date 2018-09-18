"""Test users api views"""
from django.core.mail import send_mail
from rest_framework.test import APITestCase
from rest_framework import status
from tests.utils import BaseTestCase
from users.models import User
from happykh.settings import EMAIL_HOST_USER


TEST_USER_DATA = {'user_email': 'test@mail.com',
                'user_password': 'testpassword'}


class RegistrationViewTestCase(BaseTestCase, APITestCase):
    """Test user api login view /api/users/registration/"""
    def setUp(self):
        pass

    def register_deactivated_user(self, data):
        response = self.client.post('/api/users/registration/', data)
        return response

    def test_create_deactivated_user(self):
        data = TEST_USER_DATA.copy()
        response = self.register_deactivated_user(data)
        print(response.data['message'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(User.objects.get(email=data['user_email']).is_active)

    def test_sending_email(self):
        user = User.objects.create_user(email='mykyta.sobol@nure.ua',
                                        password='password',
                                        is_active=False)

        try:
            self.assertTrue(send_mail('tets', 'test body', EMAIL_HOST_USER, (user.email,)))
        except:
            raise AssertionError('Mail has not been sent')
