# # https://pytest-django.readthedocs.io/en/latest/helpers.html#client-django-test-client
import pytest
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.test import APIClient

from rest_framework.authtoken.models import Token


@pytest.mark.django_db
@pytest.fixture
def token():
    return Token.objects.first()


@pytest.fixture
def authenticated_client(client, token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    return client


@pytest.mark.django_db
def test_api_view_unauthorized(client):
    response = client.get("/api/v1/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_api_view(authenticated_client):
    response = authenticated_client.get("/api/v1/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_admin(client):
    response = client.get("/")
    assert response.status_code in (200, 302)


def test_openapi(authenticated_client):
    response = authenticated_client.get("/openapi.yaml")
    assert response.status_code == 200


@pytest.mark.django_db
def test_openapi(authenticated_client, client):
    # requires collectstatic
    response = authenticated_client.get("/redoc/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_openapi_auth(client):
    response = client.get("/redoc/")
    assert response.status_code == 401


def test_wsgi():
    from backend.wsgi import application  # noqa

    assert application


@pytest.mark.django_db
def test_unauthorized(client):
    response = client.get("/api/v1/records/")
    assert response.status_code == 401
