"""Test users api views"""
import os
from io import BytesIO

from PIL import Image
# pylint: disable = no-member
from django.core.files.uploadedfile import UploadedFile
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from users.api.serializers import UserSerializer, EmailSerializer
from users.models import User

from utils import delete_std_images_from_media
from ..utils import BaseTestCase


USERS_PROFILE_URL = '/api/users/%s'
USERS_PROFILE_DATA_URL = '/api/users/%s/data'
USERS_PROFILE_EMAIL_URL = '/api/users/%s/email'
USERS_PROFILE_PASSWORD_URL = '/api/users/%s/password'

CORRECT_DATA = {
    'email': 'test@mail.com',
    'password': 'testpassword1',
    'age': 20,
    'gender': 'M',
    'first_name': 'firstName',
    'last_name': 'lastName',
    'is_active': True,
    'profile_image': '',
}


class TestUserProfile(BaseTestCase, APITestCase):
    """Test user profile view"""

    def setUp(self):
        """Create test user for testing"""
        super().setUp()
        self.test_user = User.objects.create_user(**CORRECT_DATA)
        self.hashed_user_id = self.HASH_IDS.encode(self.test_user.pk)
        user_token = Token.objects.create(user=self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)
        self.password = {
            'old_password': CORRECT_DATA['password'],
            'new_password': 'password2',
        }

    def tearDown(self):
        """ teardown any state that were previously setup with a call of
        setup.
        """
        instance = self.test_user
        if instance.profile_image:
            # delete images that were created in test
            delete_std_images_from_media(instance.profile_image,
                                         User.VARIATIONS_PROFILE_IMAGE
                                         )

    def test_get(self):
        """test if user exists"""

        response = self.client.get(USERS_PROFILE_URL % self.hashed_user_id)
        serializer = UserSerializer(self.test_user)
        expected = serializer.data
        expected['enable_editing_profile'] = True

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(expected, response.data)

    def test_get_unauthorized_user(self):
        """test if user is unauthorized"""
        new_test_user = User.objects.create_user(email="second@test.com",
                                                 password="password2")
        new_client = APIClient()
        response = new_client.get(USERS_PROFILE_DATA_URL % new_test_user.pk)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_patch_update_age(self):
        """test update user's age"""
        edited_user = User.objects.get(pk=self.test_user.pk)
        edited_user.age = 41
        response = self.client.patch(USERS_PROFILE_DATA_URL % self.hashed_user_id,
                                     {'age': edited_user.age})

        serializer_edited_user = UserSerializer(edited_user)
        expected = serializer_edited_user.data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected, response.data)

        serializer = UserSerializer(self.test_user)
        self.assertNotEqual(serializer.data, response.data)
        self.assertIn(edited_user, User.objects.all())

        # age == 'null'
        edited_user = User.objects.get(pk=self.test_user.pk)
        edited_user.age = None
        response = self.client.patch(USERS_PROFILE_DATA_URL % self.hashed_user_id,
                                     {'age': 'null'})

        serializer_edited_user = UserSerializer(edited_user)
        expected = serializer_edited_user.data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected, response.data)

        serializer = UserSerializer(self.test_user)
        self.assertNotEqual(serializer.data, response.data)
        self.assertIn(edited_user, User.objects.all())

    def test_patch_update_profile_image(self):
        """test update user's profile image"""
        image_file = BytesIO()
        image = Image.new('RGBA', size=(50, 50), color=(256, 0, 0))
        image.save(image_file, 'png')
        image_file.seek(0)
        image = UploadedFile(image_file, "filename.png", "image/png",
                             len(image_file.getvalue()))
        request_data = {'profile_image': image}
        response = self.client.patch(USERS_PROFILE_URL % self.hashed_user_id,
                                     request_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.test_user.refresh_from_db()
        self.assertNotEqual('', self.test_user.profile_image)
        self.assertTrue(os.path.exists(self.test_user.profile_image.path))
        self.assertTrue(os.path.isfile(self.test_user.profile_image.path))

    def test_patch_invalid_update(self):
        """test update user's age with invalid value"""
        edited_user = User.objects.get(pk=self.test_user.pk)
        edited_user.age = -41
        response = self.client.patch(USERS_PROFILE_DATA_URL % self.hashed_user_id,
                                     {'age': edited_user.age})
        serializer_edited_user = UserSerializer(edited_user)
        expected = serializer_edited_user.data["age"]
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertRaises(ValueError)

        response = self.client.get(USERS_PROFILE_DATA_URL % self.hashed_user_id)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertNotEqual(expected, response.data["age"])
        self.assertIsNot(edited_user, User.objects.get(pk=self.test_user.pk))

    def test_patch_update_password(self):
        """test update user's password"""
        response = self.client.patch(
            USERS_PROFILE_PASSWORD_URL % self.hashed_user_id,
            self.password)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_patch_invalid_update_password(self):
        """test update user's password with wrong old password"""
        invalid_password = self.password.copy()
        invalid_password['old_password'] = '123userPassword'
        response = self.client.patch(
            USERS_PROFILE_PASSWORD_URL % self.hashed_user_id,
            invalid_password)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertFalse(
            self.test_user.check_password(invalid_password['new_password'])
        )

    def test_patch_invalid_new_password(self):
        """test update user's password with invalid new password"""
        invalid_password = self.password.copy()
        invalid_password['new_password'] = ''
        response = self.client.patch(
            USERS_PROFILE_PASSWORD_URL % self.hashed_user_id,
            invalid_password)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertFalse(
            self.test_user.check_password(invalid_password['new_password'])
        )

    def test_patch_update_email(self):
        """test update user's email"""
        edited_email = 'valid@mail.com'
        response = self.client.patch(
            USERS_PROFILE_EMAIL_URL % self.hashed_user_id,
            {'email': edited_email})

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        updated_user = User.objects.get(pk=self.test_user.pk)
        self.assertFalse(updated_user.is_active)

    def test_patch_invalid_email(self):
        """test update user's email with invalid email format"""
        invalid_email = 'invalid_email_format'
        serializer = EmailSerializer(self.test_user, invalid_email)
        response = self.client.patch(
            USERS_PROFILE_EMAIL_URL % self.hashed_user_id,
            {'email': invalid_email})

        self.assertFalse(serializer.is_valid())
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_patch_existing_email(self):
        """test update user's email with email of existing user"""
        testing_email = "second@test.com"
        User.objects.create_user(email=testing_email, password="password2")
        response = self.client.patch(
            USERS_PROFILE_EMAIL_URL % self.hashed_user_id,
            {'email': testing_email})

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_patch_invalid_profile_image(self):
        """test update user's password with invalid new password"""
        incorrect_data = {}
        for key in CORRECT_DATA:
            incorrect_data[key] = CORRECT_DATA[key]

        incorrect_data['profile_image'] = 'not_base64'
        response = self.client.patch(USERS_PROFILE_URL % self.hashed_user_id,
                                     incorrect_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertNotEqual(
            self.test_user.profile_image, incorrect_data['profile_image']
        )
        self.assertEqual('', self.test_user.profile_image)

        incorrect_data['profile_image'] = 'some_file.py'
        response = self.client.patch(USERS_PROFILE_URL % self.hashed_user_id,
                                     incorrect_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertNotEqual(
            self.test_user.profile_image, incorrect_data['profile_image']
        )
        self.assertEqual('', self.test_user.profile_image)
