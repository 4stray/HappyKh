"""Views for app users"""
import logging
from smtplib import SMTPException

from django.core.mail import send_mail
from django.core.validators import validate_email
from rest_framework import exceptions
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from happykh.settings import EMAIL_HOST_USER
from .serializers import LoginSerializer
from .serializers import PasswordSerializer
from .serializers import UserSerializer
from .tokens import account_activation_token
from ..models import User

LOGGER = logging.getLogger('happy_logger')


class UserLogin(APIView):
    """"
    Login existing user to the system
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Logs User in
        :param request: HttpRequest
        :return: Response({user_token, user_id}, status)
                 Response({message}, status)
        """
        serializer = LoginSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.ValidationError as error:
            LOGGER.error(
                f'ValidationError {error.default_detail}, '
                f'Email: {request.data["user_email"]}')
            return Response({
                'message': 'Your email or password is not valid.'
            }, status=error.status_code)

        user = serializer.validated_data["user"]
        if user.is_active:
            user_token, created = Token.objects.get_or_create(user=user)
            LOGGER.info('User has been logged in')
            return Response({
                'token': user_token.key,
                'user_id': user.id,
            }, status=status.HTTP_200_OK)
        else:
            LOGGER.warning('Attempt to login by unregistered user')
            return Response({
                'message': 'You can`t login, you have to register first.'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    """
    Performs user logout action from the system
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Deletes user's token after logout
        :param request: HttpRequest
        :return: Response({message}, status)
        """

        Token.objects.get(key=request.data['user_token']).delete()
        LOGGER.info('User has been logged out')
        return Response({'message': 'User has been logged out'},
                        status=status.HTTP_201_CREATED)


class UserRegistration(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        If user credentials are valid then creates deactivated User
        :param request: http request
        :return: Response({status, message})
        """
        user_email = request.data['user_email']
        user_password = request.data['user_password']

        try:
            validate_email(user_email)
        except exceptions.ValidationError as error:
            LOGGER.error(f"Email validation error {error.default_detail}, "
                         f"Email: {request.data['user_email']}")
            return Response({
                'message': 'Invalid email format'
            }, status=error.status_code)

        try:
            user = User.objects.get(email=user_email)
            LOGGER.warning(
                f'User with such email already exists, user_id: {user.pk}')
            return Response({
                'message': 'User with such email already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            user = User.objects.create_user(email=user_email,
                                            password=user_password,
                                            is_active=False)
            if self.send_email_confirmation(user):
                return Response(status=status.HTTP_201_CREATED)
            else:
                LOGGER.error('Confirmation email has not been delivered')
                user.delete()
                return Response({
                    'message': 'The mail has not been delivered'
                               ' due to connection reasons'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def send_email_confirmation(self, user):
        """
        Sends an email on specified user.email
        :param user: User
        :return: Boolean
        """
        try:
            email_token = account_activation_token.make_token(user)
            user_id = user.pk
            send_mail(f'Confirm {user.email} on HappyKH',
                      f'We just needed to verify that {user.email} '
                      f'is your email address.'
                      f' Just click the link below \n'
                      f'http://127.0.0.1:8080/#/confirm_registration/'
                      f'{user_id}/{email_token}/',
                      EMAIL_HOST_USER,
                      [user.email])
            LOGGER.info('Confirmation mail has been sent')
        except SMTPException:
            LOGGER.error('Error occurred while sending mail')
            return False

        return True


class UserActivation(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, user_id, token):
        """
        Processes POST request from user activation page
        :param request: HttpRequest
        :param user_id: Integer
        :param token: String
        :return: Response({message}, status)
        """
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                LOGGER.warning(
                    f'Activate already activated user, user_id: {user.pk}')
                return Response({
                    'message': 'User is already exists and activated'
                }, status=status.HTTP_400_BAD_REQUEST)
            elif account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                LOGGER.info('User`s account has been activated')
                return Response({
                    'message': "User's account has been activated"
                }, status=status.HTTP_201_CREATED)
            else:
                LOGGER.error(f'User activation with invalid token,'
                             f' user_email: {user.email}, token: {token}')
                return Response({
                    'message': 'Invalid token'
                }, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist) as error:
            LOGGER.error(f'Error {error} while user activation')
            return Response({'message': str(error)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfile(APIView):
    """
    Get user's data, update data or change password.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        """
        Return user's data.
        :param request: HTTP request
        :param id: Integer
        :return: Response(data, status)
        """
        try:
            user = User.objects.get(pk=id)
            serializer = UserSerializer(user)
            LOGGER.info('Return user profile')
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            LOGGER.error(
                'Can`t get user profile because of invalid id,'
                f' user_id: {id}')
            return Response({'message': 'No user with such id.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, id):
        """
        Update user's data
        :param request: HTTP request
        :param id: Integer
        :return: Response(data, status)
        """
        user = None
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            LOGGER.error(
                'Can`t get user profile because of invalid id,'
                ' user_id: {user.pk}')
            return Response({'message': 'No user with such id.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if 'old_password' in self.request.data:
            # Change password

            serializer = PasswordSerializer(data=request.data)

            if serializer.is_valid():
                if not user.check_password(
                        serializer.data.get('old_password')):
                    LOGGER.error(
                        'Received wrong old password while changing password')
                    return Response({'message': 'Wrong password.'},
                                    status=status.HTTP_400_BAD_REQUEST)

                serializer.update(user, serializer.data)
                LOGGER.info('Updated user password')
                return Response({'message': 'Password was updated.'},
                                status=status.HTTP_200_OK)

            LOGGER.critical(
                f'Serializer error {serializer.errors} while changing password'
            )
            return Response(serializer.errors,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            # Update data
            serializer = UserSerializer(user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save(id=id, **serializer.validated_data)
                LOGGER.info('User data updated')
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
