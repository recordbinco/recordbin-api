# # https://pytest-django.readthedocs.io/en/latest/helpers.html#client-django-test-client
import pytest

from pyswagger import App, Security
from pyswagger.contrib.client.requests import Client
from backend.recordbin.models import AppToken
from rest_framework.authtoken.models import Token as UserToken


@pytest.fixture
def ADMIN_PAYLOAD(ADMIN_CREDENTIALS):
    return {"data": ADMIN_CREDENTIALS}


@pytest.fixture(scope="session")
def app(live_server):
    """ Live Server URL set on test.py LIVE_TEST_SERVER_ADDRESS """
    app = App._create_(f"{live_server.url}/openapi.yaml")
    yield app
    while live_server.thread.isAlive():
        live_server.stop()


@pytest.mark.django_db
@pytest.fixture
def client_usertoken(app):
    auth = Security(app)
    usertoken = UserToken.objects.first()
    auth.update_with("UserTokenHeader", f"UserToken {usertoken.key}")
    client = Client(auth)
    return client


@pytest.mark.django_db
@pytest.fixture
def client_apptoken(app):
    auth = Security(app)
    apptoken = AppToken.objects.first()
    auth.update_with("AppTokenHeader", f"AppToken {apptoken.key}")
    client = Client(auth)
    return client


@pytest.mark.django_db
@pytest.fixture
def app_token_readonly(app):
    apptoken = AppToken.objects.first()
    apptoken.permissions = "R"
    apptoken.save()


@pytest.mark.django_db
@pytest.fixture
def app_token_writeonly(app):
    apptoken = AppToken.objects.first()
    apptoken.permissions = "W"
    apptoken.save()


@pytest.mark.django_db
def test_api_v1_records_list(app, client_apptoken):
    operation_name = "api_v1_records_list"
    req, resp = app.op[operation_name](**{})
    resp = client_apptoken.request((req, resp))
    assert resp.status in (200, 201)


@pytest.mark.django_db
def test_api_v1_records_list_writeonly(app, client_apptoken, app_token_writeonly):
    operation_name = "api_v1_records_list"
    req, resp = app.op[operation_name](**{})
    resp = client_apptoken.request((req, resp))
    assert resp.status == 403


@pytest.mark.django_db
def test_api_v1_records_create(app, client_apptoken):
    operation_name = "api_v1_records_create"
    req, resp = app.op[operation_name](**{})
    resp = client_apptoken.request((req, resp))
    assert resp.status == 201


@pytest.mark.django_db
def test_api_v1_records_create_readonly(app, client_apptoken, app_token_readonly):
    operation_name = "api_v1_records_create"
    req, resp = app.op[operation_name](**{})
    resp = client_apptoken.request((req, resp))
    assert resp.status == 403


@pytest.mark.django_db
def test_api_v1_apps_list(app, client_usertoken):
    operation_name = "api_v1_apps_list"
    req, resp = app.op[operation_name](**{})
    resp = client_usertoken.request((req, resp))
    assert resp.status == 200


@pytest.mark.django_db
def test_api_v1_tokens_list(app, client_usertoken):
    operation_name = "api_v1_tokens_list"
    req, resp = app.op[operation_name](**{})
    resp = client_usertoken.request((req, resp))
    assert resp.status in (200, 201)
