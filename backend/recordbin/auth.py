from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from .models import SourceToken

# TODO REPLACE
# https://github.com/davesque/django-rest-framework-simplejwt

class TokenAuthenticationWithUrlSupport(TokenAuthentication):
    """ Set as default for all calls """

    keyword = "Token"
    model = SourceToken

    def authenticate(self, request):
        """ Override TokenAuthentication.authenticate to support url query param"""
        token = request.query_params.get("token")
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

