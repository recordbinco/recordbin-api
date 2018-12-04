from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import exceptions

from backend.recordbin.models import AppToken


class UserTokenAuthentication(TokenAuthentication):
    """ Uses rest_framework.authtoken.models.Token """
    keyword = "Token"
    model = Token


class AppTokenAuthentication(TokenAuthentication):
    """
    Similar to Token, but users AppToken as model (belongs to apps not users)
    and accepts url param token
    """

    keyword = "AppToken"
    model = AppToken

    def authenticate(self, request):
        """ Override TokenAuthentication.authenticate to support url query param"""
        token = request.query_params.get("app")
        if token:
            return self.authenticate_credentials(token)
        return super().authenticate(request)

    def authenticate_credentials(self, key):
        """ Override TokenAuthentication.authenticate to support url query param"""
        model = AppToken
        try:
            token = model.objects.get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid token.")

        if not token.app.owner.is_active:
            raise exceptions.AuthenticationFailed("User inactive or deleted.")

        return (token.app.owner, token)

