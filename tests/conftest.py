# https://pytest-django.readthedocs.io/en/latest/database.html#examples
import pytest

import os
import django

# from django.conf import settings
from django.core.management import call_command


@pytest.mark.django_db
def pytest_configure():
    os.environ["DJANGO_SETTINGS_MODULE"] = "backend.settings.test"
    # settings.DEBUG = False
    # settings.FIXTURE_DIRS = ['api/docs/fixtures/']
    django.setup()


@pytest.fixture
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "./backend/distribution/fixtures/ALL.json")
