from rest_framework import serializers
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.password_validation import validate_password
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for accessing user's data.
    """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'age', 'gender', 'email', 'profile_image', 'is_active', 'is_staff')


class PasswordSerializer(serializers.ModelSerializer):
    """
    Serializer for password change.
    """
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

    def update(self, instance, validated_data):
        password = validated_data.pop("new_password1")
        instance.__dict__.update(validated_data)

        if password:
            instance.set_password(password)
        instance.save()

        return instance



