""" Production Settings """

import dj_database_url
from decouple import config
from .base import *  # noqa

DEBUG = config("DJANGO_DEBUG", cast=bool, default=False)
SECRET_KEY = config("DJANGO_SECRET_KEY", default=None) or "DevSecret"
if SECRET_KEY == "DevSecret" and not DEBUG:
    raise EnvironmentError("DJANGO SECRET NOT SET in production mode not allowed")

# Set to production domain - multiple values are allowed
# (eg. 'django-vue-template-demo.herokuapp.com')
if DEBUG:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = config(
        "DJANGO_ALLOWED_HOSTS", cast=lambda v: [s.strip() for s in v.split(",")]
    )


# DATABASE
DOCKER_DATABASE_URL = "postgres://postgres@db:5432/recordbindb"
DATABASE_URL = config("DATABASE_URL", default=None) or DOCKER_DATABASE_URL
DATABASES = {"default": dj_database_url.config(default=DATABASE_URL)}
