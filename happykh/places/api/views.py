import logging
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import PlaceSerializer
from ..models import Place
from users.models import User
from users.api.serializers import UserSerializer

LOGGER = logging.getLogger('happy_logger')


class PlacePage(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    variation = Place.medium

    def get(self, request):
        places = Place.objects.all()
        context = {
            'variation': self.variation,
            'domain': get_current_site(request)
        }
        serializer = PlaceSerializer(places, many=True, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        context = {
            'variation': self.variation,
            'domain': get_current_site(request)
        }
        serializer = PlaceSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'place was created'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlaceSinglePage(APIView):
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
            return Response(status=status.HTTP_404_NOT_FOUND)

        place_context = {
            'variation': self.place_variation,
            'domain': get_current_site(request)
        }
        place_serializer = PlaceSerializer(single_place, context=place_context)
        return Response(place_serializer.data, status=status.HTTP_200_OK)


