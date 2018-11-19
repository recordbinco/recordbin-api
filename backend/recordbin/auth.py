from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from .models import SourceToken


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


# from rest_framework import parsers, renderers
# from rest_framework.authtoken.models import Token
# from rest_framework.authtoken.serializers import AuthTokenSerializer
# from rest_framework.compat import coreapi, coreschema
# from rest_framework.response import Response
# from rest_framework.schemas import ManualSchema
# from rest_framework.views import APIView


# class ObtainAuthToken(APIView):
#     throttle_classes = ()
#     permission_classes = ()
#     parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
#     renderer_classes = (renderers.JSONRenderer,)
#     serializer_class = AuthTokenSerializer
#     if coreapi is not None and coreschema is not None:
#         schema = ManualSchema(
#             fields=[
#                 coreapi.Field(
#                     name="username",
#                     required=True,
#                     location='form',
#                     schema=coreschema.String(
#                         title="Username",
#                         description="Valid username for authentication",
#                     ),
#                 ),
#                 coreapi.Field(
#                     name="password",
#                     required=True,
#                     location='form',
#                     schema=coreschema.String(
#                         title="Password",
#                         description="Valid password for authentication",
#                     ),
#                 ),
#                 coreapi.Field(
#                     name="source",
#                     required=True,
#                     location='form',
#                     schema=coreschema.String(
#                         title="Source",
#                         description="Name of a Record Source",
#                     ),
#                 ),
#             ],
#             encoding="application/json",
#         )

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key})


# obtain_auth_token = ObtainAuthToken.as_view()
