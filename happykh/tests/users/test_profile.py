"""Test user profile"""
from rest_framework.test import APITestCase
from tests.utils import BaseTestCase
from users.models import User


class ProfileViewTestCase(BaseTestCase, APITestCase):
    """
    Test user profile api

    """

    def setUp(self):
        """Create user instance for tests"""
        User.objects.create_user(email='test@mail.com', password='testpassword')

    def tearDown(self):
        """Delete user instance for tests"""
        User.objects.filter(email='test@mail.com').delete()

    def test_save_correct_password(self):
        """Test view response for new password saving"""
        pass

    def test_save_invalid_password(self):
        """Test view response for saving invalid password"""
        pass

    def test_save_empty_password(self):
        """Test view response for empty password before saving"""
        pass

    def test_save_correct_email(self):
        """Test view response for new password saving"""
        pass

    def test_save_invalid_email(self):
        """Test view response for saving invalid password"""
        pass

    def test_save_empty_email(self):
        """Test view response for empty password before saving"""
        pass

    def test_save_first_name(self):
        """Test view response for new first name saving"""
        pass

    def test_save_empty_first_name(self):
        """Test view response for empty first name saving"""
        pass

    def test_save_last_name(self):
        """Test view response for new last name saving"""
        pass

    def test_save_empty_last_name(self):
        """Test view response for empty last name saving"""
        pass

    def test_save_correct_age(self):
        """Test view response for new age value before saving"""
        pass

    def test_save_invalid_age(self):
        """Test view response for invalid age value before saving"""
        pass

    def test_save_empty_age(self):
        """Test view response for empty age value before saving"""
        pass

    def test_gender_edit(self):
        """Test change gender"""
        pass

    def test_load_new_profile_image(self):
        """Test change profile_image"""
        pass
