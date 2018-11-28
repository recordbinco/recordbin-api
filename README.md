# Record Bin

[![Build Status](https://travis-ci.org/gtalarico/recordbin-python.svg?branch=master)](https://travis-ci.org/gtalarico/recordbin-python)

[![codecov](https://codecov.io/gh/gtalarico/recordbin-python/branch/master/graph/badge.svg)](https://codecov.io/gh/gtalarico/recordbin-python)

---

![project-logo](https://github.com/gtalarico/recordbin/blob/master/art/logo.png)

Record Bin is flexible deployable API Service that can receive schemaless records for persistent storage.

### Demo

- [Admin Panel](http://ww-recordbin.herokuapp.com/) (admin:admin)
- [Api Docs](http://ww-recordbin.herokuapp.com/redoc/)\*
- [Api Explorer](http://ww-recordbin.herokuapp.com/api/v1/)\*
  \*Must login Admin panel first to authenticate

### Sample Record Post Request

```
curl -H "Content-Type: application/json" -H "Authorization: Token <token>" \
     --request POST \
     --data '{"username":"xyz","result":0, "action": "deleted"}' \
     http://ww-recordbin.herokuapp.com/api/v1/records/
```

## Querying

More on querying RecordBin Data [here](https://github.com/gtalarico/recordbin/blob/master/QUERYING.md)

## Development Server

```
$ git clone git@github.com:gtalarico/recordbin.git
$ cd recordbin
```

### Local Server (Docker)

```
$ make start
```

For other useful commands use `$ make usage`

##### Development Mode

By default, the server will run as if in a Production enviroment:
use Gunicorn and turn debugging off.

To run a local server in Django Debug and use Django Dev server,
set an environment variable (`DJANGO_DEBUG=1`) or run
`env DJANGO_DEBUG=1 docker-compose up web`

## Heroku Deployment

### Setup App

```
heroku apps:create <appname>
heroku git:remote --app <appname>
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set DJANGO_ALLOWED_HOSTS=<appname>.herokuapp.com
heroku config:set DJANGO_SECRET_KEY=<appname>.herokuapp.com
heroku config:set DJANGO_DEBUG=0
```

### Release

```
heroku container:login
heroku container:push web
heroku container:release web
```

### Create Super User

```
heroku run python manage.py createsuperuser
```

Note: In Development Mode (see section above),
the Development Server includes a seeded admin user
(username: admin, pwd: admin).

# Tests

```
$ docker-compose run tests
# or
$ docker-compose run tests bash
$ pytest
```

# Todo

- [ ] Package all commands in Makefile
- [ ] Change Schema to receive {"data": } ?
- [x] Disconnect Token from User
- [x] Add instructions for querying / retrieving data
- [x] Add Tableau Json endpoint
- [x] Add Auth
- [x] Fix Tests (test db config - sqlite not working because of json field)
