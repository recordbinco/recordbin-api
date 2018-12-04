# # https://pytest-django.readthedocs.io/en/latest/helpers.html#client-django-test-client
import pytest
from rest_framework.test import APIClient

from rest_framework.authtoken.models import Token
from backend.recordbin.models import AppToken


@pytest.mark.django_db
@pytest.fixture
def user_token(client, ADMIN_CREDENTIALS):
    token, _ = Token.objects.get_or_create(**ADMIN_CREDENTIALS)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    return client


@pytest.mark.django_db
@pytest.fixture
def authenticated_client(client):
    token = AppToken.objects.first()
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    return client


@pytest.mark.django_db
def test_api_view_unauthorized(client):
    response = client.get("/api/v1/")
    assert response.status_code == 403


