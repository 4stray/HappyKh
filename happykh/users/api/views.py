"""Views for app users"""
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import exceptions
from users.models import User
from happykh.settings import EMAIL_HOST_USER
from users.serializers import LoginSerializer
from .tokens import account_activation_token


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Logs User in
        :param request: HttpRequest
        :return: token
        """
        serializer = LoginSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.ValidationError:
            return Response({'message': 'Invalid User Credentials'},
                            status=400)

        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key} , status=200)

    def get(self, request):
        return Response({'user': str(request.user)})


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        logout(request)
        return Response(status=204)


class UserRegistration(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        """
        If user credentials are valid then creates deactivated User
        :param request: http request
        :return: Response({status, message})
        """
        email = request.data['user_email']
        password = request.data['user_password']

        try:
            user = User.objects.get(email=email)
            return Response({'message': 'User with such an email'
                                        ' already exist'},
                            status=400)
        except User.DoesNotExist:
            user = authenticate(request, user_email=email,
                                user_password=password)

            if self.send_email_confirmation(user):
                return Response(status=201)
            else:
                return Response({'message': 'The mail has not been delivered'
                                            ' due to connection reasons'},
                                status=500)

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
        Processes POST request from user activation page
        :param request: HttpRequest
        :param user_id: Integer
        :param token: String
        :return: Response({status, message})
        """

        try:
            user = User.objects.get(pk=user_id)
            user_token, created = Token.objects.get_or_create(user=user)

            if user.is_active:
                return Response({'message': "User is already activated"},
                                status=400)
            elif account_activation_token.check_token(user, token) \
                    and created:
                user.is_active = True
                user.save()

                login(request, user,
                      backend='users.backends.UserAuthentication')

                return Response({'user_token': user_token.key}, status=201)
            else:
                return Response({'message': 'User already exists'},
                                status=400)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist) as Error:
            return Response({'message': str(Error)}, status=500)
