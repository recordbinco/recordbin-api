# https://pytest-django.readthedocs.io/en/latest/database.html#examples
import pytest

import os
import django

# from django.conf import settings
from django.core.management import call_command


# @pytest.mark.django_db
def pytest_configure():
        """ Test Settings """
        # DEBUG = False
        # ALLOWED_HOSTS = ["*"]
        # # os.environ["DJANGO_LIVE_TEST_SERVER_ADDRESS"] = "localhost:8001"

        # DATABASES = {
        # "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db_test.sqlite3"}
}

#     os.environ["DJANGO_SETTINGS_MODULE"] = "backend.settings.test"
    # settings.DEBUG = False
    # settings.FIXTURE_DIRS = ['api/docs/fixtures/']
    django.setup()


@pytest.fixture
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "./backend/fixtures/all.json")
