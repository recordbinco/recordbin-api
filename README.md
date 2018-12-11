# Record Bin

[![CircleCI](https://circleci.com/gh/recordbinco/recordbin-api.svg?style=svg)](https://circleci.com/gh/recordbinco/recordbin-api)
[![codecov](https://codecov.io/gh/recordbinco/recordbin-api/branch/master/graph/badge.svg)](https://codecov.io/gh/recordbinco/recordbin-api)

Record Bin is flexible deployable API Service that can receive schemaless records for persistent storage.

### Demo

- [Web: www.recordbin.co](http://recordbin.co)
- [Api: Admin](http://api.recordbin.co/) (user: admin@admin.co / pwd:admin)
- [Api: Docs](http://api.recordbin.co/redoc/) (login into admin first)

### Sample Record Post Request

```
curl -H "Content-Type: application/json" \
     -X POST \
     -d '{"username":"xyz","result":0, "action": "deleted"}' \
     "http://api.recordbin.co/api/v1/records/?apptoken=7419a34711c3b15b1d8793ef6221e2b080e6944c"
```

#### Python Client

[RecordBin Python](http://www.github.com/gtalarico/recordbin-python)

```
$ pip install recordbin
$ pyhton
>>> from recordbin import RecordBin
>>> bin = RecordBin(url='http://api.recordbin.co',
                    token='7419a34711c3b15b1d8793ef6221e2b080e6944c')
>>> bin.post({'username': 'python'})
>>> # .post returns a Future object. To confirm result call `result()` on response:
>>> resp = bin.post({'username': 'python'})
>>> resp.result()
<Response [201]>
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
heroku config:set DJANGO_SECRET_KEY=SomeSecretString
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
(username: admin@admin.com, pwd: admin).

# Tests

```
$ make tests
$ make testsbash
```

# Helpful Docker Commands

`python manage.py makemigrations recordbin`

# Todo

- [ ] ReOrganize this Repo
- [ ] Add App Create, Token View, Token Edit
- [ ] Add JSON Export Endpoint
- [ ] Add heroku.sh initializer
- [ ] Simplify Docker Setup
- [ ] Change Schema to receive {"data": } ?
- [x] Add Circle CI (see python-stds)
- [x] Add registration
