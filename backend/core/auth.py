from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import exceptions

from backend.recordbin.models import SourceToken


class UserTokenAuthentication(TokenAuthentication):
    keyword = "Token"
    model = Token


class SourceTokennAuthentication(TokenAuthentication):
    """
    Similar to Token, but users SourceToken as model (belongs to Source not users)
    and accepts url param token
    """

    keyword = "SourceToken"
    model = SourceToken

    def authenticate(self, request):
        """ Override TokenAuthentication.authenticate to support url query param"""
        token = request.query_params.get("source")
        if token:
            return self.authenticate_credentials(token)
        return super().authenticate(request)

    def authenticate_credentials(self, key):
        """ Override TokenAuthentication.authenticate to support url query param"""
        model = SourceToken
        try:
            token = model.objects.get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid token.")

        if not token.source.owner.is_active:
            raise exceptions.AuthenticationFailed("User inactive or deleted.")

        return (token.source.owner, token)

