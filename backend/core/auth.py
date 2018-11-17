from rest_framework.authentication import TokenAuthentication


class TokenAuthenticationWithUrlSupport(TokenAuthentication):
    """ Set as default for all calls """

    keyword = "Token"

    def authenticate(self, request):
        token = request.query_params.get("token")
        if not token:
            return super().authenticate(request)
        return self.authenticate_credentials(token)
