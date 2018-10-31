"""Serializers for model Place"""

from rest_framework import serializers
from users.backends import UserHashedIdField
from utils import UploadedImageField
from places.models import Place, Address


class AddressSerializer(serializers.ModelSerializer):
    """Full ModelSerializer for model Address"""

    class Meta:
        model = Address
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    """
    Full ModelSerializer for model Place.
    All data should be passed with the same keys as attributes in the model!
    """

    user = UserHashedIdField()
    logo = UploadedImageField(max_length=None, )

    class Meta:
        model = Place
        fields = '__all__'

    def create(self, validated_data):
        new_place = Place.objects.create()
        self.update(instance=new_place, validated_data=validated_data)
        return new_place

    def to_representation(self, instance):
        """Represent `address` as string """
        ret = super().to_representation(instance)
        ret['address'] = Address.objects.get(id=ret['address']).address
        return ret
