from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext as _


class BearerTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        auth = request.headers.get("Authorization")
        if not auth:
            return None

        parts = auth.split()
        if parts[0].lower() != self.keyword.lower() or len(parts) != 2:
            return None

        token = parts[1]
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed(_("Invalid token."))

        if not token.user.is_active:
            raise AuthenticationFailed(_("User inactive or deleted."))

        return (token.user, token)
