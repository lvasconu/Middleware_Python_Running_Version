from django.shortcuts import get_object_or_404
from django.utils.timezone import make_aware

import datetime
import pytest
import pprint

from . import models as models_ga
from . import equipment

''' To run tests:
        Open cmd in project folder.
        Activate environment:   env37\Scripts\activate
        All tests:              pytest -s -v --durations=0 database_api\tests.py
        Specific test:          pytest -s -v --durations=0 database_api\tests.py -k "test_01_dia_semana_create"
        Refs:
            Using external database:    https://pytest-django.readthedocs.io/en/latest/database.html#using-an-existing-external-database-for-tests
            Pytest useful commands:     https://docs.pytest.org/en/reorganize-docs/new-docs/user/commandlineuseful.html
'''


@pytest.mark.django_db # Because needs database access. Ref: https://pytest-django.readthedocs.io/en/latest/database.html
def test_01_dia_semana_create():
    expected_data = 'Wednesday'

    models_ga.TbDiaSemana.objects.create(co_dia_semana = 8, ds_dia = expected_data, co_pessoa_cadastro = 1, dt_cadastro = make_aware(datetime.datetime.now()) )
    received = models_ga.TbDiaSemana.objects.get(co_dia_semana=8)
    
    received_data = received.ds_dia

    all_days = models_ga.TbDiaSemana.objects.all()

    # Printing ever day:
    for day in all_days:
        print(day.ds_dia)

    assert received_data == expected_data

@pytest.mark.django_db
def test_10_pessoa_create():

    tipo_pessoa = models_ga.TbTipoPessoa()
    tipo_pessoa.ds_tipo = 'tipo_pessoa_teste'
    tipo_pessoa.dt_cadastro = datetime.datetime.now()
    tipo_pessoa.save()


    key_1 = 'cpf teste 1'
    key_2 = 'cpf teste 2'

    person_1 = models_ga.TbPessoa()
    person_1.co_tipo_pessoa = tipo_pessoa
    person_1.no_pessoa = key_1
    person_1.st_ativo = 1
    person_1.dt_cadastro = datetime.datetime.now()
    person_1.nu_cpf = key_1
    person_1.save()

    person_2 = models_ga.TbPessoa()
    person_2.co_tipo_pessoa = tipo_pessoa
    person_2.no_pessoa = key_2
    person_2.st_ativo = 1
    person_2.dt_cadastro = datetime.datetime.now()
    person_2.nu_cpf = key_2
    person_2.save()

    received_1 = get_object_or_404(models_ga.TbPessoa, nu_cpf = key_1)
    received_2 = get_object_or_404(models_ga.TbPessoa, nu_cpf = key_2)

    assert received_1.nu_cpf == key_1
    assert received_2.nu_cpf == key_2

@pytest.mark.django_db
def test_11_pessoa_anonymize():

    tipo_pessoa = models_ga.TbTipoPessoa()
    tipo_pessoa.ds_tipo = 'tipo_pessoa_teste'
    tipo_pessoa.dt_cadastro = datetime.datetime.now()
    tipo_pessoa.save()

    key_1 = 'cpf teste 1'
    key_2 = 'cpf teste 2'

    person_1 = models_ga.TbPessoa()
    person_1.co_tipo_pessoa = tipo_pessoa
    person_1.no_pessoa = key_1
    person_1.st_ativo = 1
    person_1.dt_cadastro = datetime.datetime.now()
    person_1.nu_cpf = key_1
    person_1.save()

    person_2 = models_ga.TbPessoa()
    person_2.co_tipo_pessoa = tipo_pessoa
    person_2.no_pessoa = key_2
    person_2.st_ativo = 1
    person_2.dt_cadastro = datetime.datetime.now()
    person_2.nu_cpf = key_2
    person_2.save()

    received_1 = get_object_or_404(models_ga.TbPessoa, nu_cpf = key_1)
    received_2 = get_object_or_404(models_ga.TbPessoa, nu_cpf = key_2)

    assert received_1.nu_cpf == key_1
    assert received_2.nu_cpf == key_2


@pytest.mark.django_db
def test_eq():

    eq = equipment.get_equipment_from_ip()

    assert True
