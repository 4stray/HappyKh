"""Serializers for app users"""
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Standard serializer for model User"""
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'age', 'gender', 'profile_image')
