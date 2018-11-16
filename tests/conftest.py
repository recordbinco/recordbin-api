# https://pytest-django.readthedocs.io/en/latest/database.html#examples
import pytest

import os
import django
import dj_database_url

from django.core.management import call_command

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def run_sql(sql):
    conn = psycopg2.connect(database="postgres")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()


# @pytest.mark.django_db
def pytest_configure():
    os.environ["DJANGO_SETTINGS_MODULE"] = "backend.settings"
    django.setup()


# @pytest.fixture(scope="session")
# def django_db_modify_db_settings():
#     from django.conf import settings
#     docker_db = "postgres://postgres@db:5432/recordbindb"
#     db_config = dj_database_url.config(default=docker_db)
#     DATABASES = {"default": db_config}
#     settings.DATABASES = DATABASES


@pytest.fixture(scope="session")
def django_db_setup(django_db_blocker):
    from django.conf import settings

    docker_db = "postgres://postgres@db:5432/recordbindb"
    db_config = dj_database_url.config(default=docker_db)
    DATABASES = {"default": db_config}
    settings.DATABASES = DATABASES
    with django_db_blocker.unblock():
        call_command("loaddata", "./backend/fixtures/all.json")

