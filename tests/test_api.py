# # https://pytest-django.readthedocs.io/en/latest/helpers.html#client-django-test-client
import pytest
from rest_framework.test import APIClient

from backend.recordbin.models import AppToken

# TODO: Add Token Tests

@pytest.mark.django_db
@pytest.fixture
def authenticated_client(client):
    token = AppToken.objects.first()
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="AppToken " + token.key)
    return client


@pytest.mark.django_db
def test_api_view_unauthorized(client):
    response = client.get("/api/v1/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_api_view_authorized(authenticated_client):
    response = authenticated_client.get("/api/v1/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_admin(client):
    response = client.get("/")
    assert response.status_code in (200, 302)


@pytest.mark.django_db
def test_openapi_spec(authenticated_client):
    response = authenticated_client.get("/openapi.yaml")
    assert response.status_code == 200


@pytest.mark.django_db
def test_docs(authenticated_client, client):
    # requires collectstatic
    response = authenticated_client.get("/redoc/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_docs_unauthorized(client):
    response = client.get("/redoc/")
    assert response.status_code == 403


def test_wsgi():
    from backend.wsgi import application  # noqa

    assert application


@pytest.mark.django_db
def test_unauthorized(client):
    response = client.get("/api/v1/records/")
    assert response.status_code == 403
