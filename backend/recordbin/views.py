import re
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Record,
    RecordSerializer,
    App,
    AppSerializer,
    AppToken,
    AppTokenSerializer,
)
from .filtersets import RecordFilterSet


class RecordViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """
    list:
    Return a list of records.

    create:
    Create a new record instance.
    """

    # Added Globally on `settings/base.py`
    permission_classes = (IsAuthenticated,)

    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    filterset_class = RecordFilterSet
    filter_backends = (DjangoFilterBackend,)

    def perform_create(self, serializer):
        app_token = self.request.auth
        serializer.save(app_id=app_token.app.pk)

    def get_queryset(self):
        params = self.request.query_params.copy()
        filter_kwargs = {}
        # Extend filtering to allow Filtering ?data[field]=value
        # DjangoFilterBackend allows direct attribute filtering
        for key, value in params.items():
            pat = r"data\[(\w+)\]"
            match = re.search(pat, key)
            if match:
                field = match.group(1)
                filter_kwargs[f"data__{field}"] = value

        # Authentication
        user = self.request.user  # logged in user or annon
        token = self.request.auth
        if isinstance(token, AppToken):
            # TokenAuthentication: Filter Records by AppToken__app
            app = token.app
            filter_kwargs["app"] = app
        elif isinstance(token, Token):
            user = token.user
            filter_kwargs["app__owner"] = user
        elif not token and user.is_authenticated and user.is_staff:
            # SessionAuthentication: Admin session cookie (used by api/v1/ and docs)
            # No Filters
            pass
        else:
            # Not sure who this is return nothing
            return Record.objects.none()
        return Record.objects.filter(**filter_kwargs)


class AppViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
    Return a list of Apps.
    """

    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = App.objects.all()
    serializer_class = AppSerializer

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)


class AppTokenViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
    Return a list of App Tokens.
    """

    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = AppToken.objects.all()
    serializer_class = AppTokenSerializer

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)
