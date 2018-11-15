# Record Bin (WIP)

Record Bin is flexible deployable API Service that can receive schemaless records for persistent storage.

### Example

```
curl --header "Content-Type: application/json" \
     --request POST \
     --data '{"username":"xyz","password":"xyz"}' \
     http://myapp.herokuapp.com/api/v1/records/
```

## Development Server

```
$ git clone git@github.com:gtalarico/recordbin.git
$ cd recordbin
```

### Docker

- Run Local Server

```
$ docker-compose up -d db
$ docker-compose up web
```

Server will run as if in a Production enviroment.
To setup a development enviroment with debug debug, create a `.env`
file with the following:

```
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=*
```

In development mode, dev server will include an admin user (username: admin, pwd: admin).

- Inspect / Manage

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
```

### Push and Release Code

```
heroku container:login
heroku container:push web
heroku container:release web
```

### Create Super User

```
heroku run python manage.py createsuperuser
```
