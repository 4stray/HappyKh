"""Views for app users"""
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User
from users.serializers import UserSerializer


class UserLogin(APIView):
    """
    List all users, or create a new snippet.
    """

    def post(self, request, format=None):
        email = request.data.get('user_email')
        password = request.data.get('user_password')

        try:
            validate_email(email)
        except ValidationError:
            return Response({'status': False, 'message': "Invalid email data."})

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'status': False, 'message': "No user with such email."})

        if not user.check_password(password):
            return Response({'status': False, 'message': "Incorrect password."})

        return Response({'status': True, })


class UserProfile(APIView):
    """

    """

    def get_profile(self, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'status': False, 'message': "No user with such id."})
        return user

    def get(self, request, id, format=None):
        pk = id
        user = self.get_profile(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, id, format=None):
        pk = id
        user = self.get_profile(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save(id=id, **serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors)




