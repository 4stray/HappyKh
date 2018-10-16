import logging
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import PlaceSerializer
from ..models import Place

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

    variation = Place.large

    def get(self, request, id):

        try:
            single_place = Place.objects.get(pk=id)

        except Place.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            context = {
                'variation': self.variation,
                'domain': get_current_site(request)
            }
            serializer = PlaceSerializer(single_place, context=context)
            LOGGER.info(f'Requested place with id: {id}')
            return Response(serializer.data, status=status.HTTP_200_OK)

