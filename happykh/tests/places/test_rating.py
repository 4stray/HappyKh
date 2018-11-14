"""Tests for place's rating"""
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from places.api.views import PlaceRatingView
from places.models import Place, PlaceRating, Address
from tests.utils import BaseTestCase
from users.models import User
from .test_place import TEST_ADDRESS_DATA

RATING_URL = '/api/places/rating/%d'
TEST_PLACE_DATA = {
    'name': 'test name',
    'description': 'test description',
    'logo': 'undefined',
}

TEST_USER_DATA = {
    'password': 'testpassword',
    'age': 18,
    'gender': 'M',
    'first_name': 'name',
    'last_name': 'lastName',
    'is_active': True
}
TEST_RATING_DATA = {
    'rating': 4,
}


class TestPlaceRating(BaseTestCase, APITestCase):
    """Test rating"""
    def setUp(self):
        """Create user and place objects"""
        super().setUp()
        self.user = User.objects.create_user(email='test@mail.com',
                                             **TEST_USER_DATA)
        self.hashed_user_id = self.HASH_IDS.encode(self.user.pk)
        self.new_user = User.objects.create_user(email='test_new@mail.com',
                                                 **TEST_USER_DATA)
        self.hashed_new_user_id = self.HASH_IDS.encode(self.new_user.pk)
        self.address = Address.objects.create(**TEST_ADDRESS_DATA)
        self.place = Place.objects.create(user=self.user, address=self.address,
                                          **TEST_PLACE_DATA)
        user_token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)
        self.rating = PlaceRating.objects.create(user=self.user,
                                                 place=self.place,
                                                 **TEST_RATING_DATA)

    def test_get(self):
        """
        Test get request for rating
        """
        response = self.client.get(RATING_URL % self.place.pk)
        average_rating = PlaceRatingView.get_average(self.place.pk)
        expected = {'place': self.place.pk,
                    'rating': average_rating}
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertDictEqual(expected, response.data)

    def test_post_update(self):
        """
        Test post request for rating update
        """
        data = {
            'place': self.place.pk,
            'user': self.hashed_user_id,
            'rating': 2,
        }
        response = self.client.post(RATING_URL % self.place.pk, data)
        expected = {'place': self.place.pk,
                    'user': self.hashed_user_id,
                    'rating': data['rating']}
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertDictEqual(expected, response.data)

    def test_post_create(self):
        """
        Test post request for rating creation
        """
        data = {
            'place': self.place.pk,
            'user': self.hashed_new_user_id,
            'rating': TEST_RATING_DATA['rating'],
        }
        response = self.client.post(RATING_URL % self.place.pk, data)
        expected = {'place': self.place.pk,
                    'user': self.hashed_new_user_id,
                    'rating': data['rating']}
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        self.assertDictEqual(expected, response.data)
