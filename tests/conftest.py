# https://pytest-django.readthedocs.io/en/latest/database.html#examples
import pytest

import os
import django

from django.core.management import call_command

x = "asdsdsds"


def pytest_configure():
    os.environ["DJANGO_SETTINGS_MODULE"] = "backend.settings"
    django.setup()


@pytest.fixture(scope="function")
def django_db_setup(django_db_blocker):
    with django_db_blocker.unblock():
        # call_command("flush", "--noinput")
        call_command("loaddata", "./backend/fixtures/all.json")
