from rest_framework import serializers

from utils import Base64ImageField
from ..models import Place


class PlaceSerializer(serializers.ModelSerializer):
    logo = Base64ImageField(
        max_length=None,
        use_url=True,
    )

    class Meta:
        model = Place
        fields = '__all__'
