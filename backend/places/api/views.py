""" Views for places """
import json
import logging
from smtplib import SMTPException

from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import get_user_model

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import (ParseError, ValidationError)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.backends import UserAuthentication
from utils import (get_changed_uri, get_token_user)
from .serializers import (PlaceSerializer, AddressSerializer,
                          CommentPlaceSerializer, PlaceRatingSerializer)
from ..models import (Place, Address, CommentPlace, PlaceRating)

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

        search_option = request.GET.get('s')
        if search_option is not None:
            places = places.filter(name__icontains=search_option)

        objects_limit = request.GET.get('lim', 15)

        try:
            objects_limit = int(objects_limit)
            if objects_limit < 1:
                objects_limit = 1
        except ValueError:
            objects_limit = 15

        paginator = Paginator(places, objects_limit)

        page = request.GET.get('p', 1)

        places = paginator.get_page(page)

        serializer = PlaceSerializer(places, many=True, context=context)

        response = {"places": serializer.data,
                    "pages": paginator.num_pages,
                    "current_page": places.number,
                    "objects_limit": objects_limit,
                    "total_number": paginator.count}

        return Response(response,
                        status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create new place
        :param request: HTTP Request
        :return: message, status_code
        """
        place_data = PlacePage.parse_place_address(request.data.copy())
        context = {
            'variation': self.variation,
            'domain': get_current_site(request)
        }

        serializer = PlaceSerializer(data=place_data, context=context)
        if not serializer.is_valid():
            LOGGER.error(f'PlaceSerializer errors: {serializer.errors}')
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        pk = serializer.save()
        LOGGER.info(f'Created place #{pk}')
        return Response({'message': 'place was created'},
                        status=status.HTTP_201_CREATED)

    @staticmethod
    def get_address_pk(data):
        """
        Return pk of existing or just created address
        :param data: dict consists of latitude, longitude, address string
        :return: int address primary key
        """
        address_serializer = AddressSerializer(data=data)

        if not address_serializer.is_valid():
            LOGGER.error(f'Serializer errors: {address_serializer.errors}')
            raise ValidationError(detail=address_serializer.errors)

        address, _ = Address.objects.get_or_create(**data)
        return address.pk

    @classmethod
    def parse_place_address(cls, place_data):
        """
        Parses place address from JSON to native Python type
        :param place_data: dict
        :return: dict
        """
        try:
            address_data = json.loads(place_data.get('address'))
        except json.decoder.JSONDecodeError:
            parsing_address_error = {
                'message': 'Parsing address from Json failed',
            }

            LOGGER.error(parsing_address_error['message'])
            raise ParseError(detail=parsing_address_error['message'])

        place_data['address'] = cls.get_address_pk(address_data)
        return place_data


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
        :param place_id: Integer
        :return: HTTP Response
        """
        user = get_token_user(request)
        single_place = get_object_or_404(Place, pk=place_id)
        place_data = PlacePage.parse_place_address(request.data.copy())

        if not single_place.is_editing_permitted(user.id):
            access_denied = {
                'message': f'Editing place permission denied for the user '
                           f'with id {user.id}'
            }
            LOGGER.error(access_denied['message'])
            return Response(data=access_denied,
                            status=status.HTTP_403_FORBIDDEN)

        place_serializer = PlaceSerializer(data=place_data)
        if not place_serializer.is_valid():
            LOGGER.error(
                f'Place is not valid due to validation errors: '
                f'{place_serializer.errors}'
            )
            return Response(data=place_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        place_serializer.update(single_place, place_serializer.validated_data)
        LOGGER.info(f'Place with id {place_id} was successfully updated')
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, place_id):
        """
        Deletes place by the given id
        :param request: HTTP request
        :param place_id: Integer
        :return: HTTP Response
        """
        user = get_token_user(request)
        single_place = get_object_or_404(Place, pk=place_id)

        if not single_place.is_editing_permitted(user.id):
            access_denied = {
                'message': f'Deleting place permission denied for the user '
                           f'with id {user.id}'
            }
            LOGGER.info(access_denied['message'])
            return Response(data=access_denied,
                            status=status.HTTP_403_FORBIDDEN)

        single_place.delete()
        LOGGER.info(f'Place with id {place_id} was deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlacesEditingPermission(APIView):
    """Get place editing privilege"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, place_id):
        """
        Returns True if the user has privilege to edit the place
        :param request: HTTP Request
        :param place_id: Integer
        :return: HTTP Response
        """
        user = get_token_user(request)
        single_place = get_object_or_404(Place, pk=place_id)

        return Response(
            data={
                'is_place_editing_permitted':
                    single_place.is_editing_permitted(user.id)
            },
            status=status.HTTP_200_OK
        )

    def post(self, request, place_id):
        """
        Sends an email with place editing request
        :param place_id: Integer
        :return: HTTP Response
        """
        requesting_user = get_token_user(request)
        sender = requesting_user.email
        receivers = PlacesEditingPermission.get_staff_users()
        subject = f'User {sender} requesting place editing permission'
        message = (f'User {sender} requesting editing permission for the place'
                   'with id of {place_id} ')

        try:
            send_mail(subject, message, sender, receivers)
        except SMTPException:
            smtp_error = {'message': 'Error occurred while sending mail'}
            return Response(data=smtp_error,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        LOGGER.info(f'Place editing permission access mail has been sent')
        return Response(status=status.HTTP_201_CREATED)

    @staticmethod
    def get_staff_users():
        """ Returns all staff users for requesting of place edit"""
        User = get_user_model()
        return list(
            User.objects.filter(is_staff=True).values_list('email', flat=True)
        )


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

        objects_per_page = int(objects_per_page)
        if objects_per_page == 0:
            LOGGER.warning(f"Objects_per_page argument can't be 0")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not page.isdigit():
            LOGGER.warning(f'Wrong page={page} argument.')
            return Response(status=status.HTTP_400_BAD_REQUEST)

        page = int(page)
        if page == 0:
            LOGGER.warning(f"Page argument can't be 0")
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
            page_number = comments_page.next_page_number()
            next_page_link = get_changed_uri(request, 'page', page_number)

        previous_page_link = None
        if comments_page.has_previous():
            page_number = comments_page.previous_page_number()
            previous_page_link = get_changed_uri(request, 'page', page_number)

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
        if not comment_serializer.is_valid():
            LOGGER.warning(
                f'Comment serialization errors {comment_serializer.errors}'
            )
            return Response(comment_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        comment_serializer.save()
        return Response(comment_serializer.data, status=status.HTTP_201_CREATED)


class SingleCommentAPI(APIView):
    """Update or delete comment for a place"""

    def put(self, request, place_id, comment_id):
        """
        Update CommentPlace object.

        :param request: HTTP Request
        :param place_id: id of place for which comment was written
        :param comment_id id of comment being updated
        :return: Response with status
        """
        data = request.data.copy()
        user = UserAuthentication.get_user(request.data.get('creator'))
        data.update({'creator': user.id, 'place': place_id})

        comment = CommentPlace.objects.filter(pk=comment_id).first()
        if not comment:
            LOGGER.warning(f'Comment #{comment_id} not found')
            return Response(status=status.HTTP_404_NOT_FOUND)

        if user != comment.creator:
            return Response(status=status.HTTP_403_FORBIDDEN)

        comment_context = {'domain': get_current_site(request)}
        data.update(edited=True)
        comment_serializer = CommentPlaceSerializer(comment,
                                                    data=data,
                                                    context=comment_context)
        if not comment_serializer.is_valid():
            LOGGER.warning(
                f'Comment serialization errors {comment_serializer.errors}'
            )
            return Response(comment_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        comment_serializer.save()
        return Response(comment_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, place_id, comment_id):
        """
        Delete CommentPlace object.

        :param request: HTTP Request
        :param comment_id if of comment being delete
        :return: Response with status
        """

        user = get_token_user(request)
        comment = get_object_or_404(CommentPlace, pk=comment_id)
        if comment.creator != user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response(status=status.HTTP_200_OK)


class PlaceRatingView(APIView):
    """
    Display and create place's rating
    """

    @staticmethod
    def get_user_rating(user_id, place_id):
        """
        return user's rating for the place
        :param user_id: integer user_id
        :param place_id: integer place_id
        :return: float user_rating or 0 if rating doesn't exist
        """
        try:
            user_rating = PlaceRating.objects.get(user=user_id, place=place_id)
            return user_rating.rating
        except PlaceRating.DoesNotExist:
            return 0

    def get(self, request, place_id):
        """
        get average place's rating
        :param request: HTTP request
        :param place_id: integer place_id
        :return: Response with data and status
        """
        user_id = get_token_user(request)
        user_rating = self.get_user_rating(user_id, place_id)
        place = get_object_or_404(Place, id=place_id)

        response = {'place': place_id,
                    'data': place.average_rating,
                    'amount': place.rating_amount,
                    'rating': user_rating}
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
        if not serializer.is_valid():
            LOGGER.warning(f'Comment serialization errors {serializer.errors}')
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        response = {'user': request.data.get('user'),
                    'place': serializer.data['place'],
                    'rating': serializer.data['rating']}
        return Response(response, status=status.HTTP_200_OK)
