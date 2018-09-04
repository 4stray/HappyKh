"""Tests for models of users app"""
from tests.utils import BaseTestCase
from users.models import User


class UserTestCase(BaseTestCase):
    """Tests for user model"""
    def setUp(self):
        """Create user objects"""
        User.objects.create_user(email='any@mail.com', password='password')
        User.objects.create_user(email='no@pass.com', password='')
        User.objects.create_superuser(email='admin@mail.com', password='password',
                                      first_name='fn', last_name='ln', age=12)

    def test_user_creation(self):
        """Testing default user attributes"""
        user = User.objects.get(email='any@mail.com')
        self.assertIsInstance(user, User)
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')
        self.assertIsNone(user.age)
        self.assertEqual(user.gender, 'W')
        self.assertEqual(user.email, 'any@mail.com')
        self.assertEqual(user.check_password('password'), True)
        self.assertEqual(user.has_usable_password(), True)
        self.assertEqual(user.is_active, True)

    def test_default_perm(self):
        """Test default user permissions"""
        user = User.objects.get(email='any@mail.com')
        self.assertEqual(user.is_admin, False)
        self.assertEqual(user.is_staff, False)

    def test_admin_perm(self):
        """Test admin permissions"""
        user = User.objects.get(email='admin@mail.com')
        self.assertEqual(user.is_admin, True)
        self.assertEqual(user.is_staff, True)

    def test_email_exception(self):
        """Test empty email error"""
        with self.assertRaises(ValueError) as ve:
            User.objects.create_user(email='', password='password')
        self.assertEqual(ve.exception, ValueError)

    def test_empty_password(self):
        """Test is usable empty password"""
        user = User.objects.get(email='no@pass.com')
        self.assertEqual(user.check_password(''), False)
        self.assertEqual(user.has_usable_password(), False)
