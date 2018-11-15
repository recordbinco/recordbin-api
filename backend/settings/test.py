""" Test Settings """
# https://gitlab.com/gtalarico/rad.web/blob/master/api/configs/test.py
import os

# import dj_database_url
from .prod import *  # noqa

DEBUG = False
ALLOWED_HOSTS = ["*"]
# os.environ["DJANGO_LIVE_TEST_SERVER_ADDRESS"] = "localhost:8001"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join("tests", "db_test.sqlite3"),
    }
}
