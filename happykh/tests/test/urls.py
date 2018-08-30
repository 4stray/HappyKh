from tests.utils import BaseTestCase
from django.urls import is_valid_path


class UrlsTestCase(BaseTestCase):
    def test_index_url(self):
        self.assertNotEqual(is_valid_path('/'), True)
