# Record Bin (WIP)

Record Bin is flexible deployable API Service that can receive schemaless records for persistent storage.

### Example

- [Admin Panel](http://ww-recordbin.herokuapp.com/) (admin:admin)
- [Api Docs](http://ww-recordbin.herokuapp.com/redoc/)
- [Api Explorer](http://ww-recordbin.herokuapp.com/api/v1/)
- Sample Request

```
curl --header "Content-Type: application/json" \
     --request POST \
     --data '{"username":"xyz","result":0, "action": "deleted"}' \
     http://ww-recordbin.herokuapp.com/api/v1/records/
```

## Development Server

```
$ git clone git@github.com:gtalarico/recordbin.git
$ cd recordbin
```

### Docker

- Run Local Server

```
$ docker-compose up db -d
$ docker-compose up web
```

##### Development Mode

By default, the server will run as if in a Production enviroment.
To setup a development enviroment with debug debug, create a `.env`
file with the following entries:

```
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=*
```

These will be read by docker-compose and injected into the docker enviroment.

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

Note: In development mode (see section above), dev server will include an admin user (username: admin, pwd: admin).

## TODO

- Fix Tests (test db config - sqlite not working because of json field)
- Add instructions for querying / retrieving data
- Add Pagination
