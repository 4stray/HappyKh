from rest_framework import exceptions
from rest_framework import authentication
from rest_framework.authtoken.models import Token
# from .models import User
from users.models import User


class UserAuthentication:
    def authenticate(self, request, user_email=None,
                     user_password=None, user_token=None):
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
