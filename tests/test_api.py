# # https://pytest-django.readthedocs.io/en/latest/helpers.html#client-django-test-client
import pytest


@pytest.mark.django_db
def test_api_root(client):
    response = client.get("/api/v1/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_docs(client):
    response = client.get("/openapi.yaml")
    assert response.status_code == 200
    # requires collectstatic
    response = client.get("/redoc/")
    assert response.status_code == 200
    response = client.get("/swagger.json")
    assert response.status_code == 200


def test_wsgi():
    from backend.wsgi import application  # noqa

    assert application


# def test_headers_middleware(client):
#     response = client.get('/')
#     assert response.get('cache-control')
