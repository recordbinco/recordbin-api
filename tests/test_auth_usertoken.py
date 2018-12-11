# # https://pytest-django.readthedocs.io/en/latest/helpers.html#client-django-test-client
import pytest
from rest_framework.test import APIClient

from rest_framework.authtoken.models import Token as UserToken
from backend.recordbin.models import AppToken


@pytest.mark.django_db
@pytest.fixture
def client_usertoken(client, ADMIN_CREDENTIALS):
    email = ADMIN_CREDENTIALS["email"]
    token, _ = UserToken.objects.get_or_create(user__email=email)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="UserToken " + token.key)
    return client


@pytest.mark.django_db
@pytest.fixture
def client_apptoken(client):
    token = AppToken.objects.first()
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="AppToken " + token.key)
    return client


@pytest.mark.django_db
def test_api_view_unauthorized(client):
    response = client.get("/api/v1/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_api_view_records_tokens(client_apptoken, client_usertoken):
    response = client_apptoken.get("/api/v1/records/")
    assert response.status_code == 200
    response = client_usertoken.get("/api/v1/records/")
    assert response.status_code == 200
