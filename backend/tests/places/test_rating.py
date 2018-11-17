"""Tests for place's rating"""
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from places.api.views import PlaceRatingView
from places.api.serializers import PlaceRatingSerializer
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
        response = self.client.get(RATING_URL % self.place.pk,
                                   {'user': self.hashed_user_id})
        average_rating = PlaceRatingView.get_average(self.place.pk)
        expected = {'place': self.place.pk,
                    'data': average_rating['average'],
                    'amount': average_rating['amount'],
                    'rating': self.rating.rating}
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertDictEqual(expected, response.data)

    def test_get_user_rating(self):
        """Test user's rating"""
        response = PlaceRatingView.get_user_rating(self.user.pk,
                                                   self.place.pk)
        expected = self.rating.rating
        self.assertEqual(expected, response)

    def test_get_invalid_user_rating(self):
        """Test invalid user's rating"""
        response = PlaceRatingView.get_user_rating(self.new_user.pk,
                                                   self.place.pk)
        expected = 0
        self.assertEqual(expected, response)




    def test_get_empty_rating(self):
        """Test rating with invalid place id"""
        place_id = 100
        response = self.client.get(RATING_URL % place_id)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_post_update(self):
        """
        Test post request for rating update
        """
        amount = PlaceRatingView.get_average(self.place.pk)['amount']
        data = {
            'place': self.place.pk,
            'user': self.hashed_user_id,
            'rating': 2,
            'amount': amount,
        }
        response = self.client.post(RATING_URL % self.place.pk, data)
        expected = {'place': self.place.pk,
                    'user': self.hashed_user_id,
                    'rating': data['rating'],
                    'amount': data['amount']}
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertDictEqual(expected, response.data)

    def test_post_update_with_non_existing_user(self):
        """Test send rating with wrong user id"""
        user_id = 100
        data = {
            'place': self.place.pk,
            'user': user_id,
            'rating': 2,
        }
        expected = 'User does not exist'
        response = self.client.post(RATING_URL % self.place.pk, data)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(expected, response.data['detail'])


    def test_post_create(self):
        """
        Test post request for rating creation
        """
        amount = PlaceRatingView.get_average(self.place.pk)['amount']
        data = {
            'place': self.place.pk,
            'user': self.hashed_new_user_id,
            'rating': TEST_RATING_DATA['rating'],
            'amount': amount,
        }
        response = self.client.post(RATING_URL % self.place.pk, data)
        expected = {'place': self.place.pk,
                    'user': self.hashed_new_user_id,
                    'rating': data['rating'],
                    'amount': data['amount']}
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(expected, response.data)

    def test_post_without_user(self):
        """Test post request for rating creation without user id"""
        data = {
            'place': self.place.pk,
            'rating': TEST_RATING_DATA['rating'],
        }
        response = self.client.post(RATING_URL % self.place.pk, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post_create_invalid_rating(self):
        """Test post request with invalid rating format"""
        data = {
            'place': self.place.pk,
            'user': self.hashed_new_user_id,
            'rating': 'rating',
        }
        response = self.client.post(RATING_URL % self.place.pk, data)

        serializer = PlaceRatingSerializer(data=data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertFalse(serializer.is_valid())
