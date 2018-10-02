"""Tests for models of users app"""
import pytest
from tests.utils import BaseTestCase
from places.models import Place
from users.models import User



@pytest.mark.django_db
class PlaceTestCase(BaseTestCase):
    """Tests for user model"""

    def setUp(self):
        """Create user objects"""
        self.regular_user = User.objects.create_user(email='any@mail.com',
                                                     password='password')
        self.place = Place.objects.create(user=self.regular_user)

    def test_place_creation(self):
        """Testing default user attributes"""
        place = self.place
        self.assertIsInstance(place, Place)
        self.assertEqual('', place.name)
        self.assertEqual('', place.description)
        self.assertEqual('', place.image)
    