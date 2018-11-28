### Local Server

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
