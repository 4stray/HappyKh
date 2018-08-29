User = type('User', (object,), dict(firstname='Firstname', lastname='Lastname'))


class TestUser:
    def test_default_user_creation(self):
        user = User()
        assert user.firstname == 'Firstname'
        assert user.lastname == 'Lastname'

