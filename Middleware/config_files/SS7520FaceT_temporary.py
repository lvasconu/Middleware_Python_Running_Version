'''
2021-07:
This file is meant to be temporary.
As request by CNI, it is aimed to provide a quick integration with the Intelbras SS7520FaceT Controllers.
A permanent solution must carry all the information below to the database.
'''

''' List with parameters of all Intelbras SS7520FaceT Controllers
    Parameters:
        SS7520FaceT_ip:             The SS7520FaceT's IP
        SS7520FaceT_direction:      The direction in which person is going (entry (1), exit (2), entry / exit (6))
        barrier_equipment_ip:       The ip of the barrier equipment (usually a turnstyle, but it could be a door or any other).
        barrier_equipment_number:   The equipment number (in the database) of the barrier equipment

Query to search:

select TB_EQUIPAMENTO.NO_EQUIPAMENTO, TB_EQUIPAMENTO.CO_SEQ_EQUIPAMENTO, TB_PARAMETRO_EQUIPAMENTO.VL_PARAMETRO

from TB_EQUIPAMENTO
join TB_PARAMETRO_EQUIPAMENTO on TB_EQUIPAMENTO.CO_SEQ_EQUIPAMENTO = TB_PARAMETRO_EQUIPAMENTO.CO_EQUIPAMENTO
join TB_PARAMETRO on TB_PARAMETRO_EQUIPAMENTO.CO_PARAMETRO = TB_PARAMETRO.CO_SEQ_PARAMETRO

where TB_EQUIPAMENTO.CO_MODELO_EQUIPAMENTO = 1	-- Wolpac
and TB_PARAMETRO.CO_SEQ_PARAMETRO = 1			-- IP

'''

config_list = [
{'face_ip': '10.19.80.162', 'access_made_type': '1', 'barrier_equipment_number': '3', 'barrier_equipment_name': 'ERS 1SS - CATRACA 1'},
{'face_ip': '10.19.80.159', 'access_made_type': '2', 'barrier_equipment_number': '3', 'barrier_equipment_name': 'ERS 1SS - CATRACA 1'},
#N/D
{'face_ip': '10.19.80.150', 'access_made_type': '1', 'barrier_equipment_number': '5', 'barrier_equipment_name': 'ERS 00 - CATRACA 1'},
{'face_ip': '10.19.80.156', 'access_made_type': '2', 'barrier_equipment_number': '5', 'barrier_equipment_name': 'ERS 00 - CATRACA 1'},
#N/D
{'face_ip': '10.19.80.158', 'access_made_type': '1', 'barrier_equipment_number': '7', 'barrier_equipment_name': 'ERS 00 - CATRACA 3'},
{'face_ip': '10.19.80.157', 'access_made_type': '2', 'barrier_equipment_number': '7', 'barrier_equipment_name': 'ERS 00 - CATRACA 3'},
#N/D
{'face_ip': '10.19.80.151', 'access_made_type': '1', 'barrier_equipment_number': '9', 'barrier_equipment_name': 'ERS 00 - CATRACA 5'},
{'face_ip': '10.19.80.152', 'access_made_type': '2', 'barrier_equipment_number': '9', 'barrier_equipment_name': 'ERS 00 - CATRACA 5'},
{'face_ip': '10.19.80.160', 'access_made_type': '1', 'barrier_equipment_number': '10', 'barrier_equipment_name': 'EAMN 1SS - CATRACA 1'},
{'face_ip': '10.19.80.161', 'access_made_type': '2', 'barrier_equipment_number': '10', 'barrier_equipment_name': 'EAMN 1SS - CATRACA 1'},
    ]

''' Companies which employees will be inserted into temperature report.

'''
company_list = [
    4, # 5 ESTRELAS
    25, # 5 ESTRELAS CONSERVACAO
    96, # 5 ESTRELAS SEGURANÇA
    35, # AÇAO PRO AMAZONIA
    103, # AÇÃO PRO AMAZONIA
    48, # AGM
    1071, # AGM TURISMO
    77, # AMIL
    74, # CNI
    22, # SPOT
    132, # STEFANINI 
    6, # TCALL 
    93, # TREVO
    1206, # UNINDUSTRIA
    ]