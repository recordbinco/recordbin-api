#!/bin/bash

# TODO make collectstatic automatic, trigger collect only if change. Maybe using dockerfile?
# This only needs to be run once, to package admin/jet static files
# Since it's a lengthy call, disable it during dev for faster container start
# echo ">>> creating staticfiles"
# python manage.py collectstatic --noinput --link -v=0  # Collect static files

python manage.py migrate --noinput -v0
# Apply database migrations

if [ $DJANGO_DEBUG -eq "1" ]; then
    echo ">>> DJANGO DEBUG is 1"
    echo ">>> Create admin user + token if debugging"
    echo ">>> running migrations"

    echo ">>> seeding database"
    python manage.py seed # Load Seed Data
    python manage.py loaddata backend/fixtures/dev_admin.json
    python manage.py loaddata backend/fixtures/authtoken.json
    echo ">>> starting Dev Server"
    exec python manage.py runserver 0.0.0.0:$PORT
else
    echo ">>> DJANGO DEBUG not 1"
    echo ">>> starting Gunicorn"
    # exec gunicorn backend.wsgi -b 0.0.0.0:$PORT --log-file -
    # Start Gunicorn processes
    # exec python manage.py runserver 0.0.0.0:$PORT
    exec gunicorn backend.wsgi \
        --name recordbin \
        --reload
        --reload-extra-file /code/
        --bind 0.0.0.0:$PORT \
        --log-level=info \
        --log-file -
        --workers 2 \
        # "$@"
fi

