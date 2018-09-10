"""Views for app users"""
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.views import APIView
from rest_framework.response import Response
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

        from django.core.mail import send_mail
        send_mail('subject', 'message', EMAIL_HOST_USER, [email], fail_silently=False)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'status': False, 'message': "No user with such email."})

        if not user.check_password(password):
            return Response({'status': False, 'message': "Incorrect password."})

        full_name = user.get_full_name()
        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        send_mail(f'Confirm {user.email} on HappyKH',
                  f'We just needed to verify that {user.email} is your email address.'+
                  f' Just click the link below \n' +
                  f'http://127.0.0.1:8000/api/users/{uid}/{token}/',
                  EMAIL_HOST_USER,
                  [user.email])

        return Response({'status': True, 'full_name': full_name})


class UserActivation(APIView):

    def get(self, request, uid64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uid64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            return Response({'status': True})
