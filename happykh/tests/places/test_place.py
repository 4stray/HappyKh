import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from places.api.serializers import PlaceSerializer
from places.models import Place, Address
from tests.utils import BaseTestCase
from users.models import User

PLACE_URL = '/api/places/'
SINGLE_PLACE_URL = '/api/places/%d'

TEST_ADDRESS_DATA = {
    'latitude': 50,
    'longitude': 34,
    'address': 'some str',
}

TEST_PLACE_DATA = {
    'name': 'test name',
    'description': 'test description',
    'logo': '',
}

TEST_PLACE_DATA_POST = {
    'name': 'test name',
    'description': 'test description',
    'logo': 'undefined',
    'address': 1,
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
        super().setUp()
        self.user = User.objects.create_user(**CORRECT_USER_DATA)
        self.hashed_user_id = self.HASH_IDS.encode(self.user.pk)
        self.address = Address.objects.create(**TEST_ADDRESS_DATA)
        self.place = Place.objects.create(user=self.user, address=self.address,
                                          **TEST_PLACE_DATA)
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
        data['user'] = self.hashed_user_id
        data['address'] = json.dumps(TEST_ADDRESS_DATA)
        response = self.client.post(PLACE_URL, data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_get_single_place(self):
        """Gets single place data"""
        response = self.client.get(SINGLE_PLACE_URL % self.place.pk)
        serializer = PlaceSerializer(self.place)
        expected = serializer.data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(expected, response.data)
