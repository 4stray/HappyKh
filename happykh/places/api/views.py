import json
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import AddressSerializer, PlaceSerializer
from ..models import Place, Address


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
            serializer.save()
            return Response({'message': 'place was created'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_address_pk(data):
        try:
            address = Address.objects.get(address=data['address'],
                                          latitude=data['latitude'],
                                          longitude=data['longitude'])
        except Address.DoesNotExist:
            address_serializer = AddressSerializer(data=data)
            if address_serializer.is_valid():
                return address_serializer.save().pk
            else:
                return False
        return address.pk
