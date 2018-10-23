from rest_framework.test import APITestCase
from rest_framework import status
from tests.utils import BaseTestCase
from places.models import Place
from places.api.serializers import PlaceSerializer
from users.models import User
from rest_framework.authtoken.models import Token

PLACE_URL = '/api/places/'
SINGLE_PLACE_URL = '/api/places/%d'

TEST_PLACE_DATA = {
    'name': 'test name',
    'description': 'test description',
    'logo': '',
}

TEST_PLACE_DATA_POST = {
    'name': 'test name',
    'description': 'test description',
    'logo': 'undefined',
}

CORRECT_USER_DATA = {
    'email': 'test@mail.com',
    'password': 'testpassword',
    'age': 20,
    'gender': 'M',
    'first_name': 'firstName',
    'last_name': 'lastName',
    'is_active': True
}


class TestPlacePage(BaseTestCase, APITestCase):

    def setUp(self):
        """Create user and place objects"""
        self.user = User.objects.create_user(**CORRECT_USER_DATA)
        self.place = Place.objects.create(user=self.user, **TEST_PLACE_DATA)
        self.places = Place.objects.all()
        user_token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)

    def test_get(self):
        response = self.client.get(PLACE_URL)
        serializer = PlaceSerializer(self.places, many=True)
        expected = serializer.data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected, response.data)

    def test_post(self):
        data = TEST_PLACE_DATA_POST
        data['user'] = self.user.pk
        response = self.client.post(PLACE_URL, data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_get_single_place(self):
        """Gets single place data"""
        response = self.client.get(SINGLE_PLACE_URL % self.place.pk)
        serializer = PlaceSerializer(self.place)
        expected = serializer.data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(expected, response.data)
