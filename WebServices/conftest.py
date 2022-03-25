# Using an existing, external database for tests. Ref: https://pytest-django.readthedocs.io/en/latest/database.html#using-an-existing-external-database-for-tests

import pytest
from WebServices import settings

@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'sql_server.pyodbc',
        'HOST': '.\SQLEXPRESS',
        'NAME': 'GA',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'unicode_results': True,
        },
    }

