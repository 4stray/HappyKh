from tests.utils import BaseTestCase


User = type('User', (object,), dict(firstname='Firstname', lastname='Lastname'))


class TestUser(BaseTestCase):
    def test_default_user_creation(self):
        user = User()
        self.assertIsInstance(user, User)
        self.assertEqual(user.firstname, 'Firstname')
        self.assertEqual(user.lastname, 'Lastname')
