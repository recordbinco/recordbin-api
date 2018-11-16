FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/
RUN pip3 install -q -r requirements.txt

ADD . /code/

# Default Docker DB - Set Environment in to override
# DEBUG set to one so it can build without errors
ARG DJANGO_DEBUG
ARG DJANGO_ALLOWED_HOSTS
ARG DJANGO_SECRET_KEY
ARG DATABASE_URL


# Can't run here because it requires env vars
RUN python manage.py collectstatic --noinput -v=0


RUN chmod u+x ./docker-entrypoint.sh
# Heroku Requires a CMD so entrypoint
# must be called here instead of compose
CMD [ "sh", "./docker-entrypoint.sh"]
