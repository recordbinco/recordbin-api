""" Settings """
import os
import dj_database_url
from decouple import config, Csv

os.environ.setdefault("DJANGO_DEBUG", "0")
os.environ.setdefault("DJANGO_ALLOWED_HOSTS", "*")
os.environ.setdefault("DJANGO_SECRET_KEY", "DevSecret")
docker_db = "postgres://postgres@db:5432/recordbindb"
os.environ.setdefault("DATABASE_URL", docker_db)

# See Docker for defaults
DEBUG = config("DJANGO_DEBUG", cast=bool)
SECRET_KEY = config("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", cast=Csv())


# DATABASE
DATABASE_URL = config("DATABASE_URL")
db_config = dj_database_url.config(default=DATABASE_URL)
DATABASES = {"default": db_config}  # Django DATABASES

# print(f"------------------------------------")
# print(f"DEBUG IS: {DEBUG}")
# print(f"ALLOWED_HOSTS IS: {ALLOWED_HOSTS}")
# print(f"SECRET_KEY IS: {SECRET_KEY[:5]}... (truncated)")
# print("DATABASE CONFIG: {USER}@{HOST}:{PORT}/{NAME} ".format(**db_config))
# print(f"------------------------------------")
