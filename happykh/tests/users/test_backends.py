"""Test users api views"""
# pylint: disable = no-member
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from users.models import User
from users.backends import UserAuthentication
from utils import delete_std_images_from_media
from ..utils import BaseTestCase

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


class TestTokenValidation(BaseTestCase, APITestCase):
    """Test token relevance"""

    def setUp(self):
        self.test_user = User.objects.create_user(**CORRECT_DATA)
        self.test_user_token = Token.objects.create(user=self.test_user)

    def tearDown(self):
        """ teardown any state that were previously setup with a call of
        setup.
        """
        instance = self.test_user
        if instance.profile_image:
            # delete images that were created in test
            delete_std_images_from_media(
                instance.profile_image,
                User.VARIATIONS_PROFILE_IMAGE
            )

    def test_user_on_account_ownership(self):
        mocked_request = {
            'HTTP_AUTHORIZATION': 'Token ' + self.test_user_token.key,
        }

        mocked_request = type('', (), dict(META=mocked_request))
        is_owner = UserAuthentication.is_owner(mocked_request,
                                               self.test_user.id)
        self.assertEqual(True, is_owner)

    def test_getting_user_by_id(self):
        user = UserAuthentication.get_user_by_id(self.test_user.id)
        self.assertEqual(self.test_user, user)

    def test_getting_wrong_user_by_id(self):
        user = UserAuthentication.get_user_by_id(0)
        self.assertEqual(None, user)
