""" Production Settings """

import dj_database_url
from decouple import config
from .base import *  # noqa

DEBUG = config("DJANGO_DEBUG", cast=bool, default=False)
SECRET_KEY = config("DJANGO_SECRET_KEY")

# Set to production domain - multiple values are allowed
# (eg. 'django-vue-template-demo.herokuapp.com')
ALLOWED_HOSTS = (
    ["*"]
    if DEBUG
    else config(
        "DJANGO_ALLOWED_HOSTS", cast=lambda v: [s.strip() for s in v.split(",")]
    )
)


# DATABASE
DATABASE_URL = config("DATABASE_URL")
DATABASES = {"default": dj_database_url.config(default=DATABASE_URL)}
