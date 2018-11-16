FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/
RUN pip3 install -q -r requirements.txt

ADD . /code/

# Default Docker DB - Set Environment in to override
ARG DJANGO_DEBUG
ARG DJANGO_SECRET_KEY
ARG DJANGO_ALLOWED_HOSTS
ARG DATABASE_URL
# ARG DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

# Can't run here because it requires env vars
RUN python manage.py collectstatic --noinput -v=0


RUN chmod u+x ./docker-entrypoint.sh
# Heroku Requires a CMD so entrypoint
# must be called here instead of compose
CMD [ "sh", "./docker-entrypoint.sh" ]
