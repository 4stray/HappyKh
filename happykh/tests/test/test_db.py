import pytest
from tests.utils import BaseTestCase


@pytest.mark.django_db
class DbConnectionTestCase(BaseTestCase):
    """Testing database for tests"""

    def test_db_name(self):
        """Created own database for tests"""
        from django.db import connections
        self.assertEqual('test_happykh',
                         connections.databases['default']['NAME'])
