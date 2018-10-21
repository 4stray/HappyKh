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
    user_variation = User.thumbnail

    def get(self, request, id):

        try:
            single_place = Place.objects.get(pk=id)

        except Place.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            place_context = {
                'variation': self.place_variation,
                'domain': get_current_site(request)
            }
            place_serializer = PlaceSerializer(single_place, context=place_context)
            try:
                place_owner = User.objects.get(pk=place_serializer.data.get('user'))
            except User.DoesNotExist:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                user_context = {
                    'variation': self.user_variation,
                    'domain': get_current_site(request)
                }
                user_serializer = UserSerializer(place_owner, context=user_context)
                result = {
                    "place": place_serializer.data,
                    "user_name": place_owner.get_full_name(),
                    "image": user_serializer.data['profile_image']
                }
                LOGGER.info(f'Requested place with id: {id}')
                return Response(result, status=status.HTTP_200_OK)

