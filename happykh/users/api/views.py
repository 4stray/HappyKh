"""Views for app users"""
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .tokens import account_activation_token
from users.models import User
from happykh.settings import EMAIL_HOST_USER


class UserLogin(APIView):
    """
    List all users, or create a new snippet.
    """

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """

        :param request: HttpRequest
        :param format:
        :return: Response({status, message})
        """
        if 'user_token' in request.data:
            pass
        else:
            print(request.user)
            email = request.data.get('user_email')
            password = request.data.get('user_password')

            try:
                validate_email(email)
            except ValidationError:
                return Response(data={'status': False,
                                      'message': 'Invalid user credentials.'})

            user = authenticate(request, user_email=email,
                                user_password=password)

            if not user:
                return Response({'status': False,
                                 'message': 'Invalid user credentials'})

            login(request, user)

            return Response({'status': True})


class UserRegistration(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        """
        Authenticates and logs the user in (login is not working)
        :param request: http request
        :return: Response({status, message})
        """
        email = request.data['user_email']
        password = request.data['user_password']

        try:
            user = User.objects.get(email=email)
            return Response({'status': False,
                             'message': 'User with such an email'
                                        'already exist'})
        except User.DoesNotExist:
            user = authenticate(request, user_email=email,
                                user_password=password)

            if self.send_email_confirmation(user):
                return Response({'status': True})
            else:
                return Response({'status': False,
                                 'message': 'The mail has not been delivered'
                                            ' due to connection reasons'})

    def send_email_confirmation(self, user):
        """
        Sends an email on user.email mailbox
        :param user: User
        :return: Boolean
        """
        try:
            token = account_activation_token.make_token(user)
            user_id = user.pk
            send_mail(f'Confirm {user.email} on HappyKH',
                      f'We just needed to verify that {user.email} '
                      f'is your email address.' +
                      f' Just click the link below \n' +
                      f'http://127.0.0.1:8080/#/confirm_registration/'
                      f'{user_id}/{token}/',
                      EMAIL_HOST_USER,
                      [user.email])
            return True
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return False


class UserActivation(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, user_id, token):
        """
        Processes GET request from user activation page
        :param request: HttpRequest
        :param user_id: Integer
        :param token: String
        :return: Response({status, message})
        """

        try:
            user = User.objects.get(pk=user_id)
            user_token, created = Token.objects.get_or_create(user=user)

            if user.is_active:
                return Response({'status': False,
                                 'message': "User is already activated"})
            elif account_activation_token.check_token(user, token) \
                    and created:
                user.is_active = True
                user.save()

                login(request, user,
                      backend='users.backends.UserAuthentication')

                return Response({'status': True,
                                 'user_token': user_token.key})
            else:
                return Response({'status': False,
                                 'message': 'User already exists'})
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist) as Error:
            return Response({'status': False,
                             'message': str(Error)})
