"""Serializers for model Place"""

from places.models import Place, Address, CommentPlace, PlaceRating
from rest_framework import serializers
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
        """Represent `address` as string """
        ret = super().to_representation(instance)
        ret['address'] = Address.objects.get(id=ret['address']).address
        return ret


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
