"""Test users api views"""
import django

django.setup()

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from tests.utils import BaseTestCase

from users.models import User
from users.serializers import UserSerializer

USERS_PROFILE_URL = '/api/users/profile/%d'

CORRECT_DATA = {'email': 'test@mail.com',
                'password': 'testpassword1',
                'age': 20,
                'gender': 'M',
                'first_name': 'firstName',
                'last_name': 'lastName',
                'is_active': True
                }


class TestUserProfile(BaseTestCase, APITestCase):
    """Test user profile view"""

    def setUp(self):
        """Create test user for testing"""
        self.test_user = User.objects.create_user(**CORRECT_DATA)
        user_token = Token.objects.create(user=self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)

        self.PASSWORDS = {
            'old_password': CORRECT_DATA['password'],
            'new_password1': 'password2',
            'new_password2': 'password2',
        }

    def test_get(self):
        """test if user exists"""
        response = self.client.get(USERS_PROFILE_URL % self.test_user.pk)
        serializer = UserSerializer(self.test_user)
        expected = serializer.data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(expected, response.data)

    def test_get_unauthorized_user(self):
        """test if user is unauthorized"""
        new_test_user = User.objects.create_user(email="second@test.com",
                                                 password="password2")
        new_client = APIClient()
        response = new_client.get(USERS_PROFILE_URL % new_test_user.pk)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_patch_update_data(self):
        """test update user's age"""
        edited_user = User.objects.get(pk=self.test_user.pk)
        edited_user.age = 41
        response = self.client.patch(USERS_PROFILE_URL % edited_user.pk,
                                     {'age': edited_user.age})

        serializer_edited_user = UserSerializer(edited_user)
        expected = serializer_edited_user.data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected, response.data)

        serializer = UserSerializer(self.test_user)
        self.assertNotEqual(serializer.data, response.data)
        self.assertIn(edited_user, User.objects.all())

    def test_patch_invalid_update(self):
        """test update user's age with invalid value"""
        edited_user = User.objects.get(pk=self.test_user.pk)
        edited_user.age = -41
        response = self.client.patch(
            USERS_PROFILE_URL % edited_user.pk,
            {'age': edited_user.age})
        serializer_edited_user = UserSerializer(edited_user)
        expected = serializer_edited_user.data["age"]
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected, int(response.data["age"]))

        response = self.client.get(
            USERS_PROFILE_URL % self.test_user.pk)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertNotEqual(expected, response.data["age"])
        self.assertIsNot(edited_user, User.objects.get(pk=self.test_user.pk))

    def test_patch_update_password(self):
        """test update user's password"""
        response = self.client.patch(
            USERS_PROFILE_URL % self.test_user.pk,
            self.PASSWORDS)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_patch_invalid_update_password(self):
        """test update user's password with wrong old password"""
        INVALID_PASSWORD = self.PASSWORDS.copy()
        INVALID_PASSWORD['old_password'] = '123userPassword'
        response = self.client.patch(
            USERS_PROFILE_URL % self.test_user.pk,
            INVALID_PASSWORD)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertFalse(
            self.test_user.check_password(INVALID_PASSWORD['new_password1']))

    def test_patch_different_new_passwords(self):
        """test update user's password with different new passwords"""
        INVALID_PASSWORD = self.PASSWORDS.copy()
        INVALID_PASSWORD['new_password1'] = '123userPassword'
        response = self.client.patch(
            USERS_PROFILE_URL % self.test_user.pk,
            INVALID_PASSWORD)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertFalse(
            self.test_user.check_password(INVALID_PASSWORD['new_password1']))

    def test_patch_invalid_new_password(self):
        """test update user's password with invalid new password"""
        INVALID_PASSWORD = self.PASSWORDS.copy()
        INVALID_PASSWORD['new_password1'] = '123'
        response = self.client.patch(
            USERS_PROFILE_URL % self.test_user.pk,
            INVALID_PASSWORD)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertFalse(
            self.test_user.check_password(INVALID_PASSWORD['new_password1']))
