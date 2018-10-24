"""Serializers for model Place"""

from rest_framework import serializers

from utils import UploadedImageField
from places.models import Place, Address


class AddressSerializer(serializers.ModelSerializer):
    """Full ModelSerializer for model Address"""
    class Meta:
        model = Address
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    """Full ModelSerializer for model Place"""

    logo = UploadedImageField(max_length=None)

    class Meta:
        model = Place
        fields = '__all__'

    def to_representation(self, instance):
        """Represent `address` as string """
        ret = super().to_representation(instance)
        ret['address'] = Address.objects.get(id=ret['address']).address
        return ret
