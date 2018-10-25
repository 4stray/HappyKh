"""Views for app users"""
# pylint: disable = no-member, no-self-use, no-else-return, invalid-name,
# pylint: disable = unused-argument, unused-argument, logging-fstring-interpolation
import datetime
import logging
from smtplib import SMTPException

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.validators import ValidationError
from django.core.validators import validate_email
from django.utils import timezone
from rest_framework import exceptions
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
# pylint: disable = no-name-in-module, import-error
from utils import is_user_owner
from happykh.settings import EMAIL_HOST_USER
from ..backends import UserAuthentication
from .serializers import LoginSerializer
from .serializers import EmailSerializer
from .serializers import PasswordSerializer
from .serializers import UserSerializer
from .tokens import account_activation_token
from ..models import User
from ..cryptography import decode, encode

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
                f'Email: {request.data["user_email"]}'
            )
            return Response({
                'message': 'Your email or password is not valid.'
            }, status=error.status_code)

        user = serializer.validated_data['user']
        if user.is_active:
            # pylint: disable = unused-variable
            user_token, created = Token.objects.get_or_create(user=user)
            LOGGER.info('User has been logged in')
            return Response({
                'token': user_token.key,
                'user_id': user.id,
            }, status=status.HTTP_200_OK)
        else:
            LOGGER.warning('Attempt to login by unregistered user')
            return Response({
                'message': "You can't login, you have to register first."
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
        token_key = request.META['HTTP_AUTHORIZATION'][6:]
        Token.objects.get(key=token_key).delete()

        LOGGER.info('User has been logged out')

        return Response({
            'message': 'User has been logged out'
        }, status=status.HTTP_201_CREATED)


class UserRegistration(APIView):
    """ Class for registration view"""
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
        except ValidationError as error:
            LOGGER.error(
                f"Email validation error {error}, "
                f"Email: {request.data['user_email']}"
            )
            return Response({
                'message': 'Invalid email format'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=user_email)
            LOGGER.warning(
                f'User with such email already exists, user_id: {user.pk}'
            )
            return Response({
                'message': 'User with such email already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            user = User.objects.create_user(email=user_email,
                                            password=user_password,
                                            is_active=False)
            if UserActivation.send_email_confirmation(user):
                return Response(status=status.HTTP_201_CREATED)
            else:
                LOGGER.error('Confirmation email has not been delivered')
                return Response({
                    'message': 'The mail has not been delivered'
                               ' due to connection reasons'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserActivation(APIView):
    """Class for activation user account after registration"""
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Check user credentials and send new confirmation email
        :param request: http request
        :return: Response({status, message})
        """
        user_email = request.data["user_email"]
        try:
            validate_email(user_email)
        except ValidationError as error:
            LOGGER.error(
                f'ValidationError {error}, '
                f'Email: {user_email}')
            return Response({'message': 'Invalid email'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return Response({'message': 'There is no user with such email'},
                            status=status.HTTP_400_BAD_REQUEST)

        msg = 'The mail has not been delivered due to connection reasons'
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        if user.is_active:
            msg = 'User already activated'
            status_code = status.HTTP_400_BAD_REQUEST
        elif self.send_email_confirmation(user):
            msg = 'Confirmation email has been sent'
            status_code = status.HTTP_200_OK

        return Response({'message': msg}, status=status_code)

    def get(self, request, email_crypt, token):
        """
        Processes GET request from user activation page
        :param request: HttpRequest
        :param email_crypt: String
        :param token: String
        :return: Response({message}, status)
        """
        # pylint: disable=unused-argument
        try:
            email = decode(email_crypt)
            user = User.objects.get(email=email)
            if user.is_active:
                LOGGER.warning(
                    f'Activate already activated user, user_id: {user.pk}'
                )
                return Response({
                    'message': 'User is already exists and activated'
                }, status=status.HTTP_400_BAD_REQUEST)
            elif account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()

                LOGGER.info("User's account has been activated")
                return Response({
                    'message': "User's account has been activated"
                }, status=status.HTTP_201_CREATED)
            else:
                LOGGER.error(
                    f'User activation with invalid token,'
                    f' user_email: {user.email}, token: {token}'
                )
                return Response({
                    'message': 'Invalid token'
                }, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist) as error:
            LOGGER.error(f'Error {error} while user activation')
            return Response({'message': str(error)},
                            status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def send_email_confirmation(user, email=None):
        """
        Sends an email on specified user.email
        :param user: User
        :param email: target email to send confirmation
        :return: Boolean
        """
        if email is None:
            email = user.email

        try:
            email_token = account_activation_token.make_token(user)
            email_crypt = encode(email)
            send_mail(
                f'Confirm {email} on HappyKH',
                f'We just needed to verify that {email} '
                f'is your email address.'
                f' Just click the link below \n'
                f'http://127.0.0.1:8080/#/confirm_registration/'
                f'{email_crypt}/{email_token}/',
                EMAIL_HOST_USER,
                [email]
            )
            LOGGER.info('Confirmation mail has been sent')
        except SMTPException:
            LOGGER.error('Error occurred while sending mail')
            return False

        return True


class UserProfile(APIView):
    """
    Get user's data, update data or change password.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # pylint: disable = redefined-builtin
    variation = User.medium

    def get(self, request, id):
        """
        Return user's data.
        :param request: HTTP request
        :param id: Integer
        :return: Response(data, status)
        """
        user = UserAuthentication.get_user(id)

        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        context = {
            'variation': self.variation,
            'domain': get_current_site(request)
        }

        serializer = UserSerializer(user, context=context)

        response_data = serializer.data
        enable_editing_profile = is_user_owner(request, id)
        response_data['enable_editing_profile'] = enable_editing_profile

        LOGGER.info(
            f'Enable Editing User Profile is set '
            f'to {enable_editing_profile}'
        )
        LOGGER.info('Return user profile')

        return Response(response_data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        """
        Update user's data
        :param request: HTTP request
        :param id: Integer
        :return: Response(data, status)
        """
        if not is_user_owner(request, id):
            LOGGER.error(
                "User's data were not updated."
                "user_id must be equal to token user_id"
            )
            return Response({'message': 'Editing not allowed'},
                            status=status.HTTP_403_FORBIDDEN)

        user = UserAuthentication.get_user(id)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        request_data = request.data.copy()
        age = request_data.get('age')
        if age == 'null':
            request_data['age'] = None

        context = {
            'variation': self.variation,
            'domain': get_current_site(request)
        }

        serializer = UserSerializer(
            user,
            data=request_data,
            partial=True,
            context=context,
        )

        if serializer.is_valid():
            serializer.save(id=id, **serializer.validated_data)
            LOGGER.info('User data updated')
            return Response(serializer.data, status=status.HTTP_200_OK)

        LOGGER.error(
            f'Serializer error {serializer.errors} while changing data'
        )
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class UserEmail(APIView):
    """
    Gets new email for user, changes it if value is valid
    """

    # pylint: disable = redefined-builtin
    def patch(self, request, id):
        """
        Changes user email
        :param request: HTTP Request
        :param id: Integer
        :return: Response(data)
        """
        user = UserAuthentication.get_user(id)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            user = User.objects.get(email=request.data.get('email'))

            LOGGER.warning(f'User with id: {id} tried to change '
                           f'his email to existing')

            return Response({'message': 'User with such email already exists'},
                            status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            serializer = EmailSerializer(user, request.data)

            if serializer.is_valid():
                valid_mail = serializer.validated_data['email']
                if UserActivation.send_email_confirmation(user, valid_mail):
                    serializer.update(user, serializer.validated_data)
                    # Send confirmation email
                    LOGGER.info(f'User with id: {id} changed his email')
                    return Response(status=status.HTTP_200_OK)
                else:
                    LOGGER.error('Confirmation email has not been delivered')
                    return Response({
                        'message': 'The mail has not been delivered'
                                   ' due to connection reasons'
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class UserPassword(APIView):
    """
    Change user's password
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def patch(self, request, id):
        """
        :param request: HTTP request
        :param id: integer
        :return: Response(message, status)
        """
        user = UserAuthentication.get_user(id)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(
                    serializer.data.get('old_password')):
                LOGGER.error(
                    'Received wrong old password while changing password'
                )
                return Response({'message': 'Wrong password.'},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer.update(user, serializer.data)
            LOGGER.info('Updated user password')
            return Response({'message': 'Password was updated.'},
                            status=status.HTTP_200_OK)

        LOGGER.error(
            f'Serializer error {serializer.errors} while changing password'
        )
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class TokenValidation(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        token_key = request.META['HTTP_AUTHORIZATION'][6:]
        try:
            token = Token.objects.get(key=token_key)

            if (timezone.now() <= token.created
                    + datetime.timedelta(days=1)):
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Token.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
