"""Tests for models of places app"""
import pytest
from tests.utils import BaseTestCase
from places.models import Place
from users.models import User


@pytest.mark.django_db
class PlaceTestCase(BaseTestCase):
    """Tests for place model"""

    def setUp(self):
        """Create user and place objects"""
        self.regular_user = User.objects.create_user(email='any@mail.com',
                                                     password='password')
        self.place = Place.objects.create(user=self.regular_user)

    def test_place_creation(self):
        """Testing default place attributes"""
        place = self.place
        self.assertIsInstance(place, Place)
        self.assertEqual('', place.name)
        self.assertEqual('', place.description)
        self.assertEqual('', place.logo)

    def test_deletion_user(self):
        """Testing Place model behavior after deleting a user"""
        user_on_delete = self.regular_user

        User.objects.get(email="any@mail.com").delete()
        with self.assertRaises(Place.DoesNotExist) as dne:
            Place.objects.get(user=user_on_delete)
        self.assertEqual(type(dne.exception), Place.DoesNotExist)
