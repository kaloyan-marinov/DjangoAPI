```
$ cp .env.template .env

# Edit the content of `.env` as per the comments/instructions therein.
```

the remainder of this description will explain how to
use Docker to serve the persistence layer,
but use `localhost` (= the local network interface) to serve the Django application

---

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
    --env-file .env \
    --publish 5432:5432 \
    postgres:15.1
```

```
(venv) $ python manage.py migrate EmployeeApp
```

(

OPTIONALLY, verify that the previous step did create
database tables associated with the `EmployeeApp/models.py`:

```
$ docker container exec -it container-DjangoAPI-postgres /bin/bash

root@<container-id> psql \
    --host=localhost \
    --port=5432 \
    --username=<the-value-for-POSTGRES_USER-in-the-.env-file> \
    --password \
    <the-value-for-POSTGRES_DB-in-the-.env-file>

<the-value-for-POSTGRES_DB-in-the-.env-file>=# \d
                                   List of relations
 Schema |                   Name                   |   Type   |         Owner          
--------+------------------------------------------+----------+------------------------
 public | EmployeeApp_departments                  | table    | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | EmployeeApp_departments_DepartmentId_seq | sequence | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | EmployeeApp_employees                    | table    | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | EmployeeApp_employees_EmployeeId_seq     | sequence | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | django_migrations                        | table    | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | django_migrations_id_seq                 | sequence | <the-value-for-POSTGRES_USER-in-the-.env-file>
(6 rows)
```

)

(

OPTIONALLY, insert some records into the database tables:

```
$ docker container exec -it container-DjangoAPI-postgres /bin/bash

root@<container-id> psql \
    --host=localhost \
    --port=5432 \
    --username=<the-value-for-POSTGRES_USER-in-the-.env-file> \
    --password \
    <the-value-for-POSTGRES_DB-in-the-.env-file>

<the-value-for-POSTGRES_DB-in-the-.env-file>=# INSERT INTO "EmployeeApp_employees"
        VALUES (1, 'Janice', 'Accounting', '2015-09-01', 'janice@protonmail.com');

<the-value-for-POSTGRES_DB-in-the-.env-file>=# SELECT * FROM "EmployeeApp_employees";
```

it is interesting to emphasize that
the quotation marks around each table name appear to be required
(because leaving them out did not work for me at least);
it was from
https://www.postgresql.org/message-id/1064987137.3f7a6a01455cb%40www.nexusmail.uwaterloo.ca
that I got the idea about surrounding each table name with quotation marks

)

---

```
# Launch one terminal instance and, in it, start serving the application:

(venv) $ python manage.py runserver
```

```
# Launch a second terminal instance and, in it, issue requests to the application:

$ http localhost:8000/departments

$ http POST localhost:8000/departments \
    DepartmentName="Accounting"

$ http POST localhost:8000/departments \
    DepartmentName="Human Resources"

$ http POST localhost:8000/departments \
    DepartmentName="CustomerSuppor"

$ http localhost:8000/departments

$ http PUT localhost:8000/departments \
    DepartmentId=3 \
    DepartmentName="Customer Support"

$ http localhost:8000/departments

$ http DELETE localhost:8000/departments/3
```
