# https://pytest-django.readthedocs.io/en/latest/database.html#examples
import pytest

import os
import django

from django.core.management import call_command


def pytest_configure():
    os.environ["DJANGO_SETTINGS_MODULE"] = "backend.settings"
    django.setup()


@pytest.fixture(scope="function")
def django_db_setup(django_db_blocker):
    with django_db_blocker.unblock():
        # call_command("flush", "--noinput")
        call_command("loaddata", "./backend/fixtures/all.json")


@pytest.fixture
def ADMIN_CREDENTIALS():
    return dict(username="admin", password="admin")


@pytest.mark.django_db
@pytest.fixture
def XXX_TOKEN(django_user_model):
        pass
#     from rest_framework_jwt.settings import api_settings
#     jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#     jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#     admin = django_user_model.objects.first()
#     payload = jwt_payload_handler(admin)
#     token = jwt_encode_handler(payload)
#     return token