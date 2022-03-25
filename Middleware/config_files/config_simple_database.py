""" If using simple solution (not complete Global Access solution), database is this file.

Normal (default) status for each relay of each Comm5.
Parameters must be placed in this order: 
module_parameters = [
     [
     0: IP of Comm5.MA,
     1: [Default status of each relays], accepts:
             NC for normally closed relay.
             NO for normally open relay.
     2: [Default timing for each relay], accepts:
             number (greater than 0): the relay will be Temporary. It will be set for 'number' seconds and then reset. -- Default state.
             'Mirror': When input is 1, the relay will be set and stay set until input receives 0.
             'Fixed':  When input is 1, the relay change status (set/reset). If input is 0, nothing happens.
     3: [Input addresses (which relays to set when input is on)], accepts:
             '0': none
             'Self': itself, same relay number.
             'All': all Comm5 connected to Middleware, same relay number.
             ['IP:relay number']: other specific Comm5, relay number
                 Accepts list of modules, in the format such as:
                     ['10.19.80.51:1, 10.19.80.52:1, 10.19.80.53:1','Self','Self','Self']
     ],
]

    """

# For Fazenda Veredas:
module_parameters = [
[
    '192.168.1.41', 
    ['NO', 'NO', 'NO', 'NO'],
    ['Fixed', 'Fixed', 'Fixed', 'Fixed'],
    ['192.168.1.41:1, 192.168.1.42:1, 192.168.1.43:1, 192.168.1.44:1',
     '192.168.1.41:1, 192.168.1.42:1, 192.168.1.43:1, 192.168.1.44:1',
     'Self',
     'Self']
],
[
    '192.168.1.42', 
    ['NO', 'NO', 'NO', 'NO'],
    ['Fixed', 'Fixed', 'Fixed', 'Fixed'],
    ['192.168.1.41:1, 192.168.1.42:1, 192.168.1.43:1, 192.168.1.44:1','Self','Self','Self']
],
[
    '192.168.1.43', 
    ['NO', 'NO', 'NO', 'NO'],
    ['Fixed', 'Fixed', 'Fixed', 'Fixed'],
    ['192.168.1.41:1, 192.168.1.42:1, 192.168.1.43:1, 192.168.1.44:1','Self','Self','Self']
],
[
    '192.168.1.44', 
    ['NO', 'NO', 'NO', 'NO'],
    ['Fixed', 'Fixed', 'Fixed', 'Fixed'],
    ['192.168.1.41:1, 192.168.1.42:1, 192.168.1.43:1, 192.168.1.44:1','Self','Self','Self']
],
]

# Test
#module_parameters = [
#[
#    '10.19.80.51', 
#    ['NO', 'NO', 'NO', 'NO'],
#    ['Fixed', 'Fixed', 'Fixed', 'Fixed'],
#    ['10.19.80.51:1, 10.19.80.52:1, 10.19.80.53:1, 10.19.80.54:1','Self','Self','Self']
#],
#[
#    '10.19.80.52', 
#    ['NO', 'NO', 'NO', 'NO'],
#    ['Fixed', 'Fixed', 'Fixed', 'Fixed'],
#    ['10.19.80.51:1, 10.19.80.52:1, 10.19.80.53:1, 10.19.80.54:1','Self','Self','Self']
#],
#[
#    '10.19.80.53', 
#    ['NO', 'NO', 'NO', 'NO'],
#    ['Fixed', 'Fixed', 'Fixed', 'Fixed'],
#    ['10.19.80.51:1, 10.19.80.52:1, 10.19.80.53:1, 10.19.80.54:1','Self','Self','Self']
#],
#[
#    '10.19.80.54', 
#    ['NO', 'NO', 'NO', 'NO'],
#    ['Fixed', 'Fixed', 'Fixed', 'Fixed'],
#    ['10.19.80.51:1, 10.19.80.52:1, 10.19.80.53:1, 10.19.80.54:1','Self','Self','Self']
#],
#]