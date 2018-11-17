"""Serializers for model Place"""
import json

from places.models import Place, Address, CommentPlace, PlaceRating
from rest_framework import serializers, exceptions
from users.api.serializers import CommentAbstractSerializer
from users.backends import UserHashedIdField

from utils import UploadedImageField


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

    def to_representation(self, instance):
        """Represent `address` as a longitude, latitude and string address"""
        ret = super().to_representation(instance)
        place_address = Address.objects.get(id=ret['address'])

        ret['address'] = {
            'longitude': place_address.longitude,
            'latitude': place_address.latitude,
            'address': place_address.address,
        }

        return ret

    def update(self, instance, validated_data):
        validated_data = dict(validated_data)
        if validated_data.get('logo') is None:
            validated_data['logo'] = instance.logo

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

class CommentPlaceSerializer(CommentAbstractSerializer):
    """
    ModelSerializer for CommentPlace model, which extends
    CommentAbstractSerializer.
    """

    class Meta:
        model = CommentPlace
        fields = '__all__'


class PlaceRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceRating
        fields = '__all__'

    def create(self, validated_data):
        rating = {'rating': validated_data.get('rating')}
        user = validated_data.get('user')
        place = validated_data.get('place')
        rate, _ = PlaceRating.objects.update_or_create(place=place,
                                                       user=user,
                                                       defaults=rating)
        return rate
