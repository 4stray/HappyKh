import json
import logging

from django.contrib.sites.shortcuts import get_current_site
from happykh.settings import HASH_IDS
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PlaceSerializer, AddressSerializer, \
    CommentPlaceSerializer
from ..models import Place, Address, CommentPlace

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
        places = Place.objects.all()
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
        try:
            address = Address.objects.get(address=data['address'],
                                          latitude=data['latitude'],
                                          longitude=data['longitude'])
        except Address.DoesNotExist:
            address_serializer = AddressSerializer(data=data)
            if address_serializer.is_valid():
                return address_serializer.save().pk
            else:
                LOGGER.error(f'Serializer errors: {address_serializer.errors}')
                return False
        return address.pk


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
        :param request: HTTP Request
        :param place_id: id of place for which comment was written
        :return: Response with data of comment and it's creator or
                 Response with error status
        """
        place = Place.get_place(place_id)

        if place is None:
            LOGGER.warning(f'Place #{place_id} not found')
            return Response(status=status.HTTP_404_NOT_FOUND)

        comment_context = {'domain': get_current_site(request), }
        comments = CommentPlace.objects.filter(place=place_id)
        comment_serializer = CommentPlaceSerializer(comments,
                                                    context=comment_context,
                                                    many=True, )

        return Response(comment_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, place_id):
        """
        :param request: HTTP Request
        :param place_id: id of place for which comment was written
        :return: Response with status
        """
        place = Place.get_place(place_id)

        if place is None:
            LOGGER.warning(f'Place #{place_id} not found')
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['creator'] = HASH_IDS.decode(data['creator'])[0]
        data['place'] = place_id
        comment_serializer = CommentPlaceSerializer(data=data, )
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
