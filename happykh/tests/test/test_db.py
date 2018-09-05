import pytest
from tests.utils import BaseTestCase


@pytest.mark.django_db
class DbConnectionTestCase(BaseTestCase):

    def test_db_name(self):
        from django.db import connections
        self.assertEqual(connections.databases['default']['NAME'], 'test_happykh')
