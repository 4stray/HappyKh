from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from users.models import User


class UserSerializer(serializers.Serializer):
        first_name = serializers.CharField(max_length=100, required=False)
        last_name = serializers.CharField(max_length=100, required=False)
        email = serializers.EmailField(required=True)
        age = serializers.IntegerField(required=False)
        gender = serializers.ChoiceField(choices=User.GENDER_CHOICES, default='woman')
        profile_image = serializers.ImageField( required=False)
        is_active = serializers.BooleanField(default=True)
        is_staff = serializers.BooleanField(default=False)
        password = serializers.CharField(max_length=255, required=False)

        def create(self, validated_data):
            password = validated_data.pop("password")
            user = User.objects.create(**validated_data)
            if password:
                user.set_password(password)
                user.save()
            return user
            # is called if we save serializer if it have an instance

        def update(self, instance, validated_data):
            password = validated_data.pop("password")
            instance.__dict__.update(validated_data)
            if password:
                instance.set_password(password)
            instance.save()
            return instance



