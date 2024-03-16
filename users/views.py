from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import UserCreateSerializer, AuthTokenSerializer
from users.authentication import BearerTokenAuthentication


class CreateUserView(generics.CreateAPIView):
    """
    Create New User Api View
    """

    serializer_class = UserCreateSerializer


class CreateAuthTokenView(ObtainAuthToken):
    """Create Auth Token for Users"""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class LogoutView(generics.DestroyAPIView):
    """
    API endpoint to logout the authenticated user.
    """

    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
