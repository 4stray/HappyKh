"""Views for app users"""
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User
from users.serializers import UserSerializer
from users.serializers import PasswordSerializer


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
    Get user's data, update data or change password.
    """

    def get_profile(self, pk):
        """
        Check if user exists.
        :param pk: Integer
        :return: User
        """

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'message': "No user with such id."}, status=500)

        return user

    def get(self, request, id, format=None):
        """
        Return user's data.
        :param request: HTTP request
        :param id: Integer
        :return: Response(data, status)
        """
        user = self.get_profile(id)
        serializer = UserSerializer(user)

        return Response(serializer.data, status=200)

    def patch(self, request, id, format=None):
        """
        Update user's data
        :param request: HTTP request
        :param id: Integer
        :return: Response(data, status)
        """
        user = self.get_profile(id)

        if 'old_password' in self.request.data:
            """Change password"""
            serializer = PasswordSerializer(data=request.data)

            if serializer.is_valid():
                if not user.check_password(serializer.data.get('old_password')):
                    return Response({'message': 'Wrong password.'}, status=400)

                if not serializer.data.get('new_password1') == serializer.data.get('new_password2'):
                    return Response({'message': "Passwords don't match."}, status=400)

                serializer.update(user, serializer.data)
                return Response({'message': 'Password was updated.'}, status=200)

            return Response(serializer.errors, status=500)

        else:
            """Update data"""
            serializer = UserSerializer(user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save(id=id, **serializer.validated_data)

            return Response(serializer.data, status=200)