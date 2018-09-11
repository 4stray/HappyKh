"""Views for app users"""
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User
from users.serializers import UserSerializer
from happykh.settings import EMAIL_HOST_USER
from .tokens import account_activation_token


class UserLogin(APIView):
    """
    List all users, or create a new snippet.
    """
    def post(self, request, format=None):
        """
        Processes post request from login page
        :param request: http request
        :param format:
        :return: json - error message or user`s full_name
        """
        email = request.data.get('user_email')
        password = request.data.get('user_password')

        try:
            validate_email(email)
        except ValidationError:
            return Response({'message': "Invalid email data."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': "No user with such email."}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({'message': "Incorrect password."}, status=status.HTTP_400_BAD_REQUEST)

        full_name = user.get_full_name()
        send_email_confirmation(user)
        return Response({'full_name': full_name})


def send_email_confirmation(user):
    """
    Make and send mail for user confirmation
    """
    try:
        token = account_activation_token.make_token(user)
        user_id = user.pk
        send_mail(f'Confirm {user.email} on HappyKH',
                  f'We just needed to verify that {user.email} is your email address.' +
                  f' Just click the link below \n' +
                  f'http://127.0.0.1:8000/api/users/activate/{user_id}/{token}/',
                  EMAIL_HOST_USER,
                  [user.email])
        return True
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return False


class UserActivation(APIView):
    """
    Check token from email and activate user
    """
    def get(self, request, user_id, token):
        """
        Processes get request from user activation page
        :param request: http request
        :param user_id: user`s id
        :param token: onetime email confirmation token
        :return: json - status, message
        """
        try:
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user.is_active:
            return Response({'message': "User is already activated"})
        elif user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': "User successfully activated"})
        else:
            return Response({'message': "Activation error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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




