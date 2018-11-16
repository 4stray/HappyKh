"""Tests for places"""
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

TEST_PLACE_DATA_PUT = {
    'name': 'test name',
    'description': 'test description',
    'logo': 'undefined',
    'address': json.dumps(TEST_ADDRESS_DATA),
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
    """Test all places"""

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
        """
        Test get request for places
        """
        response = self.client.get(PLACE_URL)
        serializer = PlaceSerializer(self.places, many=True)
        expected = serializer.data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected, response.data)

    def test_post(self):
        """
        Test post request for places
        """
        data = TEST_PLACE_DATA_POST
        data['user'] = self.hashed_user_id
        data['address'] = json.dumps(TEST_ADDRESS_DATA)
        response = self.client.post(PLACE_URL, data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_delete_existing_place(self):
        """Test response for place deletion"""
        response = self.client.delete(f'{PLACE_URL}{self.place.id}')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_delete_nonexisting_place(self):
        """Test response for deletion of place that doesn't exist"""
        response = self.client.delete(f'{PLACE_URL}0')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_get_single_place(self):
        """Test get request for single place data"""
        response = self.client.get(SINGLE_PLACE_URL % self.place.pk)
        serializer = PlaceSerializer(self.place)
        expected = serializer.data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(expected, response.data)

    def test_changing_place_without_any_change(self):
        """Test response for changing place without changes"""
        test_data = TEST_PLACE_DATA_PUT.copy()
        test_data['user'] = self.hashed_user_id

        response = self.client.put(f'{PLACE_URL}{self.place.id}', test_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_changing_place_with_invalid_id(self):
        """Test response for changing place with invalid id"""
        test_data = TEST_PLACE_DATA_PUT.copy()
        test_data['user'] = self.hashed_user_id

        response = self.client.put(f'{PLACE_URL}{0}', test_data)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_changing_place_with_blank_name(self):
        """Test response for changing place with no name"""
        test_data = TEST_PLACE_DATA_PUT.copy()
        test_data['user'] = self.hashed_user_id
        test_data['name'] = ''

        response = self.client.put(f'{PLACE_URL}{self.place.id}', test_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_changing_place_text_fields(self):
        """Test response for changing place"""
        test_data = TEST_PLACE_DATA_PUT.copy()
        test_data['user'] = self.hashed_user_id
        test_data['name'] = 'New name'
        test_data['description'] = 'New description'

        response = self.client.put(f'{PLACE_URL}{self.place.id}', test_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_changing_place_address(self):
        """Test response for changing place's address"""
        test_data = TEST_PLACE_DATA_PUT.copy()
        test_data['address'] = json.dumps({
            'longitude': 50,
            'latitude': 49.99,
            'address': 'New Test Address',
        })
        test_data['user'] = self.hashed_user_id

        response = self.client.put(f'{PLACE_URL}{self.place.id}', test_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_changing_place_address_for_empty_one(self):
        """Test update place's address for invalid"""
        test_data = TEST_PLACE_DATA_PUT.copy()
        test_data['address'] = json.dumps({
            'longitude': 0,
            'latitude': 0,
            'address': '',
        })
        test_data['user'] = self.hashed_user_id

        response = self.client.put(f'{PLACE_URL}{self.place.id}', test_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class TestCommentsAPI(BaseTestCase, APITestCase):
    """Test comments for places"""

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
        self.comment = CommentPlace.objects.create(
            # pylint: disable=duplicate-code
            creator=self.comment_info['creator'],
            text=self.comment_info['text'],
            place=self.comment_info['place'],
        )
        self.pk = CommentPlace.objects.last().pk
        self.comment_count = CommentPlace.objects.count()
        self.COMMENT_URL = '/api/places/' + str(self.place.id) + '/comments'
        self.SINGLE_COMMENT_URL = \
            f'/api/places/{str(self.place.id)}/comments/{self.pk}'

    def test_successful_get(self):
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

    def test_get_with_wrong_page_attr(self):
        wrong_get_url = self.COMMENT_URL + '?page=0&objects_per_page=1'
        response = self.client.get(wrong_get_url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_get_with_wrong_object_per_page_attr(self):
        wrong_get_url = self.COMMENT_URL + '?page=1&objects_per_page=-1'
        response = self.client.get(wrong_get_url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_get_with_missing_page_attr(self):
        wrong_get_url = self.COMMENT_URL + '?objects_per_page=1'
        response = self.client.get(wrong_get_url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_get_with_missing_object_per_page_attr(self):
        wrong_get_url = self.COMMENT_URL + '?objects_per_page=0'
        response = self.client.get(wrong_get_url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_get_with_wrong_place(self):
        wrong_get_url = '/api/places/0/comments'
        response = self.client.get(wrong_get_url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_get_without_comments_in_db(self):
        get_url = self.COMMENT_URL + '?page=2&objects_per_page=1'
        CommentPlace.objects.all().delete()
        response = self.client.get(get_url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_successful_post(self):
        data = self.comment_info
        data['creator'] = self.hashed_user_id
        response = self.client.post(self.COMMENT_URL, data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.comment_count+1, CommentPlace.objects.count())

    def test_post_with_wrong_place(self):
        comment_url = '/api/places/0/comments'
        data = self.comment_info
        response = self.client.post(comment_url, data)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(self.comment_count, CommentPlace.objects.count())

    def test_post_with_wrong_user(self):
        data = self.comment_info
        data['creator'] = 'KLK'

        response = self.client.post(self.COMMENT_URL, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(self.comment_count, CommentPlace.objects.count())

    def test_post_with_invalid_text(self):
        data = self.comment_info
        data['text'] = None
        response = self.client.post(self.COMMENT_URL, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(self.comment_count, CommentPlace.objects.count())

    def test_successful_delete(self):
        response = self.client.delete(self.SINGLE_COMMENT_URL)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_failed_delete(self):
        url = self.COMMENT_URL + '/' + str(self.pk + 40)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_successful_update(self):
        data = self.comment_info.copy()
        data.update(creator=self.hashed_user_id)
        data.update(id=self.pk)
        data.update(text=self.comment_info.get('text') + 'test')
        response = self.client.put(self.SINGLE_COMMENT_URL, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(True, response.data['edited'])
        self.assertEqual(data['text'], response.data['text'])

    def test_update_with_wrong_id(self):
        url = self.COMMENT_URL + '/' + str(self.pk + 40)
        data = self.comment_info.copy()
        data.update(creator=self.hashed_user_id)
        response = self.client.put(url, data)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_update_with_invalid_text(self):
        data = self.comment_info.copy()
        data.update(creator=self.hashed_user_id)
        data.update(id=self.pk)
        data.update(text='')
        response = self.client.put(self.SINGLE_COMMENT_URL, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
