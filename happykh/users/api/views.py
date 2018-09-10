"""Views for app users"""
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from users.models import User
from happykh.settings import EMAIL_HOST_USER
from .tokens import account_activation_token


class UserLogin(APIView):
    """
    List all users, or create a new snippet.
    """
    def post(self, request, format=None):
        email = request.data.get('user_email')
        password = request.data.get('user_password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'status': False, 'message': "No user with such email."})

        if not user.check_password(password):
            return Response({'status': False, 'message': "Incorrect password."})

        full_name = user.get_full_name()
        return Response({'status': True, 'full_name': full_name})


def send_email_confirmation(user):
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

    def get(self, request, user_id, token):
        try:
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            return Response({'status': True})
