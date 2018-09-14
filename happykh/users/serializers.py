from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework import exceptions


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    user_email = serializers.CharField()
    user_password = serializers.CharField()

    def validate(self, data):
        user_email = data.get('user_email', '')
        user_password = data.get('user_password', '')

        if user_email and user_password:
            user = authenticate(user_email=user_email,
                                user_password=user_password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise exceptions.ValidationError('User is deactivated')
            else:
                msg = 'Unable to login with given credentials'
                raise exceptions.ValidationError(msg)
        else:
            msg = 'Must provide user email and password'
            raise exceptions.ValidationError(msg)
        return data
