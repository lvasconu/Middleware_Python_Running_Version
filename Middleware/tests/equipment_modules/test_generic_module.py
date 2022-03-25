from datetime import datetime
from time import sleep

from equipment_modules import generic_module, comm5, wolpac

IP_1 = 'XXX.XXX.XXX.1'

m = generic_module.GenericModule(IP_1)

m.number_of_IOs = 10
m.__init__(IP_1)

''' Testing block_equipment() and unblock_equipment().
    Other escape route methods are in separeted file.
'''
def test_01_block_unblock_equipment():

    received_data_0 = m.blocked_by_route[0]
    received_data_1 = m.block_equipment()
    received_data_2 = m.blocked_by_route[0]
    received_data_3 = m.unblock_equipment()
    received_data_4 = m.blocked_by_route[0]

    received_data = (received_data_0, received_data_1, received_data_2, received_data_3, received_data_4)

    expected_data = (None, True, True, True, None)

    assert received_data == expected_data

def test_02_block_unblock_equipment_3():

    relay_number = 3

    received_data_0 = m.blocked_by_route[relay_number]
    received_data_1 = m.block_equipment(relay_number)
    received_data_2 = m.blocked_by_route[relay_number]
    received_data_3 = m.unblock_equipment(relay_number)
    received_data_4 = m.blocked_by_route[relay_number]

    received_data = (received_data_0, received_data_1, received_data_2, received_data_3, received_data_4)

    expected_data = (None, True, True, True, None)

    assert received_data == expected_data

def test_03_block_unblock_equipment_4_152():

    relay_number = 4
    route = 152
    
    received_data_0 = m.blocked_by_route[relay_number]
    received_data_1 = m.block_equipment(relay_number, route)
    received_data_2 = m.blocked_by_route[relay_number]
    received_data_3 = m.unblock_equipment(relay_number, route)
    received_data_4 = m.blocked_by_route[relay_number]

    received_data = (received_data_0, received_data_1, received_data_2, received_data_3, received_data_4)
    
    expected_data = (None, True, route, True, None)

    assert received_data == expected_data

def test_04_block_equipment_5_152_153():

    relay_number = 5
    route_1 = 152
    route_2 = 153
    
    received_data_0 = m.blocked_by_route[relay_number]
    received_data_1 = m.block_equipment(relay_number,route_1)
    received_data_2 = m.blocked_by_route[relay_number]
    received_data_3 = m.block_equipment(relay_number,route_2)
    received_data_4 = m.blocked_by_route[relay_number]
    received_data_5 = m.unblock_equipment(relay_number, route_1)
    received_data_6 = m.blocked_by_route[relay_number]


    received_data = (received_data_0, received_data_1, received_data_2, received_data_3, received_data_4, received_data_5, received_data_6)
    
    expected_data = (None, True, route_1, False, route_1, True, None)

    assert received_data == expected_data

def test_05_unblock_equipment_8_152_153():

    relay_number = 8
    route_1 = 152
    route_2 = 153
    
    received_data_0 = m.blocked_by_route[relay_number]
    received_data_1 = m.block_equipment(relay_number,route_1)
    received_data_2 = m.blocked_by_route[relay_number]
    received_data_3 = m.unblock_equipment(relay_number,route_2)
    received_data_4 = m.blocked_by_route[relay_number]
    received_data_5 = m.unblock_equipment(relay_number, route_1)
    received_data_6 = m.blocked_by_route[relay_number]

    received_data = (received_data_0, received_data_1, received_data_2, received_data_3, received_data_4, received_data_5, received_data_6)
    
    expected_data = (None, True, route_1, False, route_1, True, None)

    assert received_data == expected_data

def test_08_block_equipment_error_152():

    relay_number = 'adasads'
    route = 152
    
    received_data_1, received_data_2 = m.block_equipment(relay_number,route)

    received_data = (received_data_1, received_data_2)

    expected_data = (None, f"Error in method GenericModule.block_equipment. From: IP: {IP_1}, relay: adasads, escape route: 152. Error message: invalid literal for int() with base 10: 'adasads'")

    assert received_data == expected_data

def test_09_unblock_equipment_error_152():

    relay_number = 'adasads'
    route = 152
    
    received_data_1, received_data_2 = m.unblock_equipment(relay_number,route)

    received_data = (received_data_1, received_data_2)

    expected_data = (None, f"Error in method GenericModule.unblock_equipment. From: IP: {IP_1}, relay: adasads, escape route: 152. Error message: invalid literal for int() with base 10: 'adasads'")

    assert received_data == expected_data

''' Testing relay methods - set_relay() and reset_relay(). '''
def test_11_set_reset_NO_relay():

    relay_number = 2
    m.relay_type[relay_number] = 'anything'

    received_data_0 = m.relay_status[relay_number]
    received_data_1, received_data_2 = m.set_relay(relay_number)
    received_data_3 = m.relay_status[relay_number]
    received_data_4, received_data_5 = m.reset_relay(relay_number)
    received_data_6 = m.relay_status[relay_number]

    received_data = (received_data_0, received_data_1, received_data_2, received_data_3, received_data_4, received_data_5, received_data_6)

    expected_data = ('Reset', True, 'NO', 'Set', True, 'NO',  'Reset')
    
    assert received_data == expected_data
    
def test_12_set_reset_NC_relay():

    relay_number = 2
    m.relay_type[relay_number] = 'NC'

    received_data_0 = m.relay_status[relay_number]
    received_data_1, received_data_2 = m.set_relay(relay_number)
    received_data_3 = m.relay_status[relay_number]
    received_data_4, received_data_5 = m.reset_relay(relay_number)
    received_data_6 = m.relay_status[relay_number]

    received_data = (received_data_0, received_data_1, received_data_2, received_data_3, received_data_4, received_data_5, received_data_6)

    expected_data = ('Reset', True, 'NC', 'Set', True, 'NC',  'Reset')
    
    assert received_data == expected_data

def test_13_set_reset_relay_blocked():

    relay_number = 2
    route = 15

    m.relay_type[relay_number] = 'NO'

    received_data_1 = m.block_equipment(relay_number, route)

    received_data_2 = m.set_relay(relay_number)
    received_data_3 = m.reset_relay(relay_number)

    received_data_4 = m.unblock_equipment(relay_number, route)

    received_data_5 = m.set_relay(relay_number)
    received_data_6 = m.relay_status[relay_number]
    received_data_7 = m.reset_relay(relay_number)
    received_data_8 = m.relay_status[relay_number]

    received_data = (received_data_1,
                     received_data_2, received_data_3,
                     received_data_4,
                     received_data_5, received_data_6,
                     received_data_7, received_data_8,
                     )

    expected_data = (True,
                     False, False,
                     True,
                     (True, 'NO'), 'Set',
                     (True, 'NO'), 'Reset')
    
    assert received_data == expected_data

def test_18_set_relay_error():

    received_data = m.set_relay('adasads')

    expected_data = (None, "Error in method GenericModule.set_relay. From: IP: XXX.XXX.XXX.1, relay: adasads. Error message: invalid literal for int() with base 10: 'adasads'")
    
    assert received_data == expected_data

def test_19_reset_relay_error():

    received_data = m.reset_relay('adasads')

    expected_data = (None, f"Error in method GenericModule.reset_relay. From: IP: {IP_1}, relay: adasads. Error message: invalid literal for int() with base 10: 'adasads'")
    
    assert received_data == expected_data

''' Testing relay methods - change_relay_status()'''
def test_21_change_relay_status():

    relay_number = 2

    m.reset_relay(relay_number)

    received_data_1 = m.relay_status[relay_number]
    received_data_2 = m.change_relay_status(relay_number)
    received_data_3 = m.relay_status[relay_number]
    received_data_4 = m.change_relay_status(relay_number)
    received_data_5 = m.relay_status[relay_number]

    received_data = (received_data_1,
                     received_data_2,
                     received_data_3,
                     received_data_4,
                     received_data_5,
                     )

    expected_data = ('Reset',
                     (True, 'Set'),
                     'Set',
                     (True, 'Reset'),
                     'Reset')
    
    assert received_data == expected_data

def test_21_change_relay_status_error():

    relay_number = 'adasads'

    m.reset_relay(relay_number)

    received_data_1, received_data_2 = m.change_relay_status(relay_number)

    received_data = (received_data_1, received_data_2)

    expected_data = (None, f"Error in method GenericModule.change_relay_status. From: IP: {IP_1}, relay: adasads. Error message: invalid literal for int() with base 10: 'adasads'")
    
    assert received_data == expected_data

'''Testing relay methods - set_relay_temporarily() '''

def test_31_set_relay_temporarily():

    relay_number = 0
    sleep_time_default = 3

    received_data_0 = m.relay_status[relay_number]

    start = datetime.now()
    received_data_1, received_data_2 =  m.set_relay_temporarily()
    stop = datetime.now()
    received_data_3 = (stop - start).seconds

    received_data_4 = m.relay_status[relay_number]

    received_data = (received_data_0, received_data_1, received_data_2, received_data_3, received_data_4)

    expected_data = ('Reset', True, 'sleep_time in (None or False)', sleep_time_default, 'Reset')

    assert received_data == expected_data

def test_32_set_relay_temporarily_2():

    relay_number = 2
    sleep_time_default = 3

    received_data_0 = m.relay_status[relay_number]

    start = datetime.now()
    received_data_1, received_data_2 =  m.set_relay_temporarily(relay_number)
    stop = datetime.now()
    received_data_3 = (stop - start).seconds

    received_data_4 = m.relay_status[relay_number]

    received_data = (received_data_0, received_data_1, received_data_2, received_data_3, received_data_4)

    expected_data = ('Reset', True, 'sleep_time in (None or False)', sleep_time_default, 'Reset')

    assert received_data == expected_data

def test_33_set_relay_temporarily_2_5():

    relay_number = 2
    sleep_time = 5

    received_data_0 = m.relay_status[relay_number]

    start = datetime.now()
    received_data_1, received_data_2 =  m.set_relay_temporarily(relay_number, sleep_time)
    stop = datetime.now()
    received_data_3 = (stop - start).seconds

    received_data_4 = m.relay_status[relay_number]

    received_data = (received_data_0, received_data_1, received_data_2, received_data_3, received_data_4)

    expected_data = ('Reset', True, None, sleep_time, 'Reset')

    assert received_data == expected_data

def test_34_set_relay_temporarily_2_error_string():

    relay_number = 2
    sleep_time = 'adasads'
    sleep_time_default = 3

    received_data_0 = m.relay_status[relay_number]

    start = datetime.now()
    received_data_1, received_data_2 =  m.set_relay_temporarily(relay_number, sleep_time)
    stop = datetime.now()
    received_data_3 = (stop - start).seconds

    received_data_4 = m.relay_status[relay_number]

    received_data = (received_data_0, received_data_1, received_data_2, received_data_3, received_data_4)

    expected_data = ('Reset',
                     True,
                     f"Error in method GenericModule.set_relay_temporarily. From IP: {IP_1}, IO #: {relay_number}, sleep_time: {sleep_time}. Error message: could not convert string to float: 'adasads'",
                     sleep_time_default,
                     'Reset')

    assert received_data == expected_data

def test_35_set_relay_temporarily_2_error_None():

    relay_number = 2
    sleep_time = None
    sleep_time_default = 3

    received_data_0 = m.relay_status[relay_number]

    start = datetime.now()
    received_data_1, received_data_2 =  m.set_relay_temporarily(relay_number, sleep_time)
    stop = datetime.now()
    received_data_3 = (stop - start).seconds

    received_data_4 = m.relay_status[relay_number]

    received_data = (received_data_0, received_data_1, received_data_2, received_data_3, received_data_4)

    expected_data = ('Reset',
                     True,
                     'sleep_time in (None or False)' ,
                     sleep_time_default,
                     'Reset')

    assert received_data == expected_data

def test_36_set_relay_temporarily_2_error_False():

    relay_number = 2
    sleep_time = False
    sleep_time_default = 3

    received_data_0 = m.relay_status[relay_number]

    start = datetime.now()
    received_data_1, received_data_2 =  m.set_relay_temporarily(relay_number, sleep_time)
    stop = datetime.now()
    received_data_3 = (stop - start).seconds

    received_data_4 = m.relay_status[relay_number]

    received_data = (received_data_0, received_data_1, received_data_2, received_data_3, received_data_4)

    expected_data = ('Reset',
                     True,
                     'sleep_time in (None or False)' ,
                     sleep_time_default,
                     'Reset')

    assert received_data == expected_data

'''Testing relay methods - set and reset reset_relay_accordingly_to_inputs() '''

def test_41_set_reset_relay_accordingly_to_inputs_blocked():

    relay_number = 2
    route_number = 155

    m.block_equipment(relay_number, route_number)

    received_data_1, received_data_2 =  m.set_relay_accordingly_to_inputs(relay_number)
    received_data_3, received_data_4 =  m.reset_relay_accordingly_to_inputs(relay_number)

    m.unblock_equipment(relay_number, route_number)

    received_data = (received_data_1, received_data_2, received_data_3, received_data_4)

    expected_data = (
                     False,
                     route_number,
                     False,
                     route_number,
                     )

    assert received_data == expected_data

def test_42_set_reset_relay_accordingly_to_inputs_mirror():

    relay_number = 2
    m.relay_timing[relay_number] = 'mirror'

    received_data_0 = m.relay_status[relay_number]

    received_data_1 = m.set_relay_accordingly_to_inputs(relay_number)

    received_data_2 = m.relay_status[relay_number]

    received_data_3 = m.reset_relay_accordingly_to_inputs(relay_number)

    received_data_4 = m.relay_status[relay_number]

    received_data = (received_data_0, received_data_1, received_data_2, received_data_3, received_data_4)

    expected_data = (
                     'Reset',
                     (True, 'relay was set'),
                     'Set',
                     (True, 'relay was reset'),
                     'Reset',
                     )

    assert received_data == expected_data

def test_43_set_reset_relay_accordingly_to_inputs_MIRROR():

    relay_number = 2
    m.relay_timing[relay_number] = 'MIRROR'

    received_data_0 = m.relay_status[relay_number]

    received_data_1 = m.set_relay_accordingly_to_inputs(relay_number)

    received_data_2 = m.relay_status[relay_number]

    received_data_3 = m.reset_relay_accordingly_to_inputs(relay_number)

    received_data_4 = m.relay_status[relay_number]

    received_data = (received_data_0, received_data_1, received_data_2, received_data_3, received_data_4)

    expected_data = (
                     'Reset',
                     (True, 'relay was set'),
                     'Set',
                     (True, 'relay was reset'),
                     'Reset',
                     )

    assert received_data == expected_data

def test_44_set_reset_relay_accordingly_to_inputs_fixed():

    relay_number = 2
    m.relay_timing[relay_number] = 'fixed'

    received_data_0 = m.relay_status[relay_number]

    # Set
    received_data_1 = m.set_relay_accordingly_to_inputs(relay_number)

    received_data_2 = m.relay_status[relay_number]

    received_data_3 = m.set_relay_accordingly_to_inputs(relay_number)

    received_data_4 = m.relay_status[relay_number]

    # Reset
    received_data_5 = m.reset_relay_accordingly_to_inputs(relay_number)

    received_data_6 = m.relay_status[relay_number]
    
    received_data_7 = m.reset_relay_accordingly_to_inputs(relay_number)

    received_data_8 = m.relay_status[relay_number]



    received_data = (received_data_0,
                     received_data_1, received_data_2, received_data_3, received_data_4,
                     received_data_5, received_data_6, received_data_7, received_data_8
                     )

    expected_data = (
                     'Reset',
                     (True, 'relay changed status'),
                     'Set',
                     (True, 'relay changed status'),
                     'Reset',
                     (True, 'Relay is fixed. Did nothing.'),
                     'Reset',
                     (True, 'Relay is fixed. Did nothing.'),
                     'Reset',
                     )

    assert received_data == expected_data

def test_45_set_reset_relay_accordingly_to_inputs_FIXED():

    relay_number = 2
    m.relay_timing[relay_number] = 'FIXED'

    received_data_0 = m.relay_status[relay_number]

    # Set
    received_data_1 = m.set_relay_accordingly_to_inputs(relay_number)

    received_data_2 = m.relay_status[relay_number]

    received_data_3 = m.set_relay_accordingly_to_inputs(relay_number)

    received_data_4 = m.relay_status[relay_number]

    # Reset
    received_data_5 = m.reset_relay_accordingly_to_inputs(relay_number)

    received_data_6 = m.relay_status[relay_number]
    
    received_data_7 = m.reset_relay_accordingly_to_inputs(relay_number)

    received_data_8 = m.relay_status[relay_number]



    received_data = (received_data_0,
                     received_data_1, received_data_2, received_data_3, received_data_4,
                     received_data_5, received_data_6, received_data_7, received_data_8
                     )

    expected_data = (
                     'Reset',
                     (True, 'relay changed status'),
                     'Set',
                     (True, 'relay changed status'),
                     'Reset',
                     (True, 'Relay is fixed. Did nothing.'),
                     'Reset',
                     (True, 'Relay is fixed. Did nothing.'),
                     'Reset',
                     )

    assert received_data == expected_data

def test_46_set_reset_relay_accordingly_to_inputs_temporary():

    relay_number = 2
    m.relay_timing[relay_number] = False

    received_data_0 = m.relay_status[relay_number]

    # Set
    received_data_1 = m.set_relay_accordingly_to_inputs(relay_number)

    sleep(.1)
    
    received_data_2 = m.relay_status[relay_number]

    sleep(m.sleep_time_default)

    received_data_3 = m.relay_status[relay_number]


    # Reset
    received_data_4 = m.reset_relay_accordingly_to_inputs(relay_number)

    
    received_data = (received_data_0,
                     received_data_1, received_data_2, received_data_3, received_data_4,
                     )

    expected_data = (
                     'Reset',
                     (True, 'relay was set temporarily'),
                     'Set',
                     'Reset',

                     (True, 'Relay is temporary. Did nothing.'),
                     )

    assert received_data == expected_data

def test_49_set_relay_accordingly_to_inputs_error():

    relay_number = 'adasads'

    received_data_1, received_data_2 =  m.set_relay_accordingly_to_inputs(relay_number)
    received_data_3, received_data_4 =  m.reset_relay_accordingly_to_inputs(relay_number)

    received_data = (received_data_1, received_data_2, received_data_3, received_data_4)

    expected_data = (
                     None,
                     f"Error in method GenericModule.set_relay_accordingly_to_inputs. From: IP: {IP_1}, relay: {relay_number}. Error message: invalid literal for int() with base 10: '{relay_number}'",
                     None,
                     f"Error in method GenericModule.reset_relay_accordingly_to_inputs. From: IP: {IP_1}, relay: {relay_number}. Error message: invalid literal for int() with base 10: '{relay_number}'",
                     )

    assert received_data == expected_data

'''Testing relay methods - set and reset relays_local_and_remote() '''

def test_501_set_reset_relays_local_and_remote_None():

    nu_input = 2

    received_data_1 =  m.set_relays_local_and_remote(nu_input)
    received_data_2 =  m.reset_relays_local_and_remote(nu_input)

    received_data = (received_data_1, received_data_2)

    expected_data = (
                     (False, f'set: input_addresses[{nu_input}] is None'),
                     (False, f'reset: input_addresses[{nu_input}] is None'),
                     )

    assert received_data == expected_data

def test_502_set_reset_relays_local_and_remote_0():

    nu_input = 2
    m.input_addresses[nu_input] = '0'

    received_data_1 =  m.set_relays_local_and_remote(nu_input)
    received_data_2 =  m.reset_relays_local_and_remote(nu_input)

    received_data = (received_data_1, received_data_2)

    expected_data = (
                     (False, f'set: input_addresses[{nu_input}] is 0'),
                     (False, f'reset: input_addresses[{nu_input}] is 0'),
                     )

    assert received_data == expected_data

def test_503_set_reset_relays_local_and_remote_self():

    nu_input = 2

    m.input_addresses[nu_input] = ''
    received_data_1 =  m.set_relays_local_and_remote(nu_input)
    m.input_addresses[nu_input] = '1'
    received_data_2 =  m.set_relays_local_and_remote(nu_input)
    m.input_addresses[nu_input] = 'self'
    received_data_3 =  m.set_relays_local_and_remote(nu_input)
    m.input_addresses[nu_input] = 'SELF'
    received_data_4 =  m.set_relays_local_and_remote(nu_input)
    m.input_addresses[nu_input] = 'sElF'
    received_data_5 =  m.set_relays_local_and_remote(nu_input)

    m.input_addresses[nu_input] = ''
    received_data_6 =  m.reset_relays_local_and_remote(nu_input)
    m.input_addresses[nu_input] = '1'
    received_data_7 =  m.reset_relays_local_and_remote(nu_input)
    m.input_addresses[nu_input] = 'self'
    received_data_8 =  m.reset_relays_local_and_remote(nu_input)
    m.input_addresses[nu_input] = 'SELF'
    received_data_9 =  m.reset_relays_local_and_remote(nu_input)
    m.input_addresses[nu_input] = 'sElF'
    received_data_10 =  m.reset_relays_local_and_remote(nu_input)

    received_data = (
                     received_data_1, received_data_2, received_data_3, received_data_4, received_data_5, 
                     received_data_6, received_data_7, received_data_8, received_data_9, received_data_10,
                     )

    expected_data = (
                     (True, f'set: input_addresses[{nu_input}] is self'),
                     (True, f'set: input_addresses[{nu_input}] is self'),
                     (True, f'set: input_addresses[{nu_input}] is self'),
                     (True, f'set: input_addresses[{nu_input}] is self'),
                     (True, f'set: input_addresses[{nu_input}] is self'),
                     (True, f'reset: input_addresses[{nu_input}] is self'),
                     (True, f'reset: input_addresses[{nu_input}] is self'),
                     (True, f'reset: input_addresses[{nu_input}] is self'),
                     (True, f'reset: input_addresses[{nu_input}] is self'),
                     (True, f'reset: input_addresses[{nu_input}] is self'),
                     )

    assert received_data == expected_data

def test_504_set_reset_relays_local_and_remote_all():

    nu_input = 2

    m.input_addresses[nu_input] = 'all'
    received_data_1 =  m.set_relays_local_and_remote(nu_input)
    received_data_4 =  m.reset_relays_local_and_remote(nu_input)

    m.input_addresses[nu_input] = 'ALL'
    received_data_2 =  m.set_relays_local_and_remote(nu_input)
    received_data_5 =  m.reset_relays_local_and_remote(nu_input)

    m.input_addresses[nu_input] = 'aLl'
    received_data_3 =  m.set_relays_local_and_remote(nu_input)
    received_data_6 =  m.reset_relays_local_and_remote(nu_input)

    expected_data = (
                    (True, f'set: input_addresses[{nu_input}] is all'),
                    (True, f'set: input_addresses[{nu_input}] is all'),
                    (True, f'set: input_addresses[{nu_input}] is all'),
                    (True, f'reset: input_addresses[{nu_input}] is all'),
                    (True, f'reset: input_addresses[{nu_input}] is all'),
                    (True, f'reset: input_addresses[{nu_input}] is all'),
                    )

    received_data = (
                     received_data_1, received_data_2, received_data_3, 
                     received_data_4, received_data_5, received_data_6, 
                     )

    assert received_data == expected_data

def test_510_set_relays_local_and_remote_remote_one_address_fixed():

    # Variables and objects have to be independent to not interfere with other tests.
    IP_1_510 = 'XXX.XXX.XXX.1_510'
    IP_2_510 = 'XXX.XXX.XXX.2_510'
    IP_3_510 = 'XXX.XXX.XXX.3_510'

    m_510 = generic_module.GenericModule(IP_1_510)
    c_510 = comm5.MA(IP_2_510)
    w_510 = wolpac.Waffer(IP_3_510)

    m_510.number_of_IOs = 10
    m_510.__init__(IP_1_510)

    nu_input = 2

    for r in range(len(m_510.relay_status)):
        m_510.reset_relay(r)                    # Resetting relays.
        m_510.relay_timing[r] = 'FIXED'         # Making relays fixed.

    # Adding modules to module_list. Necessary to set relays remotely.
    m_510.module_list.append(m_510)

    m_510.input_addresses[nu_input] = f'{IP_1_510}:2'

    # Reading initial relay status.
    received_data_1 = m_510.relay_status[:] # [:] indicates to copy values. Without it, objects are the same.

    # Setting relays
    received_data_2 = m_510.set_relays_local_and_remote(nu_input)
    received_data_3 = m_510.relay_status[:]

    # Setting relays
    received_data_4 = m_510.set_relays_local_and_remote(nu_input)
    received_data_5 = m_510.relay_status[:]


    received_data = (
                     received_data_1,
                     received_data_2,
                     received_data_3,
                     received_data_4,
                     received_data_5,
                     )

    expected_data = (
                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    (True, 'set: remotely'),
                    ['Reset', 'Reset', 'Set', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    (True, 'set: remotely'),
                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    )

    assert received_data == expected_data

def test_511_set_reset_relays_local_and_remote_remote_some_addresses_fixed():

    # Variables and objects have to be independent to not interfere with other tests.
    IP_1_511 = 'XXX.XXX.XXX.1_511'
    IP_2_511 = 'XXX.XXX.XXX.2_511'
    IP_3_511 = 'XXX.XXX.XXX.3_511'

    m_511 = generic_module.GenericModule(IP_1_511)
    c_511 = comm5.MA(IP_2_511)
    w_511 = wolpac.Waffer(IP_3_511)

    m_511.number_of_IOs = 10
    m_511.__init__(IP_1_511)

    nu_input = 2

    for r in range(len(m_511.relay_status)):
        m_511.reset_relay(r)                    # Resetting relays.
        m_511.relay_timing[r] = 'fixed'         # Making relays fixed.
    for r in range(len(c_511.relay_status)):
        c_511.reset_relay(r)                    # Resetting relays.
        c_511.relay_timing[r] = 'fixed'         # Making relays fixed.
    for r in range(len(w_511.relay_status)):
        w_511.reset_relay(r)                    # Resetting relays.
        w_511.relay_timing[r] = 'fixed'         # Making relays fixed.

    # Adding modules to module_list. Necessary to set relays remotely.
    m_511.module_list.append(m_511)
    m_511.module_list.append(c_511)
    m_511.module_list.append(w_511)

    m_511.input_addresses[nu_input] = f'{IP_1_511}:2, {IP_2_511}:1, {IP_2_511}:3, {IP_3_511}:0'

    # Reading initial relay status.
    received_data_1_01 = m_511.relay_status[:] # [:] indicates to copy values. Without it, objects are the same.
    received_data_1_02 = c_511.relay_status[:]
    received_data_1_03 = w_511.relay_status[:]

    # Resetting relays
    received_data_2_01 = m_511.reset_relays_local_and_remote(nu_input)
    sleep(.1)

    # Reading relay status.
    received_data_1_04 = m_511.relay_status[:]
    received_data_1_05 = c_511.relay_status[:]
    received_data_1_06 = w_511.relay_status[:]

    # Setting relays
    received_data_2_02 =  m_511.set_relays_local_and_remote(nu_input)
    sleep(.1)

    # Reading relay status.
    received_data_1_07 = m_511.relay_status[:]
    received_data_1_08 = c_511.relay_status[:]
    received_data_1_09 = w_511.relay_status[:]

    # Resetting relays
    received_data_2_03 = m_511.reset_relays_local_and_remote(nu_input)
    sleep(.1)

    # Reading relay status.
    received_data_1_10 = m_511.relay_status[:]
    received_data_1_11 = c_511.relay_status[:]
    received_data_1_12 = w_511.relay_status[:]

    # Setting relays
    received_data_2_04 = m_511.set_relays_local_and_remote(nu_input)
    sleep(.1)

    # Reading relay status.
    received_data_1_13 = m_511.relay_status[:]
    received_data_1_14 = c_511.relay_status[:]
    received_data_1_15 = w_511.relay_status[:]

    received_data = (
                     received_data_1_01, received_data_1_02, received_data_1_03,
                     received_data_2_01,
                     received_data_1_04, received_data_1_05, received_data_1_06,
                     received_data_2_02,
                     received_data_1_07, received_data_1_08, received_data_1_09,
                     received_data_2_03,
                     received_data_1_10, received_data_1_11, received_data_1_12,
                     received_data_2_04,
                     received_data_1_13, received_data_1_14, received_data_1_15,
                     )

    expected_data = (
                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset'],

                    (True, 'reset: remotely'),

                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset'],

                    (True, 'set: remotely'),

                    ['Reset', 'Reset', 'Set', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset', 'Set', 'Reset', 'Set', 'Reset'],
                    ['Set'],

                    (True, 'reset: remotely'),

                    ['Reset', 'Reset', 'Set', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset', 'Set', 'Reset', 'Set', 'Reset'],
                    ['Set'],

                    (True, 'set: remotely'),

                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset'],
                    )

    assert received_data == expected_data

def test_512_set_reset_relays_local_and_remote_remote_some_addresses_mirror():
    
    # Variables and objects have to be independent to not interfere with other tests.
    IP_1_512 = 'XXX.XXX.XXX.1_512'
    IP_2_512 = 'XXX.XXX.XXX.2_512'
    IP_3_512 = 'XXX.XXX.XXX.3_512'

    m_512 = generic_module.GenericModule(IP_1_512)
    c_512 = comm5.MA(IP_2_512)
    w_512 = wolpac.Waffer(IP_3_512)

    m_512.number_of_IOs = 10
    m_512.__init__(IP_1_512)

    nu_input = 2

    for r in range(len(m_512.relay_status)):
        m_512.reset_relay(r)                    # Resetting relays.
        m_512.relay_timing[r] = 'mirror'         # Making relays fixed.
    for r in range(len(c_512.relay_status)):
        c_512.reset_relay(r)                    # Resetting relays.
        c_512.relay_timing[r] = 'mirror'         # Making relays fixed.
    for r in range(len(w_512.relay_status)):
        w_512.reset_relay(r)                    # Resetting relays.
        w_512.relay_timing[r] = 'mirror'         # Making relays fixed.

    # Adding modules to module_list. Necessary to set relays remotely.
    m_512.module_list.append(m_512)
    m_512.module_list.append(c_512)
    m_512.module_list.append(w_512)

    m_512.input_addresses[nu_input] = f'{IP_1_512}:2, {IP_2_512}:1, {IP_2_512}:3, {IP_3_512}:0'

    # Reading initial relay status.
    received_data_1_01 = m_512.relay_status[:] # [:] indicates to copy values. Without it, objects are the same.
    received_data_1_02 = c_512.relay_status[:]
    received_data_1_03 = w_512.relay_status[:]

    # Resetting relays
    received_data_2_01 = m_512.reset_relays_local_and_remote(nu_input)
    sleep(.1)

    # Reading relay status.
    received_data_1_04 = m_512.relay_status[:]
    received_data_1_05 = c_512.relay_status[:]
    received_data_1_06 = w_512.relay_status[:]

    # Setting relays
    received_data_2_02 =  m_512.set_relays_local_and_remote(nu_input)
    sleep(.1)

    # Reading relay status.
    received_data_1_07 = m_512.relay_status[:]
    received_data_1_08 = c_512.relay_status[:]
    received_data_1_09 = w_512.relay_status[:]

    # Resetting relays
    received_data_2_03 = m_512.reset_relays_local_and_remote(nu_input)
    sleep(.1)

    # Reading relay status.
    received_data_1_10 = m_512.relay_status[:]
    received_data_1_11 = c_512.relay_status[:]
    received_data_1_12 = w_512.relay_status[:]

    # Setting relays
    received_data_2_04 = m_512.set_relays_local_and_remote(nu_input)
    sleep(.1)

    # Reading relay status.
    received_data_1_13 = m_512.relay_status[:]
    received_data_1_14 = c_512.relay_status[:]
    received_data_1_15 = w_512.relay_status[:]

    received_data = (
                     received_data_1_01, received_data_1_02, received_data_1_03,
                     received_data_2_01,
                     received_data_1_04, received_data_1_05, received_data_1_06,
                     received_data_2_02,
                     received_data_1_07, received_data_1_08, received_data_1_09,
                     received_data_2_03,
                     received_data_1_10, received_data_1_11, received_data_1_12,
                     received_data_2_04,
                     received_data_1_13, received_data_1_14, received_data_1_15,
                     )

    expected_data = (
                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset'],

                    (True, 'reset: remotely'),

                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset'],

                    (True, 'set: remotely'),

                    ['Reset', 'Reset', 'Set', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset', 'Set', 'Reset', 'Set', 'Reset'],
                    ['Set'],

                    (True, 'reset: remotely'),

                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset'],

                    (True, 'set: remotely'),

                    ['Reset', 'Reset', 'Set', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset', 'Set', 'Reset', 'Set', 'Reset'],
                    ['Set'],
                    )

    assert received_data == expected_data

def test_513_set_reset_relays_local_and_remote_remote_some_addresses_temporary_1():
    ''' Resets, Sets, Resets
        With time for each command to complete.
    '''

    # Variables and objects have to be independent to not interfere with other tests.
    IP_1_513 = 'XXX.XXX.XXX.1_513'
    IP_2_513 = 'XXX.XXX.XXX.2_513'
    IP_3_513 = 'XXX.XXX.XXX.3_513'

    m_513 = generic_module.GenericModule(IP_1_513)
    c_513 = comm5.MA(IP_2_513)
    w_513 = wolpac.Waffer(IP_3_513)

    m_513.number_of_IOs = 10
    m_513.__init__(IP_1_513)

    nu_input = 2

    for r in range(len(m_513.relay_status)):
        m_513.reset_relay(r)                    # Resetting relays.
    for r in range(len(c_513.relay_status)):
        c_513.reset_relay(r)                    # Resetting relays.
    for r in range(len(w_513.relay_status)):
        w_513.reset_relay(r)                    # Resetting relays.


    # Adding modules to module_list. Necessary to set relays remotely.
    m_513.module_list.append(m_513)
    m_513.module_list.append(c_513)
    m_513.module_list.append(w_513)

    m_513.input_addresses[nu_input] = f'{IP_1_513}:2, {IP_2_513}:1, {IP_2_513}:3, {IP_3_513}:0'

    # Reading initial relay status.
    received_data_1_01 = m_513.relay_status[:] # [:] indicates to copy values. Without it, objects are the same.
    received_data_1_02 = c_513.relay_status[:]
    received_data_1_03 = w_513.relay_status[:]

    # Resetting relays
    received_data_2_01 = m_513.reset_relays_local_and_remote(nu_input)
    
    # Reading relay status.
    sleep(.1)
    received_data_1_04 = m_513.relay_status[:]
    received_data_1_05 = c_513.relay_status[:]
    received_data_1_06 = w_513.relay_status[:]

    # Reading relay status.
    sleep(3)
    received_data_1_07 = m_513.relay_status[:]
    received_data_1_08 = c_513.relay_status[:]
    received_data_1_09 = w_513.relay_status[:]

    # Setting relays
    received_data_2_02 =  m_513.set_relays_local_and_remote(nu_input)
    
    # Reading relay status.
    sleep(.1)
    received_data_1_10 = m_513.relay_status[:]
    received_data_1_11 = c_513.relay_status[:]
    received_data_1_12 = w_513.relay_status[:]

    # Reading relay status.
    sleep(3)
    received_data_1_13 = m_513.relay_status[:]
    received_data_1_14 = c_513.relay_status[:]
    received_data_1_15 = w_513.relay_status[:]

    # Resetting relays
    received_data_2_03 = m_513.reset_relays_local_and_remote(nu_input)
    
    # Reading relay status.
    sleep(.1)
    received_data_1_16 = m_513.relay_status[:]
    received_data_1_17 = c_513.relay_status[:]
    received_data_1_18 = w_513.relay_status[:]

    # Reading relay status.
    sleep(3)
    received_data_1_19 = m_513.relay_status[:]
    received_data_1_20 = c_513.relay_status[:]
    received_data_1_21 = w_513.relay_status[:]

    received_data = (
                     received_data_1_01, received_data_1_02, received_data_1_03,
                     received_data_2_01,
                     received_data_1_04, received_data_1_05, received_data_1_06,
                     received_data_1_07, received_data_1_08, received_data_1_09,
                     received_data_2_02,
                     received_data_1_10, received_data_1_11, received_data_1_12,
                     received_data_1_13, received_data_1_14, received_data_1_15,
                     received_data_2_03,
                     received_data_1_16, received_data_1_17, received_data_1_18,
                     received_data_1_19, received_data_1_20, received_data_1_21,
                     )

    expected_data = (
                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset'],

                    (True, 'reset: remotely'),

                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset'],

                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset'],

                    (True, 'set: remotely'),

                    ['Reset', 'Reset', 'Set', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset', 'Set', 'Reset', 'Set', 'Reset'],
                    ['Set'],

                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset'],

                    (True, 'reset: remotely'),

                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset'],

                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset'],
                    )

    assert received_data == expected_data

def test_514_set_reset_relays_local_and_remote_remote_some_addresses_temporary_2():
    ''' Resets, Sets, Resets
        Without time for set command to complete.
    '''

    # Variables and objects have to be independent to not interfere with other tests.
    IP_1_514 = 'XXX.XXX.XXX.1_514'
    IP_2_514 = 'XXX.XXX.XXX.2_514'
    IP_3_514 = 'XXX.XXX.XXX.3_514'

    m_514 = generic_module.GenericModule(IP_1_514)
    c_514 = comm5.MA(IP_2_514)
    w_514 = wolpac.Waffer(IP_3_514)

    m_514.number_of_IOs = 10
    m_514.__init__(IP_1_514)

    nu_input = 2

    for r in range(len(m_514.relay_status)):
        m_514.reset_relay(r)                    # Resetting relays.
    for r in range(len(c_514.relay_status)):
        c_514.reset_relay(r)                    # Resetting relays.
    for r in range(len(w_514.relay_status)):
        w_514.reset_relay(r)                    # Resetting relays.

    # Adding modules to module_list. Necessary to set relays remotely.
    m_514.module_list.append(m_514)
    m_514.module_list.append(c_514)
    m_514.module_list.append(w_514)

    m_514.input_addresses[nu_input] = f'{IP_1_514}:2, {IP_2_514}:1, {IP_2_514}:3, {IP_3_514}:0'

    # Reading initial relay status.
    received_data_1_01 = m_514.relay_status[:] # [:] indicates to copy values. Without it, objects are the same.
    received_data_1_02 = c_514.relay_status[:]
    received_data_1_03 = w_514.relay_status[:]

    # Setting relays
    received_data_2_01 =  m_514.set_relays_local_and_remote(nu_input)
    
    # Reading relay status.
    sleep(.1)
    received_data_1_04 = m_514.relay_status[:]
    received_data_1_05 = c_514.relay_status[:]
    received_data_1_06 = w_514.relay_status[:]

    # Resetting relays
    received_data_2_02 = m_514.reset_relays_local_and_remote(nu_input)
    
    # Reading relay status.
    sleep(.1)
    received_data_1_07 = m_514.relay_status[:]
    received_data_1_08 = c_514.relay_status[:]
    received_data_1_09 = w_514.relay_status[:]

    # Reading relay status.
    sleep(3)
    received_data_1_10 = m_514.relay_status[:]
    received_data_1_11 = c_514.relay_status[:]
    received_data_1_12 = w_514.relay_status[:]

    received_data = (
                     received_data_1_01, received_data_1_02, received_data_1_03,
                     received_data_2_01,
                     received_data_1_04, received_data_1_05, received_data_1_06,
                     received_data_2_02,
                     received_data_1_07, received_data_1_08, received_data_1_09,
                     received_data_1_10, received_data_1_11, received_data_1_12,
                     )

    expected_data = (
                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset'],

                    (True, 'set: remotely'),

                    ['Reset', 'Reset', 'Set', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset', 'Set', 'Reset', 'Set', 'Reset'],
                    ['Set'],

                    (True, 'reset: remotely'),

                    ['Reset', 'Reset', 'Set', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset', 'Set', 'Reset', 'Set', 'Reset'],
                    ['Set'],

                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset', 'Reset', 'Reset', 'Reset', 'Reset'],
                    ['Reset'],
                    )

    assert received_data == expected_data

def test_590_set_reset_relays_local_and_remote_error():

    received_data_1 =  m.set_relays_local_and_remote()
    received_data_2 =  m.reset_relays_local_and_remote()

    expected_data = (received_data_1, received_data_2)

    expected_data = (
                (None, f"Error in method GenericModule.set_relays_local_and_remote. From: IP: {IP_1} input: None, To: IP: None relay: None. Error message: int() argument must be a string, a bytes-like object or a number, not 'NoneType'"),
                (None, f"Error in method GenericModule.reset_relays_local_and_remote. From: IP: {IP_1} input: None, To: IP: None relay: None. Error message: int() argument must be a string, a bytes-like object or a number, not 'NoneType'")
                )

    received_data = (received_data_1, received_data_2)

    assert received_data == expected_data

if __name__ == "__main__":
    pass
