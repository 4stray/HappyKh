"""Tests for places"""
import json

from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import (APITestCase, APIClient)
from tests.utils import BaseTestCase
from users.models import User
from places.api.serializers import PlaceSerializer
from places.models import Place, Address, CommentPlace

PLACE_URL = '/api/places/'
SPECIFYING_PAGINATION_PLACE_URL = '/api/places/?lim={0}&p={1}'
SPECIFYING_FILTER_PLACE_URL = '/api/places/?s={}'

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
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')

    def test_get(self):
        """Test get request for places"""
        response = self.client.get(PLACE_URL)
        serializer = PlaceSerializer(self.places, many=True)
        expected = serializer.data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected, response.data.get('places'))

    def test_post(self):
        """Test post request for places"""
        data = TEST_PLACE_DATA_POST.copy()
        data['address'] = json.dumps(TEST_ADDRESS_DATA)
        response = self.client.post(PLACE_URL, data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_invalid_post(self):
        """Test post request for places with wrong data"""
        data = TEST_PLACE_DATA_POST.copy()
        data.pop('name')
        data.pop('logo')
        data['address'] = json.dumps(TEST_ADDRESS_DATA)
        response = self.client.post(PLACE_URL, data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_creating_place_with_nonjson_address(self):
        """Test response when creating place with wrong json address format"""
        test_data = TEST_PLACE_DATA_POST.copy()
        test_data['address'] = 'nonjson format'

        response = self.client.post(f'{PLACE_URL}', test_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_creating_place_with_not_formatted_address(self):
        """Test response when creating place with wrong address format"""
        test_data = TEST_PLACE_DATA_POST.copy()
        test_data['address'] = json.dumps({
            'longitude': 50,
            'address': 'New Test Address',
        })

        response = self.client.post(f'{PLACE_URL}', test_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

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
        response = self.client.get(f'{PLACE_URL}{self.place.pk}')
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

    def test_changing_place_with_wrong_address(self):
        """Test response when changing place with wrong address format"""
        test_data = TEST_PLACE_DATA_PUT.copy()
        test_data['address'] = 'nonjson format'

        response = self.client.put(f'{PLACE_URL}{self.place.id}', test_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

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

    def test_changing_place_with_nonjson_address(self):
        """Test response when changing place with wrong json address format"""
        test_data = TEST_PLACE_DATA_POST.copy()
        test_data['address'] = 'nonjson format'

        response = self.client.put(f'{PLACE_URL}{self.place.id}', test_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_changing_place_with_not_formatted_address(self):
        """Test response when changing place with wrong address format"""
        test_data = TEST_PLACE_DATA_POST.copy()
        test_data['address'] = json.dumps({
            'longitude': 50,
            'address': 'New Test Address',
        })

        response = self.client.put(f'{PLACE_URL}{self.place.id}', test_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

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
        response = self.client.get(f'{PLACE_URL}0/editing_permission')

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
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')

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
            f'{PLACE_URL}{self.place.id}/editing_permission'
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)


class TestMultiplePlaces(BaseTestCase, APITestCase):
    """Test places with number of instances"""

    def setUp(self):
        """Create user and couple place's instances"""
        super().setUp()
        self.user = User.objects.create_user(**CORRECT_USER_DATA)
        self.hashed_user_id = self.HASH_IDS.encode(self.user.pk)
        self.address = Address.objects.create(**TEST_ADDRESS_DATA)
        self.default_limit = 15

        Place.objects.create(address=self.address,
                             name='A first name',
                             description='description',
                             logo='')

        Place.objects.create(address=self.address,
                             name='B second name',
                             description='description',
                             logo='')

        self.places = Place.objects.all()
        user_token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)

    def test_get_multiple_places_specifying_invalid_str_params(self):
        """
        Test get request for multiple specifying
        limit and page params with str values
        """
        response = self.client.get(SPECIFYING_PAGINATION_PLACE_URL.format(
            'bad', 'params'))
        serializer = PlaceSerializer(self.places, many=True)

        paginator = Paginator(serializer.data, self.default_limit)
        expected = paginator.get_page(1)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.object_list, response.data['places'])
        self.assertEqual(paginator.count, response.data['total_number'])
        self.assertEqual(expected.number, response.data['current_page'])
        self.assertEqual(self.default_limit, response.data['objects_limit'])

    def test_get_multiple_places_specifying_invalid_value_params(self):
        """
        Test get request for multiple specifying
        limit and page params with nonpositive values
        """
        response = self.client.get(SPECIFYING_PAGINATION_PLACE_URL.format(
            -1, -1))
        serializer = PlaceSerializer(self.places, many=True)

        specific_limit = 1  # limit sets 1 if param value is nonpositive
        paginator = Paginator(serializer.data, specific_limit)
        expected = paginator.get_page(paginator.num_pages)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.object_list, response.data['places'])
        self.assertEqual(paginator.count, response.data['total_number'])
        self.assertEqual(expected.number, response.data['current_page'])
        self.assertEqual(specific_limit, response.data['objects_limit'])

    def test_get_multiple_places_specifying_filter_param(self):
        """
        Test get request for multiple places
        specifying search param for filtering
        """
        filter_param = 'first'
        response = self.client.get(SPECIFYING_FILTER_PLACE_URL.format(
            filter_param))

        filtered_places = Place.objects.filter(name__icontains=filter_param)
        serializer = PlaceSerializer(filtered_places, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data['places'])


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
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')

        self.comment_info = {
            'creator': self.user,
            'text': 'Lol_test',
            'place': self.place,
        }

        self.comment = CommentPlace.objects.create(**self.comment_info)
        self.pk = CommentPlace.objects.last().pk
        self.comment_count = CommentPlace.objects.count()

        place_pk = self.place.pk
        self.COMMENT_URL = f'{PLACE_URL}{place_pk}/comments'
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
        get_url = f'{self.COMMENT_URL}?page=2&objects_per_page=1'
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
        self.assertEqual(1, len(response.data['comments']))
        self.assertEqual(comment.text, response.data['comments'][0]['text'])

    def test_get_with_wrong_page_attr(self):
        """Test response for get with wrong page attribute"""
        wrong_get_url = f'{self.COMMENT_URL}?page=0&objects_per_page=1'
        response = self.client.get(wrong_get_url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_get_with_wrong_object_per_page_attr(self):
        """Test response for get with wrong object per page attribute"""
        wrong_get_url = f'{self.COMMENT_URL}?page=1&objects_per_page=-1'
        response = self.client.get(wrong_get_url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_get_with_missing_page_attr(self):
        """Test get with missing page attribute"""
        wrong_get_url = f'{self.COMMENT_URL}?objects_per_page=1'
        response = self.client.get(wrong_get_url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_get_with_missing_object_per_page_attr(self):
        """Test get with missing object per page attribute"""
        wrong_get_url = f'{self.COMMENT_URL}?objects_per_page=0'
        response = self.client.get(wrong_get_url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_get_with_wrong_place(self):
        """Test get request with wrong place id"""
        wrong_get_url = '/api/places/0/comments'
        response = self.client.get(wrong_get_url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_get_without_comments_in_db(self):
        """Test get response to empty comment table"""
        get_url = f'{self.COMMENT_URL}?page=2&objects_per_page=1'
        CommentPlace.objects.all().delete()
        response = self.client.get(get_url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_successful_post(self):
        """Test successful post request"""
        data = self.comment_info
        data['creator'] = self.hashed_user_id
        response = self.client.post(self.COMMENT_URL, data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.comment_count + 1, CommentPlace.objects.count())

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
        url = f'{self.COMMENT_URL}/{self.pk + 40}'
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

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
        url = f'{self.COMMENT_URL}/{self.pk + 40}'
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

    def test_update_with_wrong_user(self):
        """Test put request with user id, who is not a creator of the comment"""
        new_user_data = CORRECT_USER_DATA.copy()
        new_user_data.update(email='test2@mail.com')
        new_user_data.update(password='testpassword2')
        new_user_data.update(first_name='firstName2')

        new_user = User.objects.create_user(**new_user_data)
        new_hashed_user_id = self.HASH_IDS.encode(new_user.pk)

        new_user_token = Token.objects.create(user=new_user)
        temp_client = APIClient()
        temp_client.credentials(
            HTTP_AUTHORIZATION=f'Token {new_user_token.key}')

        data = self.comment_info.copy()
        data.update(creator=new_hashed_user_id)
        data.update(id=self.pk)
        data.update(text=self.comment_info.get('text') + 'test')
        response = temp_client.put(self.SINGLE_COMMENT_URL, data)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
