# Record Bin (WIP)

Record Bin is flexible deployable API Service that can receive schemaless records for persistent storage.

### Example

- [Admin Panel](http://ww-recordbin.herokuapp.com/) (admin:admin)
- [Api Docs](http://ww-recordbin.herokuapp.com/redoc/)
- [Api Explorer](http://ww-recordbin.herokuapp.com/api/v1/)
- Sample Request

```
curl -H "Content-Type: application/json" -H "Authorization: Token <token>" \
     --request POST \
     --data '{"username":"xyz","result":0, "action": "deleted"}' \
     http://ww-recordbin.herokuapp.com/api/v1/records/
```

## Development Server

```
$ git clone git@github.com:gtalarico/recordbin.git
$ cd recordbin
```

### Local Server - Non-Docker

#### Requirements

- pipenv
- postgres
- python 3+

```
$ pipenv install --dev
$ createdb recordbindb
$ set  DATABASE_URL="postgres://postgres:postgres@localhost:5432/recordbindb"
$ python manage.py migrate
$ python manage.py runserver
```

### Local Server - Docker

#### Requirements

- docker

```
$ docker-compose up db -d
$ docker-compose up web
```

##### Development Mode

By default, the server will run as if in a Production enviroment:
use Gunicorn and turn debugging off.

To run a local server in Django Debug and use Django Dev server,
set an environment varriable (`DJANGO_DEBUG=1`) or run
`env DJANGO_DEBUG=1 docker-compose up web`

- Inspect / Manage

This command will enter a bash enviroment inside your docker container,
allowing you to perform tasks with `python manage.py` freely.

```
$ docker-compose run web bash
```

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

### Push and Release Code (Container)

```
heroku container:login
heroku container:push web
heroku container:release web
```

### Push and Release Code (Legacy)

```
heroku git:remote
git push heroku
```

### Create Super User

```
heroku run python manage.py createsuperuser
```

Note: In development mode (see section above), dev server will include an admin user (username: admin, pwd: admin).

# Tests

```
docker-compose run tests
```

## TODO

- [ ] Change Schema to receive {"data": } ?
- [ ] Add Auth Docs
- [x] Add instructions for querying / retrieving data
- [x] Add Tableau Json endpoint
- [x] Add Auth
- [x] Fix Tests (test db config - sqlite not working because of json field)
