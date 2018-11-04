import json

from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from places.api.serializers import PlaceSerializer
from places.models import Place, Address, CommentPlace
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


class TestCommentsAPI(BaseTestCase, APITestCase):

    def setUp(self):
        """Create user, place and comment objects"""
        super().setUp()
        self.user = User.objects.create_user(**CORRECT_USER_DATA)
        self.hashed_user_id = self.HASH_IDS.encode(self.user.pk)
        self.address = Address.objects.create(**TEST_ADDRESS_DATA)
        self.place = Place.objects.create(user=self.user, address=self.address,
                                          **TEST_PLACE_DATA)
        self.places = Place.objects.all()
        user_token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)

        self.comment_info = {'creator': self.user,
                             'text': 'Lol_test',
                             'place': self.place,
                             }
        self.COMMENT_URL = '/api/places/' + str(self.place.id) + '/comments'
        self.comment = CommentPlace.objects.create(
            creator=self.comment_info['creator'],
            text=self.comment_info['text'],
            place=self.comment_info['place'],
        )

    def test_get(self):
        comment = CommentPlace.objects.create(
            creator=self.comment_info['creator'],
            text='com2',
            place=self.comment_info['place'],
        )
        CommentPlace.objects.create(
            creator=self.comment_info['creator'],
            text='com3',
            place=self.comment_info['place'],
        )
        get_url = self.COMMENT_URL + '?page=2&objects_per_page=1'
        objects_per_page = 1
        page = 2
        response = self.client.get(get_url)
        paginator = Paginator(CommentPlace.objects.all(), objects_per_page)
        comments_page = paginator.get_page(page)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(paginator.count, response.data['count'])
        self.assertEqual(paginator.num_pages, response.data['number_of_pages'])
        self.assertEqual(comments_page.number,
                         response.data['current_page_number'])
        next_link = 'http://testserver' + self.COMMENT_URL + \
                    '?page=3&objects_per_page=1'
        self.assertEqual(next_link, response.data['next'])
        previous_link = 'http://testserver' + self.COMMENT_URL + \
                        '?page=1&objects_per_page=1'
        self.assertEqual(previous_link, response.data['previous'])
        self.assertEqual(1, len(response.data['comments']))
        self.assertEqual(comment.text, response.data['comments'][0]['text'])

        wrong_get_url = self.COMMENT_URL + '?page=0&objects_per_page=1'
        response = self.client.get(wrong_get_url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        wrong_get_url = self.COMMENT_URL + '?page=1&objects_per_page=-1'
        response = self.client.get(wrong_get_url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        wrong_get_url = self.COMMENT_URL + '?objects_per_page=1'
        response = self.client.get(wrong_get_url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        wrong_get_url = self.COMMENT_URL + '?page=1'
        response = self.client.get(wrong_get_url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        wrong_get_url = '/api/places/0/comments'
        response = self.client.get(wrong_get_url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

        CommentPlace.objects.all().delete()
        response = self.client.get(get_url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_post(self):
        data = self.comment_info
        data['creator'] = self.hashed_user_id

        response = self.client.post(self.COMMENT_URL, data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, CommentPlace.objects.count())

        comment_url = '/api/places/0/comments'
        response = self.client.post(comment_url, data)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(2, CommentPlace.objects.count())

        data['creator'] = 'KLK'
        response = self.client.post(self.COMMENT_URL, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(2, CommentPlace.objects.count())

        data['text'] = None
        response = self.client.post(self.COMMENT_URL, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(2, CommentPlace.objects.count())
