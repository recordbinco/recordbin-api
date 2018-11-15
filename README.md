# Record Bin

Django Based, Minimal Rest API ro receive log records

### Launch Server

- Run Dev Server

```
docker-compose up
```

- Inspect

```
docker-compose run web bash
```

### Database

- Launch

```
docker-compose up db
```

- Inspect / Connect from Host

```
psql -p 5433 -d logger -U postgres -h 0.0.0.0
```

# Heroku

`heroku container:login`
`heroku container:push web -r staging`
`heroku container:release web -r staging`
`heroku run python manage.py createsuperuser -r staging`

## Deploy Legacy

```
$ heroku apps:create logger
$ heroku git:remote --app logger
$ heroku buildpacks:add heroku/python
$ heroku addons:create heroku-postgresql:hobby-dev
$ heroku config:set DJANGO_ALLOWED_HOSTS=yourdomain.com
$ git push heroku
```

The python buildpack will detect the `pipfile` and install all the python dependencies.
`collectstatic` will run automatically.

The `Procfile` will run Django migrations and then launch Django'S app using gunicorn,
as recommended by heroku.

### Template Structure

| Location          | Content                         |
| ----------------- | ------------------------------- |
| `/backend`        | Django Project & Backend Config |
| `/backend/logger` | Django App (`/api/v1/`)         |

## Setup

```
$ git clone {URL}
$ cd genomevr
$ pipenv install --dev & pipenv shell
$ python manage.py migrate
```

```
docker-compose run web python manage.py makemigrations records
```
