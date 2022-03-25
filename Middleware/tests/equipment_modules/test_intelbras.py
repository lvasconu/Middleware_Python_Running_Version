from datetime import datetime, timedelta

from equipment_modules import intelbras

# To run, open cmd in folder and type:
    # All tests: pytest -v --durations=0
    # Specific test: pytest -v --durations=0 -k "method name"
    # Ref: https://docs.pytest.org/en/latest/usage.html

IP_1 = '192.168.0.205'
username = 'admin'
password = 'G@coin1000'

m = intelbras.SS7520FaceT(IP_1, username, password)

# Person methods:
def test_01_1_person_create():

    person_number = 'person_number_01'
    person_name = 'person_name_01'
    card_number = 'card_number_01'

    response = m.person_create(person_number, person_name, card_number)
    received_data_1 = response.status_code

    # Reverting:
    records_found, record_info = m.person_find_by_person_number(person_number)
    received_data_2 = m.person_delete_by_recno(record_info['RecNo'])

    received_data = (received_data_1, records_found, received_data_2)
    expected_data = (200, 1, True)

    assert received_data == expected_data

def test_01_2_person_create_existing():

    person_number = 'person_number_02'
    person_name = 'person_name_02'
    card_number = 'card_number_02'

    response_1 = m.person_create(person_number, person_name, card_number)
    response_2 = m.person_create(person_number, person_name, card_number)

    received_data_1 = response_1.status_code
    received_data_2 = response_2.status_code

    # Reverting:
    records_found, record_info = m.person_find_by_person_number(person_number)
    received_data_3 = m.person_delete_by_recno(record_info['RecNo'])

    received_data = (received_data_1, received_data_2, records_found, received_data_3)
    expected_data = (200, 400, 1, True)

    assert received_data == expected_data

def test_02_1_person_find_by_person_number():

    person_number = 'person_number_03'
    person_name = 'person_name_03'
    card_number = 'card_number_03'

    response = m.person_create(person_number, person_name, card_number)
    received_data_1 = response.status_code

    records_found, record_info = m.person_find_by_person_number(person_number)
    
    # Comparing how many itens dictionaries have in common (RecNo) will not be the same. Ref: https://stackoverflow.com/questions/4527942/comparing-two-dictionaries-and-checking-how-many-key-value-pairs-are-equal
    expected_data_2 = {'CardName': person_name, 'CardNo': card_number, 'CardStatus': '0', 'CardType': '0', 'CitizenIDNo': '', 'DynamicCheckCode': '', 'FirstEnter': 'false', 'Handicap': 'false', 'IsValid': 'false', 'Password': '', 'RecNo': '8', 'RepeatEnterRouteTimeout': '4294967295', 'UseTime': '0', 'UserID': person_number, 'UserType': '0', 'VTOPosition': '', 'ValidDateEnd': '', 'ValidDateStart': ''}
    shared_items = {k: record_info[k] for k in record_info if k in expected_data_2 and record_info[k] == expected_data_2[k]}

    # Reverting:
    received_data_3 = m.person_delete_by_recno(record_info['RecNo'])

    received_data = (received_data_1, records_found, len(shared_items), received_data_3)
    expected_data = (200, 1, 17, True)

    assert received_data == expected_data

def test_02_2_person_find_by_person_number_not_existing():

    records_found, record_info = m.person_find_by_person_number('akljsdkasdh')
    received_data = (records_found, record_info)

    expected_data = (0, [])

    assert received_data == expected_data

def test_03_1_person_get_all():

     records_found, record_list = m.person_get_all()

     assert isinstance(records_found, int)

def test_03_2_person_get_with_limit():

     records_found, record_list = m.person_get_all(limit = 2)

     assert isinstance(records_found, int)

def test_04_person_delete_by_recno():

    person_number = 'person_number_06'
    person_name = 'person_name_06'
    card_number = 'card_number_06'

    response = m.person_create(person_number, person_name, card_number)
    received_data_1 = response.status_code

    records_found, record_info = m.person_find_by_person_number(person_number)

    received_data_3 = m.person_delete_by_recno(record_info['RecNo'])

    expected_data = True

    received_data = (received_data_1, records_found, received_data_3)
    expected_data = (200, 1, True)

    assert received_data == expected_data

def test_05_1_person_delete_by_person_number():

    person_number = 'person_number_07'
    person_name = 'person_name_07'
    card_number = 'card_number_07'

    response = m.person_create(person_number, person_name, card_number)
    received_data_1 = response.status_code

    received_data_2 = m.person_delete_by_person_number(person_number)

    received_data = (received_data_1, received_data_2)
    expected_data = (200, True)

    assert received_data == expected_data

def test_05_2_person_delete_by_person_number_not_found():

    person_number = 'person_number_08'

    received_data = m.person_delete_by_person_number(person_number)

    expected_data = None

    assert received_data == expected_data

# Time methods:
def test_51_1_time_set_and_get_current():

    received_data_1 = m.time_set()
    received_data_2 = m.time_get()

    received_data = received_data_1 + received_data_2

    now_1 = datetime.now()                  # Now
    now_2 = now_1 - timedelta(seconds=1)    # One second before

    # Due to delays, get can be one second after set.
    expected_data_1 = (200, ['OK'], 200, now_1.strftime('%Y-%m-%d %H:%M:%S'))
    expected_data_2 = (200, ['OK'], 200, now_2.strftime('%Y-%m-%d %H:%M:%S'))

    assert (received_data == expected_data_1) or (received_data == expected_data_2)

def test_51_2_time_set_and_get_specific():

    test_time = '2014-02-07 14:00:32'

    received_data_1 = m.time_set(time = test_time)
    received_data_2 = m.time_get()

    expected_data = (200, ['OK'], 200, test_time)

    # Returning to current time:
    m.time_set()

    assert received_data_1 + received_data_2 == expected_data

def test_51_3_time_set_error():

    received_data = m.time_set(time = 'blah')

    expected_data = (400, ['Error', 'Bad Request!'])

    assert received_data == expected_data

# Configuration methods - Mask:

    # 0: do not detect mask
def test_61_0_config_mask_mode():

    received_data = m.config_mask_mode(0)

    expected_data = (200, ['OK'])

    assert received_data == expected_data

    # 1: mask prompt
def test_61_1_config_mask_mode():

    received_data = m.config_mask_mode(1)

    expected_data = (200, ['OK'])

    assert received_data == expected_data

    # 2: mask intercept
def test_61_2_config_mask_mode():

    received_data = m.config_mask_mode(2)

    expected_data = (200, ['OK'])

    assert received_data == expected_data

# Configuration methods - Temperature only:
def test_62_1_config_temperature_only_true():

    received_data = m.config_temperature_only(True)

    expected_data = (200, ['OK'])

    assert received_data == expected_data

def test_62_2_config_temperature_only_false():

    received_data = m.config_temperature_only(False)

    expected_data = (200, ['OK'])

    assert received_data == expected_data


def test_62_3_config_temperature_only_error():

    received_data = m.config_temperature_only(55)

    expected_data = (200, ['Error'])

    assert received_data == expected_data