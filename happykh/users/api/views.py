"""Views for app users"""
import logging
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import exceptions
from users.models import User
from users.serializers import LoginSerializer, UserSerializer, PasswordSerializer
from happykh.settings import EMAIL_HOST_USER
from .tokens import account_activation_token

logger = logging.getLogger('happy_logger')


class UserLogin(APIView):
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
            logger.error(f'ValidationError {error.detail["non_field_errors"]}')
            return Response({
                'message': error.detail["non_field_errors"]
            }, status=400)

        user = serializer.validated_data['user']

        if user.is_active:
            user_token, created = Token.objects.get_or_create(user=user)
            logger.info('User has been logged in')
            return Response({
                'user_token': user_token.key,
                'user_id': user.id,
            }, status=200)
        else:
            logger.warning(f'Login by unregistered user')
            return Response({
                'message': 'You have to register first'
            }, status=400)


class UserLogout(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        Token.objects.get(key=request.data['user_token']).delete()
        logger.info('User has been logged out')
        return Response({'message': 'User has been logged out'}, status=201)


class UserRegistration(APIView):
    permission_classes = (AllowAny, )

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
            logger.error(f'Email validation error "{error.message}"')
            return Response({
                'message': 'Invalid email format'
            }, status=400)

        try:
            User.objects.get(email=user_email)
            logger.warning('User with such an email already exists')
            return Response({
                'message': 'User with such an email already exists'
            }, status=400)
        except User.DoesNotExist:
            user = User.objects.create_user(email=user_email,
                                            password=user_password,
                                            is_active=False)

            if self.send_email_confirmation(user):
                return Response({
                    'message': 'Mail has been sent'
                }, status=201)
            else:
                logger.error('Confirmation email has not delivered')
                return Response({
                    'message': 'The mail has not been delivered'
                    ' due to connection reasons'
                }, status=500)

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
                      f'is your email address.' +
                      f' Just click the link below \n' +
                      f'http://127.0.0.1:8080/#/confirm_registration/'
                      f'{user_id}/{email_token}/',
                      EMAIL_HOST_USER,
                      [user.email])
            logger.info('Confirmation mail has been sent')
            return True
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as error:
            logger.error(f'Send email error {error}')
            return False


class UserActivation(APIView):
    permission_classes = (AllowAny, )

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
                logger.warning('Activate already activated user')
                return Response({
                    'message': "User is already exists and activated"
                }, status=400)
            elif account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                logger.info('User`s account has been activated')
                return Response({
                    'message': "User's account has been activated"
                }, status=201)
            else:
                logger.error('User activation with invalid token')
                return Response({
                    'message': 'Invalid token'
                }, status=400)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist) as error:
            logger.error(f'Error {error} while user activation')
            return Response({'message': str(error)}, status=500)


class UserProfile(APIView):
    """
    Get user's data, update data or change password.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_profile(self, pk):
        """
        Check if user exists.
        :param pk: Integer
        :return: User
        """
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            logger.error('Can`t get user profile because of invalid id')
            return Response({'message': "No user with such id."}, status=500)

        return user

    def get(self, request, id):
        """
        Return user's data.
        :param request: HTTP request
        :param id: Integer
        :return: Response(data, status)
        """
        user = self.get_profile(id)
        serializer = UserSerializer(user)

        logger.info('Return user profile')
        return Response(serializer.data, status=200)

    def patch(self, request, id):
        """
        Update user's data
        :param request: HTTP request
        :param id: Integer
        :return: Response(data, status)
        """
        user = self.get_profile(id)

        if 'old_password' in self.request.data:
            """
            Change password
            """
            serializer = PasswordSerializer(data=request.data)

            if serializer.is_valid():
                if not user.check_password(serializer.data.get('old_password')):
                    logger.error('Received wrong old password while changing password')
                    return Response({'message': 'Wrong password.'}, status=400)

                if not serializer.data.get('new_password1') == serializer.data.get('new_password2'):
                    logger.error('Passwords don`t match while changing password')
                    return Response({'message': "Passwords don't match."}, status=400)

                serializer.update(user, serializer.data)
                logger.info('Updated user password')
                return Response({'message': 'Password was updated.'}, status=200)

            logger.critical(f'Serializer error {serializer.errors} while changing password')
            return Response(serializer.errors, status=500)

        else:
            """
            Update data
            """
            serializer = UserSerializer(user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save(id=id, **serializer.validated_data)

            logger.info('User data updated')
            return Response(serializer.data, status=200)
