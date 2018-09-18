import logging
from users.models import User

logger = logging.getLogger('happy_logger')


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
        try:
            user = User.objects.get(email=user_email)
            if user.check_password(user_password):
                logger.info('User authenticated')
                return user
        except User.DoesNotExist:
            logger.error('User does not exists while authentication')
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
