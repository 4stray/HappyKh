import pytest
from tests.utils import BaseTestCase

pytest_mark = pytest.mark.django_db


@pytest.mark.django_db
class DbConnectionTestCase(BaseTestCase):
    """Testing database for tests"""
    pytest_mark = pytest.mark.django_db

    def test_db_name(self):
        """Created own database for tests"""
        from django.db import connections
        self.assertEqual(connections.databases['default']['NAME'],
                         'test_happykh')
