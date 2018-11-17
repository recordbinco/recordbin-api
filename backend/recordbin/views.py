from rest_framework import viewsets
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
import re

from rest_framework.response import Response
from rest_framework import status

# Add Auth
# https://www.django-rest-framework.org/api-guide/authentication/#setting-the-authentication-scheme
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Record, RecordSerializer
from .filtersets import RecordFilterSet


class RecordViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    list:
    Return a list of records.

    create:
    Create a new record instance.
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    filterset_class = RecordFilterSet
    filter_backends = (DjangoFilterBackend,)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.auth.user.id)

    # def create(self, request):
    #     user = request.auth.user
    #     serializer = self.serializer_class(...)
    #     data = serializer.data
    #     return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        params = self.request.query_params.copy()
        filter_kwargs = {}
        for key, value in params.items():
            pat = r"data\[(\w+)\]"
            match = re.search(pat, key)
            if match:
                field = match.group(1)
                filter_kwargs[f"data__{field}"] = value
        return Record.objects.filter(**filter_kwargs)
