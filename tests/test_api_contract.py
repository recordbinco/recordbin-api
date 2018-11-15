# # https://pytest-django.readthedocs.io/en/latest/helpers.html#client-django-test-client
import pytest
import json

from pyswagger import App
from pyswagger.contrib.client.requests import Client


FIXTURE_UNIT_MIX_ID = "3da7b9f6-1462-4647-8f03-e825ced535be"
FIXTURE_DISTRIBUTION_ID = "8c6eacb6-bf15-4e05-adef-242c7313e2e4"

DISTRIBUTION_POST_PAYLOAD = {
    "floors": [
        {
            "id": "0a94bb09-8d7e-44cf-a0c8-496948ef0640",
            "level": 1,
            "area": 10000,
            "stargate_floor_uuid": None,
            "target_desk_count": 181,
            "unit_mix_map": "8.5",
        },
        {
            "id": "b940d8ee-6c3b-456e-8218-c9a715056b67",
            "level": 2,
            "area": 15000,
            "stargate_floor_uuid": None,
            "target_desk_count": 181,
            "unit_mix_map": "6.5",
        },
    ],
    "stargate_property_uuid": None,
    "created_by": "dev@dev.com",
}

UNIT_MIX_MAP_PAYLOAD = {
    "name": "Test Unit Mix Name",
    "directives": [
        {
            "space_type_sku": {"space_type": "PRIVATE OFFICE", "desk_count": 2},
            "percentage_min": 0.03,
        },
        {
            "space_type_sku": {"space_type": "PRIVATE OFFICE", "desk_count": 4},
            "percentage_min": 0.05,
        },
    ],
}

operation_list = [
    ("distributions_list", {}),
    ("floors_list", {}),
    ("pricing-exports_list", {}),
    ("program-types_list", {}),
    ("space-type-instances_list", {}),
    ("space-type-sku-instances_list", {}),
    ("space-types_list", {}),
    ("unit-mix-directives_list", {}),
    ("unit-mix-maps_list", {}),
    ("unit-mix-maps_read", dict(id=FIXTURE_UNIT_MIX_ID)),
    ("virtual-reservables_list", {}),
    ("distributions_read", dict(id=FIXTURE_DISTRIBUTION_ID)),
    ("distributions_create", dict(data=DISTRIBUTION_POST_PAYLOAD)),
    ("unit-mix-maps_create", dict(data=UNIT_MIX_MAP_PAYLOAD)),
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


@pytest.mark.parametrize("operation_name,kwargs", operation_list)
def test_contracts(app, client, operation_name, kwargs):
    client = Client()
    req, resp = app.op[operation_name](**kwargs)
    resp = client.request((req, resp))
    assert resp.status in (200, 201)
    if resp.status == 200:
        assert resp.data


def test_pricing_has_windows_filter(app, client):
    client = Client()
    req, resp = app.op["pricing-exports_list"](has_window=True)
    resp = client.request((req, resp))
    assert resp.status == 200
    data = json.loads(resp.raw)
    assert all([r["has_window"] == True for r in data])


def test_pricing_desk_count_filter(app, client):
    client = Client()
    req, resp = app.op["pricing-exports_list"](desk_count=4)
    resp = client.request((req, resp))
    assert resp.status == 200
    data = json.loads(resp.raw)
    assert data
    assert all([r["desk_count"] == 4 for r in data])


def test_pricing_room_number(app, client):
    client = Client()
    req, resp = app.op["pricing-exports_list"](room_number="VR-1-101")
    resp = client.request((req, resp))
    assert resp.status == 200
    data = json.loads(resp.raw)
    assert data
    assert all([r["room_number"] == "VR-1-101" for r in data])


def test_pricing_room_floor_filter(app, client):
    client = Client()
    kwarg = dict(stargate_floor_uuid="dea2cc95-0e12-11e6-9312-063c4950d72f")
    req, resp = app.op["pricing-exports_list"](**kwarg)
    resp = client.request((req, resp))
    assert resp.status == 200
    data = json.loads(resp.raw)
    assert data
    assert all(
        [r["stargate_floor_uuid"] == kwarg["stargate_floor_uuid"] for r in data]
    )


# def test_pricing_room_property_filter(app, client):
#     client = Client()
#     kwarg = dict(stargate_floor_uuid="dea2cc95-0e12-11e6-9312-063c4950d72f")
#     req, resp = app.op["pricing-exports_list"](**kwarg)
#     resp = client.request((req, resp))
#     assert resp.status == 200
#     data = json.loads(resp.raw)
#     assert data
#     assert all(
#         [r["stargate_floor_uuid"] == kwarg["stargate_floor_uuid"] for r in data]
#     )
