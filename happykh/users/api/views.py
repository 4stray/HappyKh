"""Views for app users"""
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User


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

        return Response({'status': True,})
