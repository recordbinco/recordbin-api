# # https://pytest-django.readthedocs.io/en/latest/helpers.html#client-django-test-client
import pytest

from pyswagger import App, Security
from pyswagger.contrib.client.requests import Client
from backend.recordbin.models import SourceToken


@pytest.fixture
def ADMIN_PAYLOAD(ADMIN_CREDENTIALS):
    return {"data": ADMIN_CREDENTIALS}


@pytest.fixture
def JWT_PAYLOAD(JWT_TOKEN):
    return {"data": {"token": JWT_TOKEN}}


operation_list = [
    ("api_v1_records_list", {}),
    ("api_v1_records_create", {}),
    ("api_v1_sources_list", {}),
    ("api_v1_tokens_list", {}),
    ("api_v1_auth_token-new_create", pytest.lazy_fixture("ADMIN_PAYLOAD")),
    ("api_v1_auth_token-refresh_create", pytest.lazy_fixture("JWT_PAYLOAD")),
    ("api_v1_auth_token-verify_create", pytest.lazy_fixture("JWT_PAYLOAD")),
]


@pytest.fixture(scope="session")
def app(live_server):
    """ Live Server URL set on test.py LIVE_TEST_SERVER_ADDRESS """
    app = App._create_(f"{live_server.url}/openapi.yaml")
    yield app
    while live_server.thread.isAlive():
        live_server.stop()


def test_all_operations_tested(app):
    defined_ops = list(app.op.keys())
    assert len(defined_ops) == len(operation_list)


@pytest.mark.django_db
@pytest.fixture
def auth(app):
    auth = Security(app)
    token = SourceToken.objects.first()
    auth.update_with("SourceTokenHeader", f"Token {token.key}")
    return auth


@pytest.mark.django_db
@pytest.mark.parametrize("operation_name,kwargs", operation_list)
def test_contracts(app, auth, operation_name, kwargs):
    client = Client(auth)
    req, resp = app.op[operation_name](**kwargs)
    resp = client.request((req, resp))
    assert resp.status in (200, 201)
    # jwt endpoints resp.data returns None

