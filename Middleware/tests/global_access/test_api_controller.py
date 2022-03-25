from global_access.api_controller import ApiController

# To run, open cmd in folder and type:
    # All tests: pytest -v --durations=0
    # Specific test: pytest -v --durations=0 -k "method name"
    # Ref: https://docs.pytest.org/en/latest/usage.html

api = ApiController()

# Methods that run on each equipment module connection:

    # Method get_eqpt_parameters

def test_01_get_eqpt_valid():

    ip = '10.19.0.101'

    received_data = api.get_eqpt_parameters(ip)

    expected_data = (5,
                    {"CONVERSAO_DE_IDENTIFICADOR":"1","TIPO_ACESSO_LEITOR3":"3","TIPO_ACESSO_LEITOR2":"2","TIPO_ACESSO_LEITOR1":"1","TAMANHO_BUFFER":"256","TIMEOUT_ACESSO":"60","ID":"0","IP":"10.19.0.101"},
                    f'Equipment parameters identified for IP: {ip}')

    assert received_data == expected_data

def test_02_get_eqpt_invalid():

    ip = 'dasdasdas'

    received_data = api.get_eqpt_parameters(ip)

    expected_data = None, None, f'IP not found by ApiController.get_eqpt_parameters. IP: {ip}. Try {api.max_try}/{api.max_try}.'

    assert received_data == expected_data

def test_03_get_eqpt_parameters_error():

    ip = '10.19.80.51'
    
    # Storing original value.
    max_try_aux = api.max_try
    # Changing value for test.   
    api.max_try = ''
    err = "'<=' not supported between instances of 'int' and 'str'"

    received_data = api.get_eqpt_parameters(ip)

    expected_data = None, None, f'Error in ApiController.get_eqpt_parameters. '+\
                                f'Error message: {err}. ' +\
                                f'IP: {ip}.'

    # Restoring original value.
    api.max_try = max_try_aux

    assert received_data == expected_data

def test_04_get_eqpt_parameters_none():

    ip = '10.19.80.51'
    
    # Storing original value.
    max_try_aux = api.max_try
    # Changing value for test.   
    api.max_try = 0

    received_data = api.get_eqpt_parameters(ip)

    expected_data = None, None, None

    # Restoring original value.
    api.max_try = max_try_aux

    assert received_data == expected_data

    # Method get_eqpt_parameters_by_IP_port

def test_11_get_eqpt_parameters_by_IP_port_valid():

    ip = '10.19.80.51'
    originalPort = 5001

    received_data = api.get_eqpt_parameters_by_IP_port(ip, originalPort)

    expected_data = 129, 1, 1, f'Identified connection. Equipment: 129 (IP: {ip}, relay: 1, port: {originalPort})'

    assert received_data == expected_data

def test_12_get_eqpt_parameters_by_IP_port_invalid():

    ip = 'dlkasndlksa'
    originalPort = 5001

    received_data = api.get_eqpt_parameters_by_IP_port(ip, originalPort)

    expected_data = None, None, None, f'Equipment not found in method ApiController.get_eqpt_parameters_by_IP_port. IP: {ip}, port: {originalPort}'

    assert received_data == expected_data

def test_13_get_eqpt_parameters_by_IP_port_error():

    ip = '10.19.80.51'
    originalPort = 5001
    
    # Storing original value.
    max_try_aux = api.max_try
    # Changing value for test.   
    api.max_try = ''
    err = "'<=' not supported between instances of 'int' and 'str'"

    received_data = api.get_eqpt_parameters_by_IP_port(ip, originalPort)

    expected_data = None, None, None,   f'Error in ApiController.get_eqpt_parameters_by_IP_port. '+\
                                        f'Error message: {err}. ' +\
                                        f'IP: {ip}, port: {originalPort}.'


    # Restoring original value.
    api.max_try = max_try_aux

    assert received_data == expected_data

def test_14_get_eqpt_parameters_by_IP_port_none():

    ip = '10.19.80.51'
    originalPort = 5001
    
    # Storing original value.
    max_try_aux = api.max_try
    # Changing value for test.   
    api.max_try = 0

    received_data = api.get_eqpt_parameters_by_IP_port(ip, originalPort)

    expected_data = None, None, None, None

    # Restoring original value.
    api.max_try = max_try_aux

    assert received_data == expected_data

    # method get_eqpt_parameters_by_IP_relay

def test_21_get_eqpt_parameters_by_IP_relay_valid():

    ip = '10.19.80.51'
    nu_IO = 1

    received_data = api.get_eqpt_parameters_by_IP_relay(ip, nu_IO)

    expected_data = 129, 'NO', '.5', '1', f'IO parameters identified for IP: {ip}, nu_IO: {nu_IO}'

    assert received_data == expected_data

def test_22_get_eqpt_parameters_by_IP_relay_invalid():

    ip = 'adasdas'
    nu_IO = 1

    received_data = api.get_eqpt_parameters_by_IP_relay(ip, nu_IO)

    expected_data = None, None, None, None, f'IP/relay not found by ApiController.get_eqpt_parameters_by_IP_relay. IP: {ip}, Relay: {nu_IO}. Try {api.max_try}/{api.max_try}.'

    assert received_data == expected_data

def test_23_get_eqpt_parameters_by_IP_relay_error():

    ip = '10.19.80.51'
    originalPort = 5001

    # Storing original value.
    max_try_aux = api.max_try
    # Changing value for test.   
    api.max_try = ''
    err = "'<=' not supported between instances of 'int' and 'str'"

    received_data = api.get_eqpt_parameters_by_IP_relay(ip, originalPort)

    expected_data = None, None, None, None, f'Error in ApiController.get_eqpt_parameters_by_IP_relay. '+\
                                            f'Error message: {err}. ' +\
                                            f'IP: {ip}, IO: {originalPort}.'


    # Restoring original value.
    api.max_try = max_try_aux

    assert received_data == expected_data

def test_24_get_eqpt_parameters_by_IP_relay_none():

    ip = '10.19.80.51'
    originalPort = 5001
    
    # Storing original value.
    max_try_aux = api.max_try
    # Changing value for test.   
    api.max_try = 0

    received_data = api.get_eqpt_parameters_by_IP_relay(ip, originalPort)

    expected_data = None, None, None, None, None

    # Restoring original value.
    api.max_try = max_try_aux

    assert received_data == expected_data


# Methods that run on each person access:

access_request_number = 0
access_request_type = 1
access_response_type = 0

def test_31_access_request():

    global access_request_number, access_response_type, access_request_type
    access_request_number, access_response_type = api.access_request('F9136325', 1, access_request_type)

    assert access_response_type in (1, 12)

def test_32_access_register():

    global access_request_number, access_response_type
    received_data = api.access_register(access_request_number, access_request_type, access_response_type)

    expected_data = True

    assert received_data == expected_data

def test_33_get_person_access_info_1_cartao():

    co_solicitacao = 138543
    
    expected_data = {
        "person_number":27476,
        "person_name":"TEREZINHA NUNES DA FONSECA",
        "person_id_cpf":"09641122134",
        "person_id_id":None,
        "person_id_id_agency":"DF",
        "person_id_passport":None,
        "identifier_type":"Crachá",
        "identifier_number":"F66E9A9D",
        "place_name":"2 EAMN CATRACAS - SS, TÉRREO",
        "equipment_number":12,
        "equipment_name":"EAMN 1SS - CATRACA 3",
        "access_request_type":1,
        "access_request_description":"ENTRADA",
        "access_response_type":1,
        "access_response_description":"ENTRADA",
        "access_made_type":1,
        "access_made_description":"ENTRADA"
        }

    received_data = api.get_person_access_info(co_solicitacao)

    assert received_data == expected_data

def test_34_get_person_access_info_2_botao():

    co_solicitacao = 13904515
    
    expected_data = None

    received_data = api.get_person_access_info(co_solicitacao)

    assert received_data == expected_data

def test_35_get_person_access_info_3_invalid_number():

    co_solicitacao = 5645456456464546
    
    expected_data = None

    received_data = api.get_person_access_info(co_solicitacao)

    assert received_data == expected_data

def test_36_get_person_photo():

    received_data = api.get_person_photo(47049)

    expected_data = "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"

    assert received_data == expected_data

def test_39_get_info_and_photo_and_update_dashboad():
    
    assert api.get_info_and_photo_and_update_dashboad


if __name__ == '__main__':
    #test_get_eqpt_by_IP_port()
    pass