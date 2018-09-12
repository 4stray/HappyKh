from rest_framework import exceptions
from rest_framework import authentication
from rest_framework.authtoken.models import Token
from users.models import User


class UserAuthentication:
    def authenticate(self, request, user_email=None,
                     user_password=None, user_token=None):
        """
        User credentials are being processed on the valid format.
        If User credentials are valid then will be returned User instance.
        If No then None.
        :param request: HttpRequest
        :param user_email: String
        :param user_password: String
        :param user_token: String
        :return: User object or None
        """
        if user_token:
            pass
        else:
            try:
                user = User.objects.get(email=user_email)
                if user.check_password(user_password):
                    return user
            except User.DoesNotExist:
                user = User.objects.create_user(email=user_email,
                                                password=user_password,
                                                is_active=False)
                return user
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
