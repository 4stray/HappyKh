"""Tests for models of users app"""
import pytest
from tests.utils import BaseTestCase
from users.models import User


@pytest.mark.django_db
class UserTestCase(BaseTestCase):
    """Tests for user model"""
    def setUp(self):
        """Create user objects"""
        self.regular_user = User.objects.create_user(email='any@mail.com', password='password')
        self.admin_user = User.objects.create_superuser(email='admin@mail.com', password='password')

    def test_user_creation(self):
        """Testing default user attributes"""
        user = self.regular_user
        self.assertIsInstance(user, User)
        self.assertEqual('', user.first_name)
        self.assertEqual('', user.last_name)
        self.assertIsNone(user.age)
        self.assertEqual('W', user.gender)
        self.assertEqual('any@mail.com', user.email)
        self.assertEqual(True, user.check_password('password'))
        self.assertEqual(True, user.has_usable_password())
        self.assertEqual(False, user.is_active)

    def test_default_perm(self):
        """Test default user permissions"""
        user = self.regular_user
        self.assertEqual(False, user.is_staff)

    def test_admin_perm(self):
        """Test admin permissions"""
        user = self.admin_user
        self.assertEqual(True, user.is_staff)

    def test_email_exception(self):
        """Test empty email error"""
        with self.assertRaises(ValueError) as ve:
            User.objects.create_user(email='', password='password')
        self.assertEqual(ValueError, type(ve.exception))

    def test_empty_password(self):  # Test failed, now empty password is allowed for use
        """Test is usable empty password"""
        with self.assertRaises(ValueError) as ve:
            User.objects.create_user(email='no@pass.com', password='')
        self.assertEqual(type(ve.exception), ValueError)
        self.assertEqual('Users must have an non-empty password', str(ve.exception))

    def test_get_short_name_function(self):
        """Test 'get_short_name' function"""
        user = self.regular_user
        self.assertEqual(user.get_short_name(), user.first_name)

    def test_get_full_name_function(self):
        """Test 'get_full_name' function"""
        user = self.regular_user
        self.assertEqual(f'{user.first_name} {user.last_name}'.strip(), user.get_full_name())
        user.first_name = 'First name'
        user.last_name = 'Last name'
        self.assertEqual('First name Last name', user.get_full_name())
