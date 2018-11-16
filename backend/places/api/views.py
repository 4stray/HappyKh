""" Views for places """
import json
import logging

from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.backends import UserAuthentication

from utils import get_changed_uri
from .serializers import (PlaceSerializer, AddressSerializer,
                          CommentPlaceSerializer, PlaceRatingSerializer)
from ..models import Place, Address, CommentPlace, PlaceRating

LOGGER = logging.getLogger('happy_logger')


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
        data = request.data.copy()
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
            address, _ = Address.objects.get_or_create(**data)
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

        single_place = get_object_or_404(Place, pk=place_id)
        place_context = {
            'variation': self.place_variation,
            'domain': get_current_site(request)
        }
        place_serializer = PlaceSerializer(single_place, context=place_context)
        return Response(place_serializer.data, status=status.HTTP_200_OK)

    def put(self, request, place_id):
        """
        Updates place by the given id
        :param request: HTTP Request
        :param place_id: place's id
        :return: status code
        """
        single_place = get_object_or_404(Place, pk=place_id)
        request_data = request.data.copy()
        address_data = json.loads(request_data.get('address'))
        request_data['address'] = PlacePage.get_address_pk(data=address_data)

        place_serializer = PlaceSerializer(data=request_data)

        if not single_place:
            LOGGER.error(f'Place with id {place_id} does not exist')
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not place_serializer.is_valid():
            LOGGER.error(
                f'Place is not valid due to validation errors: '
                f'{place_serializer.errors}'
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)

        LOGGER.info(f'Place with id {place_id} was successfully updated')

        place_serializer.update(
            single_place,
            place_serializer.validated_data
        )
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, place_id):
        """
        Deletes place by the given id
        :param request: HTTP request
        :param place_id: place's id
        :return: status code
        """
        try:
            single_place = Place.objects.get(id=place_id)
            single_place.delete()

            LOGGER.info(f'Place with id {place_id} was deleted')

            return Response(status=status.HTTP_200_OK)
        except Place.DoesNotExist:
            LOGGER.info(f'Place with id {place_id} was not deleted')

            return Response(status=status.HTTP_404_NOT_FOUND)


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

        get_object_or_404(Place, pk=place_id)
        objects_per_page = request.GET.get('objects_per_page', '')
        page = request.GET.get('page', '')

        all_comments = CommentPlace.objects.filter(
            place=place_id).order_by('-creation_time')

        if not all_comments:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not objects_per_page.isdigit():
            LOGGER.warning(f'Wrong objects_per_page={objects_per_page}'
                           f' argument.')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if int(objects_per_page) == 0:
            LOGGER.warning(f"Objects_per_page argument can't be 0")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not page.isdigit():
            LOGGER.warning(f'Wrong page={page} argument.')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if int(page) == 0:
            LOGGER.warning(f"Page argument can't be 0")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        paginator = Paginator(all_comments, int(objects_per_page))
        comments_page = paginator.get_page(int(page))
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
        place = get_object_or_404(Place, pk=place_id)
        data = request.data.copy()
        user = UserAuthentication.get_user(request.data.get('creator'))

        data['creator'] = user.id
        data['place'] = place.id
        comment_context = {'domain': get_current_site(request), }
        comment_serializer = CommentPlaceSerializer(data=data,
                                                    context=comment_context)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data,
                            status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class SingleCommentAPI(APIView):

    def put(self, request, place_id, comment_id):
        """
        Update CommentPlace object.

        :param request: HTTP Request
        :param place_id: id of place for which comment was written
        :param comment_id id of comment being updated
        :return: Response with status
        """
        data = request.data.copy()
        data.update(creator=settings.HASH_IDS.decode(data['creator'])[0])
        data.update(place=place_id)

        comment = CommentPlace.objects.filter(pk=comment_id).first()
        if not comment:
            LOGGER.warning(f'Comment #{comment_id} not found')
            return Response(status=status.HTTP_404_NOT_FOUND)

        comment_context = {'domain': get_current_site(request)}
        data.update(edited=True)
        comment_serializer = CommentPlaceSerializer(comment,
                                                    data=data,
                                                    context=comment_context)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_200_OK)

        LOGGER.warning(
            f'Comment serialization errors {comment_serializer.errors}')
        return Response(comment_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, place_id, comment_id):
        """
        Delete CommentPlace object.

        :param request: HTTP Request
        :param comment_id if of comment being delete
        :return: Response with status
        """
        try:
            CommentPlace.objects.get(pk=comment_id).delete()
            return Response(status=status.HTTP_200_OK)
        except CommentPlace.DoesNotExist:
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
        user_id = request.data.get('user')
        if not user_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = UserAuthentication.get_user(user_id)

        request_data = {'user': user.id,
                        'place': place_id,
                        'rating': request.data.get('rating')}
        serializer = PlaceRatingSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            response = {'user': request.data.get('user'),
                        'place': serializer.data['place'],
                        'rating': serializer.data['rating']}

            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
