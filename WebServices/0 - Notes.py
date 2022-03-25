""" For app database_api, steps to get django connecting to database and tests to work:

!!! django-mssql-backend currently supporting till Django 3.0.10. Temporary fix is downgrade your Django version from Django 3.1.x to 3.0.10. !!!!
Ref: https://stackoverflow.com/questions/63282351/django-and-azure-sql-key-error-deferrable-when-start-migrate-command

Restore new database using SSMS (if on SRV02, it will propably need to delete and recreate user adm.ga (both in general and in GA)).

Open Command Prompt in project folder.
    env37\Scripts\activate                                      Activating environment.
    python manage.py migrate database_api 0001 --fake           Faking migration of database_api - 0001 (writing in table django_migrations that migration already occoured). Ref: https://stackoverflow.com/questions/43880426/how-to-force-migrations-to-a-db-if-some-tables-already-exist-in-django/43881920    
    python manage.py migrate                                    Migrating other models (includind Django tables).
    python manage.py createsuperuser                            Creating super user.
        login: adm.ga
        email: DevOps.GlobalAdvising@gmail.com
        Password: dj
"""