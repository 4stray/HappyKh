"""Serializers for model Place"""

from rest_framework import serializers

from utils import Base64ImageField
from places.models import Place


class PlaceSerializer(serializers.ModelSerializer):
    """Full ModelSerializer for model Place"""

    logo = Base64ImageField(
        max_length=None,
        use_url=True,
        required=False,
    )

    class Meta:
        model = Place
        fields = '__all__'
