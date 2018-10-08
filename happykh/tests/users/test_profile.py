"""Test users api views"""
# pylint: disable = no-member
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from users.api.serializers import UserSerializer
from users.models import User

from ..utils import BaseTestCase

USERS_PROFILE_URL = '/api/users/%d'

CORRECT_DATA = {
    'email': 'test@mail.com',
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

        other_test_user = CORRECT_DATA.copy()
        other_test_user['email'] = 'test2@gmail.com'
        self.other_test_user = User.objects.create_user(**other_test_user)

        self.PASSWORD = {
            'old_password': CORRECT_DATA['password'],
            'new_password': 'password2',
        }

    def test_get_user_with_access_for_editing_own_profile(self):
        response = self.client.get(USERS_PROFILE_URL % self.test_user.pk)
        serializer = UserSerializer(self.test_user)
        expected = serializer.data
        expected['enable_editing_profile'] = True

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(expected, response.data)

    def test_get_user_without_access_for_editing_own_profile(self):
        response = self.client.get(USERS_PROFILE_URL % self.other_test_user.id)
        serializer = UserSerializer(self.other_test_user)
        expected = serializer.data
        expected['enable_editing_profile'] = False

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(expected, response.data)

    def test_get_unauthorized_user(self):
        """test if user is unauthorized"""
        new_test_user = User.objects.create_user(email="second@test.com",
                                                 password="password2")
        new_client = APIClient()
        response = new_client.get(USERS_PROFILE_URL % new_test_user.pk)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_patch_update_user_data_with_editing_profile_access(self):
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

    def test_patch_update_user_data_without_editing_profile_access(self):
        response = self.client.patch(
            USERS_PROFILE_URL % self.other_test_user.id,
            {'age': self.other_test_user.age},
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_patch_invalid_update(self):
        """test update user's age with invalid value"""
        edited_user = User.objects.get(pk=self.test_user.pk)
        edited_user.age = -41
        response = self.client.patch(USERS_PROFILE_URL % edited_user.pk,
                                     {'age': edited_user.age})
        serializer_edited_user = UserSerializer(edited_user)
        expected = serializer_edited_user.data["age"]
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertRaises(ValueError)

        response = self.client.get(USERS_PROFILE_URL % self.test_user.pk)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertNotEqual(expected, response.data["age"])
        self.assertIsNot(edited_user, User.objects.get(pk=self.test_user.pk))

    def test_patch_update_password(self):
        """test update user's password"""
        response = self.client.patch(USERS_PROFILE_URL % self.test_user.pk,
                                     self.PASSWORD)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_patch_invalid_update_password(self):
        """test update user's password with wrong old password"""
        invalid_password = self.PASSWORD.copy()
        invalid_password['old_password'] = '123userPassword'
        response = self.client.patch(USERS_PROFILE_URL % self.test_user.pk,
                                     invalid_password)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertFalse(
            self.test_user.check_password(invalid_password['new_password'])
        )

    def test_patch_invalid_new_password(self):
        """test update user's password with invalid new password"""
        invalid_password = self.PASSWORD.copy()
        invalid_password['new_password'] = ''
        response = self.client.patch(USERS_PROFILE_URL % self.test_user.pk,
                                     invalid_password)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertFalse(
            self.test_user.check_password(invalid_password['new_password'])
        )
