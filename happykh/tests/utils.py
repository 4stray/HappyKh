"""Setup module for tests"""
# pylint: disable = useless-super-delegation
from unittest import TestCase


class BaseTestCase(TestCase):
    """Setup class for unittests"""
    def setUp(self):
        super(BaseTestCase, self).setUp()

    def tearDown(self):
        super(BaseTestCase, self).tearDown()
