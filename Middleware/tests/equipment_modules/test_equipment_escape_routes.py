from controllers.list_controller import ListController
from equipment_modules import generic_module, comm5, wolpac

# To run, open cmd in folder and type:
    # All tests: pytest -v --durations=0
    # Specific test: pytest -v --durations=0 -k "method name"
    # Ref: https://docs.pytest.org/en/latest/usage.html

list_controller = ListController()

# Generating modules and equipment numbers.
a = generic_module.GenericModule('10.19.2.1')
b = comm5.MA('10.19.2.2')
c = comm5.MA('10.19.2.3')
d = wolpac.Waffer('10.19.2.3')
d.delayed_send_allowed = True

a.equipment_number[0] = 245
b.equipment_number[1] = 245
c.equipment_number[2] = 289
d.equipment_number[0] = 21

# Adding to list.
list_controller.append(a)
list_controller.append(b)
list_controller.append(c)
list_controller.append(d)

# Escape Routes - Simple activations - Wolpac:

route_number_1 = 244
route_number_2 = 265

""" Escape Routes - Generic Module - Compound activations - 1221:
Activate 1st.
(Tryes to) activate 2nd.
Deactivate 2nd.
Deactivate 1st.
"""

def test_generic_block_block():

    # Activate 1st
    received_data_1 = a.passage_block(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = a.blocked_by_route[0]

    # (Tryes to) Activate 2nd
    received_data_2 = a.passage_block(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = a.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = a.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = a.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = a.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = a.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

def test_generic_block_soft():

    # Activate 1st
    received_data_1 = a.passage_block(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = a.blocked_by_route[0]

    # (Tryes to) Activate 2nd
    received_data_2 = a.passage_allow_soft(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = a.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = a.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = a.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = a.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = a.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

def test_generic_block_hard():

    # Activate 1st
    received_data_1 = a.passage_block(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = a.blocked_by_route[0]

    # (Tryes to) Activate 2nd
    received_data_2 = a.passage_allow_hard(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = a.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = a.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = a.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = a.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = a.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

def test_generic_soft_soft():

    # Activate 1st
    received_data_1 = a.passage_allow_soft(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = a.blocked_by_route[0]

    # (Tryes to) Activate 2nd
    received_data_2 = a.passage_allow_soft(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = a.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = a.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = a.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = a.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = a.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

def test_generic_soft_block():

    # Activate 1st
    received_data_1 = a.passage_allow_soft(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = a.blocked_by_route[0]

    # (Tryes to) Activate 2nd
    received_data_2 = a.passage_block(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = a.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = a.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = a.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = a.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = a.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

def test_generic_soft_hard():

    # Activate 1st
    received_data_1 = a.passage_allow_soft(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = a.blocked_by_route[0]

    # (Tryes to) Activate 2nd
    received_data_2 = a.passage_allow_hard(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = a.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = a.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = a.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = a.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = a.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

def test_generic_hard_hard():

    # Activate 1st
    received_data_1 = a.passage_allow_hard(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = a.blocked_by_route[0]

    # (Tryes to) Activate 2nd
    received_data_2 = a.passage_allow_hard(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = a.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = a.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = a.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = a.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = a.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

def test_generic_hard_soft():

    # Activate 1st
    received_data_1 = a.passage_allow_hard(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = a.blocked_by_route[0]
    
    # (Tryes to) Activate 2nd
    received_data_2 = a.passage_allow_soft(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = a.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = a.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = a.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = a.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = a.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

def test_generic_hard_block():

    # Activate 1st
    received_data_1 = a.passage_allow_hard(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = a.blocked_by_route[0]

    # (Tryes to) Activate 2nd
    received_data_2 = a.passage_block(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = a.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = a.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = a.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = a.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = a.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

""" Escape Routes - Comm5 - Compound activations - 1221:
Activate 1st.
(Tryes to) activate 2nd.
Deactivate 2nd.
Deactivate 1st.
"""

def test_comm5_block_block():

    # Activate 1st
    received_data_1 = b.passage_block(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = b.blocked_by_route[0]

    # (Tryes to) Activate 2nd
    received_data_2 = b.passage_block(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = b.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = b.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = b.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = b.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = b.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

def test_comm5_block_soft():

    # Activate 1st
    received_data_1 = b.passage_block(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = b.blocked_by_route[0]

    # (Tryes to) Activate 2nd
    received_data_2 = b.passage_allow_soft(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = b.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = b.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = b.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = b.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = b.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

def test_comm5_block_hard():

    # Activate 1st
    received_data_1 = b.passage_block(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = b.blocked_by_route[0]

    # (Tryes to) Activate 2nd
    received_data_2 = b.passage_allow_hard(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = b.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = b.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = b.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = b.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = b.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

def test_comm5_soft_soft():

    # Activate 1st
    received_data_1 = b.passage_allow_soft(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = b.blocked_by_route[0]

    # (Tryes to) Activate 2nd
    received_data_2 = b.passage_allow_soft(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = b.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = b.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = b.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = b.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = b.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

def test_comm5_soft_block():

    # Activate 1st
    received_data_1 = b.passage_allow_soft(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = b.blocked_by_route[0]

    # (Tryes to) Activate 2nd
    received_data_2 = b.passage_block(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = b.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = b.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = b.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = b.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = b.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

def test_comm5_soft_hard():

    # Activate 1st
    received_data_1 = b.passage_allow_soft(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = b.blocked_by_route[0]

    # (Tryes to) Activate 2nd
    received_data_2 = b.passage_allow_hard(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = b.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = b.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = b.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = b.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = b.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

def test_comm5_hard_hard():

    # Activate 1st
    received_data_1 = b.passage_allow_hard(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = b.blocked_by_route[0]

    # (Tryes to) Activate 2nd
    received_data_2 = b.passage_allow_hard(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = b.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = b.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = b.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = b.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = b.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

def test_comm5_hard_soft():

    # Activate 1st
    received_data_1 = b.passage_allow_hard(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = b.blocked_by_route[0]
    
    # (Tryes to) Activate 2nd
    received_data_2 = b.passage_allow_soft(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = b.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = b.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = b.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = b.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = b.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

def test_comm5_hard_block():

    # Activate 1st
    received_data_1 = b.passage_allow_hard(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = b.blocked_by_route[0]

    # (Tryes to) Activate 2nd
    received_data_2 = b.passage_block(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = b.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = b.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = b.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = b.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = b.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

""" Escape Routes - Wolpac - Compound activations - 1221:
Activate 1st.
(Tryes to) activate 2nd.
Deactivate 2nd.
Deactivate 1st.
"""

def test_wolpac_block_block():

    # Activate 1st
    received_data_1 = d.passage_block(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = d.blocked_by_route[0]

    # (Tryes to) Activate 2nd
    received_data_2 = d.passage_block(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = d.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = d.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = d.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = d.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = d.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

def test_wolpac_block_soft():

    # Activate 1st
    received_data_1 = d.passage_block(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = d.blocked_by_route[0]

    # (Tryes to) Activate 2nd
    received_data_2 = d.passage_allow_soft(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = d.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = d.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = d.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = d.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = d.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

def test_wolpac_block_hard():

    # Activate 1st
    received_data_1 = d.passage_block(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = d.blocked_by_route[0]

    # (Tryes to) Activate 2nd
    received_data_2 = d.passage_allow_hard(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = d.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = d.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = d.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = d.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = d.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

def test_wolpac_soft_soft():

    # Activate 1st
    received_data_1 = d.passage_allow_soft(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = d.blocked_by_route[0]

    # (Tryes to) Activate 2nd
    received_data_2 = d.passage_allow_soft(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = d.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = d.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = d.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = d.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = d.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

def test_wolpac_soft_block():

    # Activate 1st
    received_data_1 = d.passage_allow_soft(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = d.blocked_by_route[0]

    # (Tryes to) Activate 2nd
    received_data_2 = d.passage_block(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = d.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = d.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = d.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = d.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = d.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

def test_wolpac_soft_hard():

    # Activate 1st
    received_data_1 = d.passage_allow_soft(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = d.blocked_by_route[0]

    # (Tryes to) Activate 2nd
    received_data_2 = d.passage_allow_hard(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = d.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = d.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = d.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = d.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = d.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

def test_wolpac_hard_hard():

    # Activate 1st
    received_data_1 = d.passage_allow_hard(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = d.blocked_by_route[0]

    # (Tryes to) Activate 2nd
    received_data_2 = d.passage_allow_hard(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = d.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = d.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = d.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = d.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = d.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

def test_wolpac_hard_soft():

    # Activate 1st
    received_data_1 = d.passage_allow_hard(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = d.blocked_by_route[0]
    
    # (Tryes to) Activate 2nd
    received_data_2 = d.passage_allow_soft(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = d.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = d.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = d.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = d.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = d.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

def test_wolpac_hard_block():

    # Activate 1st
    received_data_1 = d.passage_allow_hard(escape_route_number = route_number_1, test = True)
    blocked_by_route_1 = d.blocked_by_route[0]

    # (Tryes to) Activate 2nd
    received_data_2 = d.passage_block(escape_route_number = route_number_2, test = True)
    blocked_by_route_2 = d.blocked_by_route[0]

    # Deactivate 2nd
    received_data_3 = d.passage_normalize(escape_route_number = route_number_2, test = True)
    blocked_by_route_3 = d.blocked_by_route[0]

    # Deactivate 1st
    received_data_4 = d.passage_normalize(escape_route_number = route_number_1, test = True)
    blocked_by_route_4 = d.blocked_by_route[0]

    received_data = (received_data_1, blocked_by_route_1, received_data_2, blocked_by_route_2, received_data_3, blocked_by_route_3, received_data_4, blocked_by_route_4)
    expected_data = (True, route_number_1, False, route_number_1, False, route_number_1, True, None)

    assert received_data == expected_data

""" Escape Routes - Wolpac - Compound activations - 1212:
Activate 1st.
(Tryes to) activate 2nd.
Deactivate 1st.
Deactivate 2nd.

Can only be tested if escape_route_controller is running and escape routes really change status.


"""

if __name__ == "__main__":
    test_201_comm5_block_block()

