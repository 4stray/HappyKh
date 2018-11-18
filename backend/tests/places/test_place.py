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


class TestPlacePageWithPermission(BaseTestCase, APITestCase):
    """Test user CRUD place with editing place permission """

    def setUp(self):
        """Create user and place objects"""
        super().setUp()
        self.user = User.objects.create_user(**CORRECT_USER_DATA)
        self.hashed_user_id = self.HASH_IDS.encode(self.user.pk)
        self.address = Address.objects.create(**TEST_ADDRESS_DATA)
        self.place = Place.objects.create(address=self.address,
                                          **TEST_PLACE_DATA)

        self.place.edit_permitted_users.add(self.user)

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
        data['address'] = json.dumps(TEST_ADDRESS_DATA)
        response = self.client.post(PLACE_URL, data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_delete_existing_place(self):
        """Test response for place deletion"""
        response = self.client.delete(f'{PLACE_URL}{self.place.id}')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

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

        response = self.client.put(f'{PLACE_URL}{self.place.id}', test_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_changing_place_with_invalid_id(self):
        """Test response for changing place with invalid id"""
        test_data = TEST_PLACE_DATA_PUT.copy()

        response = self.client.put(f'{PLACE_URL}{0}', test_data)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_changing_place_with_blank_name(self):
        """Test response for changing place with no name"""
        test_data = TEST_PLACE_DATA_PUT.copy()
        test_data['name'] = ''

        response = self.client.put(f'{PLACE_URL}{self.place.id}', test_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_changing_place_text_fields(self):
        """Test response for changing place"""
        test_data = TEST_PLACE_DATA_PUT.copy()
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

        response = self.client.put(f'{PLACE_URL}{self.place.id}', test_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_having_permission_for_place_editing(self):
        """Test user on having permission for editing place """
        test_data = TEST_PLACE_DATA_PUT.copy()
        response = self.client.get(
            f'{PLACE_URL}{self.place.id}/editing_permission',
            test_data
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(True, response.data.get('is_place_editing_permitted'))

    def test_getting_permission_of_nonexisting_place(self):
        """Test getting user permission of unexisting place"""
        response = self.client.get(
            f'{PLACE_URL}{0}/editing_permission'
        )

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class TestPlacePageWithoutEditingPermission(APITestCase):
    """ Test changing place without having permission for it """

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(**CORRECT_USER_DATA)

        self.address = Address.objects.create(**TEST_ADDRESS_DATA)
        self.place = Place.objects.create(address=self.address,
                                          **TEST_PLACE_DATA)

        self.places = Place.objects.all()
        user_token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)

    def test_getting_no_permission_for_place_editing(self):
        """ Check getting the response without editing place permission
        for the test user """
        test_data = TEST_PLACE_DATA_PUT.copy()
        response = self.client.get(
            f'{PLACE_URL}{self.place.id}/editing_permission',
            test_data
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(False,
                         response.data.get('is_place_editing_permitted'))

    def test_changing_place_address(self):
        """ Attempt to change place without having a permission for it """
        test_data = TEST_PLACE_DATA_PUT.copy()
        test_data['address'] = json.dumps({
            'longitude': 50,
            'latitude': 49.99,
            'address': 'New Test Address',
        })

        response = self.client.put(f'{PLACE_URL}{self.place.id}', test_data)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_deleting_place(self):
        """ Attempt to delete place without having a permission for it """
        test_data = TEST_PLACE_DATA_PUT.copy()

        response = self.client.delete(f'{PLACE_URL}{self.place.id}', test_data)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_requesting_editing_permission(self):
        """ Send an email to admin with request to get a permission for editing
        place"""
        response = self.client.post(
            f'{PLACE_URL}{self.place.id}/editing_permission_request'
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)


class TestCommentsAPI(BaseTestCase, APITestCase):
    """Test comments for places"""

    def setUp(self):
        """Create user, place and comment objects"""
        super().setUp()
        self.user = User.objects.create_user(**CORRECT_USER_DATA)
        self.hashed_user_id = self.HASH_IDS.encode(self.user.pk)
        self.address = Address.objects.create(**TEST_ADDRESS_DATA)
        self.place = Place.objects.create(address=self.address,
                                          **TEST_PLACE_DATA)
        self.places = Place.objects.all()
        user_token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)

        self.comment_info = {
            'creator': self.user,
            'text': 'Lol_test',
            'place': self.place,
        }
        self.COMMENT_URL = '/api/places/' + str(self.place.id) + '/comments'

        self.comment = CommentPlace.objects.create(
            # pylint: disable=duplicate-code
            creator=self.comment_info['creator'],
            text=self.comment_info['text'],
            place=self.comment_info['place'],
        )
        self.pk = CommentPlace.objects.last().pk
        self.comment_count = CommentPlace.objects.count()
        self.place_pk = self.places.last().pk
        self.COMMENT_URL = f'/api/places/{self.place_pk}/comments'
        self.SINGLE_COMMENT_URL = f'{self.COMMENT_URL}/{self.pk}'

    def test_successful_get(self):
        """Test response for successful get"""
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
        """Test response for get with wrong page attribute"""
        wrong_get_url = self.COMMENT_URL + '?page=0&objects_per_page=1'
        response = self.client.get(wrong_get_url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_get_with_wrong_object_per_page_attr(self):
        """Test response for get with wrong object per page attribute"""
        wrong_get_url = self.COMMENT_URL + '?page=1&objects_per_page=-1'
        response = self.client.get(wrong_get_url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_get_with_missing_page_attr(self):
        """Test get with missing page attribute"""
        wrong_get_url = self.COMMENT_URL + '?objects_per_page=1'
        response = self.client.get(wrong_get_url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_get_with_missing_object_per_page_attr(self):
        """Test get with missing object per page attribute"""
        wrong_get_url = self.COMMENT_URL + '?objects_per_page=0'
        response = self.client.get(wrong_get_url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_get_with_wrong_place(self):
        """Test get request with wrong place id"""
        wrong_get_url = '/api/places/0/comments'
        response = self.client.get(wrong_get_url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_get_without_comments_in_db(self):
        """Test get response to empty comment table"""
        get_url = self.COMMENT_URL + '?page=2&objects_per_page=1'
        CommentPlace.objects.all().delete()
        response = self.client.get(get_url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_successful_post(self):
        """Test successful post request"""
        data = self.comment_info
        data['creator'] = self.hashed_user_id
        response = self.client.post(self.COMMENT_URL, data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.comment_count+1, CommentPlace.objects.count())

    def test_post_with_wrong_place(self):
        """Test post request with wrong place id"""
        comment_url = '/api/places/0/comments'
        data = self.comment_info
        response = self.client.post(comment_url, data)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(self.comment_count, CommentPlace.objects.count())

    def test_post_with_wrong_user(self):
        """Test post request with wrong user id"""
        data = self.comment_info
        data['creator'] = 'KLK'

        response = self.client.post(self.COMMENT_URL, data)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(self.comment_count, CommentPlace.objects.count())

    def test_post_with_invalid_text(self):
        """Test post request with invalid comment text"""
        data = self.comment_info
        data['creator'] = self.hashed_user_id
        data['text'] = ''
        response = self.client.post(self.COMMENT_URL, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(self.comment_count, CommentPlace.objects.count())

    def test_successful_delete(self):
        """Test successful delete request"""
        comment = CommentPlace.objects.create(
            creator=self.comment_info['creator'],
            text=self.comment_info['text'],
            place=self.comment_info['place'],
        )
        url = f'{self.COMMENT_URL}/{comment.pk}'
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_failed_delete(self):
        """Test delete request with wrong comment id"""
        url = self.COMMENT_URL + '/' + str(self.pk + 40)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_successful_update(self):
        """Test successful put request"""
        data = self.comment_info.copy()
        data.update(creator=self.hashed_user_id)
        data.update(id=self.pk)
        data.update(text=self.comment_info.get('text') + 'test')
        response = self.client.put(self.SINGLE_COMMENT_URL, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(True, response.data['edited'])
        self.assertEqual(data['text'], response.data['text'])

    def test_update_with_wrong_id(self):
        """Test put request with wrong comment id"""
        url = self.COMMENT_URL + '/' + str(self.pk + 40)
        data = self.comment_info.copy()
        data.update(creator=self.hashed_user_id)
        response = self.client.put(url, data)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_update_with_invalid_text(self):
        """Test put request with invalid comment text"""
        data = self.comment_info.copy()
        data.update(creator=self.hashed_user_id)
        data.update(id=self.pk)
        data.update(text='')
        response = self.client.put(self.SINGLE_COMMENT_URL, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
