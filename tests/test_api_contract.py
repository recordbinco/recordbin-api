# # https://pytest-django.readthedocs.io/en/latest/helpers.html#client-django-test-client
import pytest
import json

from pyswagger import App, Security
from pyswagger.contrib.client.requests import Client
from django.conf import settings
from rest_framework.authtoken.models import Token

# FIXTURE_UNIT_MIX_ID = "3da7b9f6-1462-4647-8f03-e825ced535be"
# FIXTURE_DISTRIBUTION_ID = "8c6eacb6-bf15-4e05-adef-242c7313e2e4"

operation_list = [("api_v1_records_list", {}), ("api_v1_records_create", {})]


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
def auth():
    auth = Security(app)
    token = Token.objects.first()
    auth.update_with("APIKeyHeader", f"Token {token.key}")
    return auth


@pytest.mark.django_db
@pytest.mark.parametrize("operation_name,kwargs", operation_list)
def test_contracts(app, client, operation_name, kwargs):
    auth = Security(app)
    token = Token.objects.first()
    auth.update_with("APIKeyHeader", f"Token {token.key}")
    client = Client(auth)
    req, resp = app.op[operation_name](**kwargs)
    resp = client.request((req, resp))
    assert resp.status in (200, 201)
    if resp.status == 200:
        assert resp.data


# def test_pricing_has_windows_filter(app, client, token):
# client = Client()


#     req, resp = app.op["pricing-exports_list"](has_window=True)
#     resp = client.request((req, resp))
#     assert resp.status == 200
#     data = json.loads(resp.raw)
#     assert all([r["has_window"] == True for r in data])
