"""Serializers for model Place"""

from rest_framework import serializers
from places.models import Place
from users.backends import UserHashedIdField
from utils import UploadedImageField


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
