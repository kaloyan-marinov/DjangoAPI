use Docker to serve the persistence layer,
but use `localhost` (= the local network interface) to serve the Django application:

```
$ python3 --version
Python 3.8.3

$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install --upgrade pip
(venv) $ pip install -r requirements.txt
```

```
docker run \
    --name container-DjangoAPI-postgres \
    --mount source=volume-DjangoAPI-postgres,destination=/var/lib/postgresql/data \
    --env POSTGRES_PASSWORD=p_4_DjangoAPI_database \
    --env POSTGRES_USER=u_4_DjangoAPI_database \
    --env POSTGRES_DB=DjangoAPI_database \
    --publish 5432:5432 \
    postgres:15.1
```

```
# Launch one terminal instance and, in it, start serving the application:

(venv) $ python manage.py runserver
```
