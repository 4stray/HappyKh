"""Test users api views"""
import django
django.setup()
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from tests.utils import BaseTestCase
from users.models import User
from users.serializers import UserSerializer

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
        response = self.client.get(f'/api/users/profile/{self.test_user.pk}')
        serializer = UserSerializer(self.test_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], serializer.data["id"])
        self.assertEqual(response.data['email'], serializer.data['email'])
        self.assertEqual(response.data['first_name'],
                         serializer.data['first_name'])
        self.assertEqual(response.data['last_name'],
                         serializer.data['last_name'])
        self.assertEqual(response.data['profile_image'],
                         serializer.data['profile_image'])
        self.assertEqual(response.data['is_active'],
                         serializer.data['is_active'])
        self.assertEqual(response.data['age'], serializer.data['age'])
        self.assertEqual(response.data['gender'], serializer.data['gender'])

    def test_get_unauthorized_user(self):
        """test if user is unauthorized"""
        test_user = User.objects.create_user(email="second@test.com",
                                             password="password2")
        new_client = APIClient()
        response = new_client.get(f'/api/users/profile/{test_user.pk}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_update_data(self):
        """test update user's age"""
        edited_user = User.objects.get(pk=self.test_user.pk)
        edited_user.age = 41
        response = self.client.patch(f'/api/users/profile/{edited_user.pk}',
                                     {'age': edited_user.age})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_edited_user = UserSerializer(edited_user)
        self.assertEqual(response.data, serializer_edited_user.data)

        serializer = UserSerializer(self.test_user)
        self.assertNotEqual(response.data, serializer.data)

        self.assertIn(edited_user, User.objects.all())

    def test_patch_invalid_update(self):
        """test update user's age with invalid value"""
        edited_user = User.objects.get(pk=self.test_user.pk)
        edited_user.age = -41
        response = self.client.patch(f'/api/users/profile/{edited_user.pk}',
                                     {'age': edited_user.age})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_edited_user = UserSerializer(edited_user)
        self.assertEqual(int(response.data["age"]),
                         serializer_edited_user.data["age"])

        response = self.client.get(f'/api/users/profile/{self.test_user.pk}')
        self.assertNotEqual(response.data["age"],
                            serializer_edited_user.data["age"])

        self.assertIsNot(edited_user, User.objects.get(pk=self.test_user.pk))

    def test_patch_update_password(self):
        """test update user's password"""
        response = self.client.patch(f'/api/users/profile/{self.test_user.pk}',
                                     **self.PASSWORDS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_invalid_update_password(self):
        """test update user's password with wrong old password"""
        INVALID_PASSWORD = self.PASSWORDS.copy()
        INVALID_PASSWORD['old_password'] = '123userPassword'
        response = self.client.patch(f'/api/users/profile/{self.test_user.pk}',
                                     INVALID_PASSWORD)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            self.test_user.check_password(INVALID_PASSWORD['new_password1']))

    def test_patch_different_new_passwords(self):
        """test update user's password with different new passwords"""
        INVALID_PASSWORD = self.PASSWORDS.copy()
        INVALID_PASSWORD['new_password1'] = '123userPassword'
        response = self.client.patch(f'/api/users/profile/{self.test_user.pk}',
                                     INVALID_PASSWORD)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            self.test_user.check_password(INVALID_PASSWORD['new_password1']))

    def test_patch_invalid_new_password(self):
        """test update user's password with invalid new password"""
        INVALID_PASSWORD = self.PASSWORDS.copy()
        INVALID_PASSWORD['new_password1'] = '123'
        response = self.client.patch(f'/api/users/profile/{self.test_user.pk}',
                                     INVALID_PASSWORD)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            self.test_user.check_password(INVALID_PASSWORD['new_password1']))
