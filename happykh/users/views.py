from users.models import User
from rest_framework.views import APIView
from rest_framework.response import Response


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
