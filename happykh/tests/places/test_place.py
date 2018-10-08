from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from tests.utils import BaseTestCase
from places.models import Place
from places.api.serializers import PlaceSerializer
from users.models import User
from rest_framework.authtoken.models import Token



PLACE_URL = '/api/places/'
TEST_USER_DATA = {
            'name': 'test name',
            'description': 'test description',
            'logo': 'test logo',
            'user': '',
        }


class TestPlacePage(BaseTestCase, APITestCase):

    def setUp(self):
        """Create user and place objects"""
        self.user = User.objects.create_user(email='testplace@mail.com',
                                             password='password')
        self.place = Place.objects.create(name=TEST_USER_DATA['name'],
                                          description=TEST_USER_DATA['description'],
                                          logo=TEST_USER_DATA['logo'],
                                          user=self.user)
        self.places = Place.objects.all()
        user_token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)
        self.client.force_authenticate(user=self.user)


    def test_get(self):
        response = self.client.get(PLACE_URL)
        serializer = PlaceSerializer(self.places, many=True)
        expected = serializer.data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected, response.data)

    def test_post(self):
        data = TEST_USER_DATA
        data['user'] = self.user.pk
        response = self.client.post(PLACE_URL, data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

