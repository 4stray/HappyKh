""" Views for places """
import json
import logging

from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator
from happykh.settings import HASH_IDS
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.backends import UserAuthentication

from utils import get_changed_uri
from .serializers import (PlaceSerializer, AddressSerializer,
                          CommentPlaceSerializer, PlaceRatingSerializer
                          )
from ..models import Place, Address, CommentPlace, PlaceRating

LOGGER = logging.getLogger('happy_logger')


class CustomValidationError(Exception):
    pass


class PlacePage(APIView):
    """List places or create a new one"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    variation = Place.medium

    def get(self, request):
        """
        List all places
        :param request: HTTP Request
        :return: list of all places
        """
        order = request.GET.get('order', '')
        order_by = request.GET.get('orderBy', 'name')
        places = Place.objects.order_by(f"{order}{order_by}")

        context = {
            'variation': self.variation,
            'domain': get_current_site(request)
        }
        serializer = PlaceSerializer(places, many=True, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create new place
        :param request: HTTP Request
        :return: message, status_code
        """
        data = request.POST.copy()
        address_data = json.loads(data['address'])
        data['address'] = self.get_address_pk(address_data)

        if not data['address']:
            return Response('Address serializer error',
                            status=status.HTTP_400_BAD_REQUEST)

        context = {
            'variation': self.variation,
            'domain': get_current_site(request)
        }

        serializer = PlaceSerializer(data=data, context=context)
        if serializer.is_valid():
            pk = serializer.save()
            LOGGER.info(f'Created place #{pk}')
            return Response({'message': 'place was created'},
                            status=status.HTTP_201_CREATED)

        LOGGER.error(f'Serializer errors: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_address_pk(data):
        """
        Return pk of existing or just created address
        :param data: dict consists of latitude, longitude, address string
        :return: int address primary key
        """
        address_serializer = AddressSerializer(data=data)
        if address_serializer.is_valid():
            address, _ = Address.objects.get_or_create(address=data['address'],
                                                       latitude=data[
                                                           'latitude'],
                                                       longitude=data[
                                                           'longitude'])

            return address.pk

        LOGGER.error(f'Serializer errors: {address_serializer.errors}')
        return None


class PlaceSinglePage(APIView):
    """Display and modify existing place"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    place_variation = Place.large

    def get(self, request, place_id):
        """
        :param request: HTTP Request
        :param place_id: place's id
        :return: place's data, status code
        """
        single_place = Place.get_place(place_id)

        if single_place is None:
            LOGGER.warning(f'Place #{place_id} not found')
            return Response(status=status.HTTP_404_NOT_FOUND)

        place_context = {
            'variation': self.place_variation,
            'domain': get_current_site(request)
        }
        place_serializer = PlaceSerializer(single_place, context=place_context)
        return Response(place_serializer.data, status=status.HTTP_200_OK)


class CommentsAPI(APIView):
    """Get comments for a place or create new one for place"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, place_id):
        """
        Return comments for page via paginator.
        Parameters for paginator should be in url.

        :param request: HTTP Request
        :param place_id: id of place for which comment was written
        :return: Response with data of comment and it's creator or
                 Response with error status
        """
        place = Place.get_place(place_id)
        objects_per_page = request.GET.get('objects_per_page')
        page = request.GET.get('page')

        if place is None:
            LOGGER.warning(f'Place #{place_id} not found')
            return Response(status=status.HTTP_404_NOT_FOUND)

        all_comments = CommentPlace.objects.filter(place=place_id)
        if all_comments is None or not all_comments:
            return Response(status=status.HTTP_204_NO_CONTENT)

        try:
            objects_per_page = int(objects_per_page)
            page = int(page)
            assert (page > 0)
            assert (objects_per_page > 0)
        except (TypeError, AssertionError, ValueError):
            LOGGER.warning(f'Wrong objects_per_page={objects_per_page} or '
                           f'page={page} arguments.')
            return Response(status=status.HTTP_400_BAD_REQUEST)

        paginator = Paginator(all_comments, objects_per_page)
        comments_page = paginator.get_page(page)
        comments_for_page = comments_page.object_list

        comment_context = {'domain': get_current_site(request), }
        comment_serializer = CommentPlaceSerializer(comments_for_page,
                                                    context=comment_context,
                                                    many=True, )
        next_page_link = None
        if comments_page.has_next():
            next_page_link = get_changed_uri(
                request,
                'page',
                comments_page.next_page_number()
            )
        previous_page_link = None
        if comments_page.has_previous():
            previous_page_link = get_changed_uri(
                request,
                'page',
                comments_page.previous_page_number()
            )
        response_dict = {
            "count": paginator.count,
            "number_of_pages": paginator.num_pages,
            "current_page_number": comments_page.number,
            "next": next_page_link,
            "previous": previous_page_link,
            "comments": comment_serializer.data,
        }

        return Response(response_dict, status=status.HTTP_200_OK)

    def post(self, request, place_id):
        """
        Creates new CommentPlace object.

        :param request: HTTP Request
        :param place_id: id of place for which comment was written
        :return: Response with status
        """
        place = Place.get_place(place_id)

        if place is None:
            LOGGER.warning(f'Place #{place_id} not found')
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        try:
            data['creator'] = HASH_IDS.decode(data['creator'])[0]
            data['place'] = place_id
            comment_serializer = CommentPlaceSerializer(data=data, )
            if comment_serializer.is_valid():
                comment_serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            raise CustomValidationError
        except (IndexError, CustomValidationError):
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PlaceRatingView(APIView):
    """
    Display and create place's rating
    """

    @staticmethod
    def get_average(place_id):
        """
        calculate average rating for place
        :param place_id: integer place_id
        :return: float average or 0 if there are not ratings for this place
        """
        ratings = PlaceRating.objects.filter(place=place_id)
        if not ratings.count():
            return 0

        amount = ratings.count()
        rating = sum([rate.rating for rate in ratings])
        average = round(rating / amount, 1)
        return average

    def get(self, request, place_id):
        """
        get average place's rating
        :param request: HTTP request
        :param place_id: integer place_id
        :return: Response with data and status
        """
        average_rating = self.get_average(place_id)
        response = {'place': place_id,
                    'rating': average_rating}
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, place_id):
        """
        create or update user's rating for place
        :param request: HTTP request
        :param place_id: integer place_id
        :return: Response with data and status
        """

        user = UserAuthentication.get_user(request.data.get('user'))

        if not user:
            return Response({'message': 'User does not exist'},
                            status=status.HTTP_400_BAD_REQUEST)

        place = Place.get_place(place_id)

        request_data = {'user': user.id,
                        'place': place_id,
                        'rating': request.data.get('rating')}

        serializer = PlaceRatingSerializer(data=request_data)

        if serializer.is_valid():
            response = {'user': HASH_IDS.encode(user.id),
                        'place': serializer.data['place'],
                        'rating': serializer.data['rating']}

            rating = {'rating': response['rating']}
            rate, _ = PlaceRating.objects.update_or_create(place=place,
                                                           user=user,
                                                           defaults=rating)

            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
