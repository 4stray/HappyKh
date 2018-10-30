"""Serializers for model Place"""

from rest_framework import serializers
from places.models import Place
from users.backends import UserHashedIdField
from utils import UploadedImageField


class PlaceSerializer(serializers.ModelSerializer):
    """Full ModelSerializer for model Place"""
    user = UserHashedIdField()
    logo = UploadedImageField(max_length=None, )

    class Meta:
        model = Place
        fields = '__all__'
