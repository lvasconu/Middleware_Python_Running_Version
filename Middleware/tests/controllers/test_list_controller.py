from controllers.list_controller import ListController
from equipment_modules import generic_module, comm5, wolpac

# To run, open cmd in folder and type:
    # All tests: pytest -v --durations=0
    # Specific test: pytest -v --durations=0 -k "method name"
    # Ref: https://docs.pytest.org/en/latest/usage.html

list_controller = ListController()

# Generating modules and equipment numbers.
a = generic_module.GenericModule('10.19.1.1')
b = comm5.MA('10.19.1.2')
c = comm5.MA('10.19.1.3')
d = wolpac.Waffer('10.19.1.3')

a.equipment_number[0] = 45
b.equipment_number[1] = 45
c.equipment_number[2] = 89
d.equipment_number[0] = 1

# Adding to list.
list_controller.append(a)
list_controller.append(b)
list_controller.append(c)
list_controller.append(d)

# Tests:

def test_get_modules_no_param():

    received_data = list_controller.get_modules()

    expected_data = [], []

    assert received_data == expected_data

def test_get_modules_IP_doesnt_exist():

    received_data = list_controller.get_modules(IP = 'dajddas')

    expected_data = [], []

    assert received_data == expected_data

def test_get_modules_IP_one_occurence():

    received_data = list_controller.get_modules(IP = '10.19.1.2')

    expected_data = [b], [0]

    assert received_data == expected_data

def test_get_modules_IP_two_occurences():

    received_data = list_controller.get_modules(IP = '10.19.1.3')

    expected_data = [c, d], [0, 0]

    assert received_data == expected_data

def test_get_modules_number_doesnt_exist():

    received_data = list_controller.get_modules(equipment_number = 'dajddas')

    expected_data = [], []

    assert received_data == expected_data

def test_get_modules_number_one_occurence_1():

    received_data = list_controller.get_modules(89)

    expected_data = [c], [2]

    assert received_data == expected_data

def test_get_modules_number_one_occurence_2():

    received_data = list_controller.get_modules(equipment_number = 89)

    expected_data = [c], [2]

    assert received_data == expected_data

def test_get_modules_number_two_occurences():

    received_data = list_controller.get_modules(45)

    expected_data = [a, b], [0, 1]

    assert received_data == expected_data

def test_get_modules_number_and_IP():

    received_data = list_controller.get_modules(89, '10.19.1.2')

    expected_data = [c], [2]

    assert received_data == expected_data

