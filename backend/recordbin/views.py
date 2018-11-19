import re
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Record,
    RecordSerializer,
    Source,
    SourceSerializer,
    SourceToken,
    SourceTokenSerializer,
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
    # authentication_classes = (TokenAuthenticationWithUrlSupport,)
    # permission_classes = (IsAuthenticated,)

    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    filterset_class = RecordFilterSet
    filter_backends = (DjangoFilterBackend,)

    def perform_create(self, serializer):
        token = self.request.auth
        serializer.save(source_id=token.source.pk)

    def get_queryset(self):
        params = self.request.query_params.copy()
        filter_kwargs = {}
        for key, value in params.items():
            pat = r"data\[(\w+)\]"
            match = re.search(pat, key)
            if match:
                field = match.group(1)
                filter_kwargs[f"data__{field}"] = value
        token = self.request.auth
        if token:
            source = token.source
            filter_kwargs["source"] = source
        elif not token and self.request.user.is_authenticated:
            # Session Authenticatio from API View, no Token
            filter_kwargs["source__owner"] = self.request.user
        else:
            return Record.objects.none()
        return Record.objects.filter(**filter_kwargs)


class SourceViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
    Return a list of Record Sources.
    """

    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)


class SourceTokenViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
    Return a list of Record Source Tokens.
    """

    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = SourceToken.objects.all()
    serializer_class = SourceTokenSerializer

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)
