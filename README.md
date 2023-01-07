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
    --username=u_4_DjangoAPI_database \
    --password \
    DjangoAPI_database

DjangoAPI_database=# \d
                                   List of relations
 Schema |                   Name                   |   Type   |         Owner          
--------+------------------------------------------+----------+------------------------
 public | EmployeeApp_departments                  | table    | u_4_DjangoAPI_database
 public | EmployeeApp_departments_DepartmentId_seq | sequence | u_4_DjangoAPI_database
 public | EmployeeApp_employees                    | table    | u_4_DjangoAPI_database
 public | EmployeeApp_employees_EmployeeId_seq     | sequence | u_4_DjangoAPI_database
 public | django_migrations                        | table    | u_4_DjangoAPI_database
 public | django_migrations_id_seq                 | sequence | u_4_DjangoAPI_database
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
    --username=u_4_DjangoAPI_database \
    --password \
    DjangoAPI_database

DjangoAPI_database=# INSERT INTO "EmployeeApp_departments" VALUES (1, 'Accounting');
        
DjangoAPI_database=# INSERT INTO "EmployeeApp_departments" VALUES (2, 'Human Resources');
        
DjangoAPI_database=# SELECT * FROM "EmployeeApp_departments";

DjangoAPI_database=# INSERT INTO "EmployeeApp_employees"
        VALUES (1, 'Janice', 'Accounting', '2015-09-01', 'janice@protonmail.com');

DjangoAPI_database=# SELECT * FROM "EmployeeApp_employees";
```

it is interesting to emphasize that
the quotation marks around each table name appear to be required
(because leaving them out did not work for me at least);
it was from
https://www.postgresql.org/message-id/1064987137.3f7a6a01455cb%40www.nexusmail.uwaterloo.ca
that I got the idea about surrounding each table name with quotation marks

)

```
# Launch one terminal instance and, in it, start serving the application:

(venv) $ python manage.py runserver
```
