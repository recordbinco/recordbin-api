""" Settings """

import dj_database_url
from decouple import config

# Imports base settings
from .base import *  # noqa

# Configurable Vars
# DJANGO_DEBUG (default: False)
# DJANGO_SECRET_KEY (default if DEBUG else required)
# DJANGO_ALLOWED_HOSTS (default if DEBUG else required)
# DATABASE_URL (default docker db, else env)

DEBUG = config("DJANGO_DEBUG", cast=bool, default=False)

if DEBUG:
    SECRET_KEY = config("DJANGO_SECRET_KEY", default="DevSecret")
    ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", default=["*"])
else:
    SECRET_KEY = config("DJANGO_SECRET_KEY")
    cast_func = lambda v: [s.strip() for s in v.split(",")]  # noqa
    ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", cast=cast_func)
    # (eg. "'django-vue-template-demo.herokuapp.com')


# DATABASE
DOCKER_DATABASE_URL = "postgres://postgres@db:5432/recordbindb"
DATABASE_URL = config("DATABASE_URL", default=None) or DOCKER_DATABASE_URL
DATABASES = {"default": dj_database_url.config(default=DATABASE_URL)}
