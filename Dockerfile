FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/
RUN pip3 install -q -r requirements.txt

ADD . /code/

# This is
ARG DATABASE_URL="postgres://postgres@db:5432/recordbindb"
ARG DJANGO_SETTINGS_MODULE="backend.settings.prod"
ARG DJANGO_SECRET_KEY"DevSecret"
# ARG DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

# Can't run here because it requires env vars
RUN python manage.py collectstatic --noinput -v=0


RUN chmod u+x ./docker-entrypoint.sh
# Heroku Requires a CMD so entrypoint
# must be called here instead of compose
CMD [ "sh", "./docker-entrypoint.sh" ]
