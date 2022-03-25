import requests
from time import sleep
import threading
import sys

from config_files import config_email, config_global_access
from controllers import email_controller, list_controller, log_controller


class EscapeRouteController:

    # Class variables:
    logger = log_controller.LogController()                             # Log controller.
    escape_route_url = config_global_access.API_URL + 'EscapeRoute'     # Getting GA API url.
    email_controller = email_controller.EmailController()               # Starting e-mail controller:
    module_list = list_controller.ListController()                      # Controller that will access and manipulate list of modules.

    """ Statuses in database to be considered:

    In table TB_ROTA_FUGA:
    ST_ATIVO	Modo de Operação
        0	    Invisível para usuário / "Excluída"
        1	    Visível para usuário e desativada
        2	    Visível para usuário e ativada

    In equipment tables TB_EQUIPAMENTOS.ST_ATIVO and TB_ROTA_EQUIPAMENTO.ST_MODO_OPERACAO:
    ST_ATIVO	Modo de Operação
        0	    Desativado
        1	    Ativado
        2	    Em Bloqueio
        3	    Liberado remota
        4	    Liberado física
    """

    def watch_escape_routes_statuses(self):
        """ Checks indefinety for escape routes statuses and
        activate/deactivate a escape route when it's status changes.
        """

        try:
            # Getting first matrix, with Escape Routes numbers and status.
            escape_route_list_1 = self.get_escape_route_statuses()

            # Running indefinitely:
            while True:
                # Waiting for some seconds.
                sleep(3)

                # Getting second list, with Escape Routes numbers and status.
                escape_route_list_2 = self.get_escape_route_statuses()

                # Comparing lists:
                for ii in range(len(escape_route_list_1)):          # Getting each escape route on list_1
                    for jj in range(len(escape_route_list_2)):      # Getting each escape route on list_2.

                        if escape_route_list_1[ii]['escape_route_number'] == escape_route_list_2[jj]['escape_route_number']:            # If escape_route_number is equal:
                        
                            # If escape route was set to active (ST_ATIVO = 2), sends activation command constantly:
                            if escape_route_list_2[jj]['escape_route_status'] == '2':

                                # Activating escape route.
                                success = self.activate_escape_route(escape_route_list_1[ii]['escape_route_number'])

                                # If this is the 1st activation of escape route (escape_route_status was 1 in the previous check):
                                if escape_route_list_1[ii]['escape_route_status'] == '1':               
                                
                                    # If activation was successfull: 
                                    if success:                      
                                        preamble = 'Escape Route: Activated'
                                        msg = preamble + ': # ' + str(int(escape_route_list_1[ii]['escape_route_number'])) + ' - Name: ' + escape_route_list_1[ii]['escape_route_name']
                                    else:
                                        preamble = 'Escape Route: 1st activation failed'
                                        msg = preamble + ': # ' + str(int(escape_route_list_1[ii]['escape_route_number'])) + ' - Name: ' + escape_route_list_1[ii]['escape_route_name']
                                    
                                    # Registering on log.
                                    self.logger.info(msg)           

                                    # Sending e-mail:
                                    if config_email.send_email_on_escape_route == True:
                                        # Parameters: send_gmail(subject, message):
                                        threading.Thread(target = self.email_controller.send_gmail,
                                                            name = 'send_gmail', 
                                                            args = (preamble, msg)
                                                        ).start()

                            # If escape route was set to deactive (ST_ATIVO was 2 and now is 1), sends deactivation command only once.
                            # If command to deactivate escape route was constantly sent, commands to reset the relays could be sent in inappropriate times.
                            if escape_route_list_1[ii]['escape_route_status'] == '2' and escape_route_list_2[jj]['escape_route_status'] == '1':
                                
                                # Deactivating escape Route.
                                success = self.deactivate_escape_route(escape_route_list_1[ii]['escape_route_number'])  

                                # If deactivation was successfull: 
                                if success:
                                    preamble = 'Escape Route: Deactivated'
                                    msg = preamble + ': # ' + str(int(escape_route_list_1[ii]['escape_route_number'])) + ' - Name: ' + escape_route_list_1[ii]['escape_route_name']
                                else:
                                    preamble = 'Escape Route: 1st deactivation failed'
                                    msg = preamble + ': # ' + str(int(escape_route_list_1[ii]['escape_route_number'])) + ' - Name: ' + escape_route_list_1[ii]['escape_route_name']

                                # Registering on log.
                                self.logger.info(msg)
                                
                                # Sending e-mail:
                                if config_email.send_email_on_escape_route == True:
                                    # Parameters: send_gmail(subject, message):
                                    threading.Thread(target = self.email_controller.send_gmail,
                                                        name = 'send_gmail', 
                                                        args = (preamble, msg)
                                                    ).start()

                # Updating list_1:
                escape_route_list_1 = escape_route_list_2

        except Exception as err:
            msg = ('Error in method {}.{}. '+\
                    'Error message: {}').format(
                    self.__class__.__name__,
                    sys._getframe().f_code.co_name,
                    err)
            self.logger.error(msg)

        return

    def get_escape_route_statuses(self):
        """ Gets list of Escape Routes.
            Returns list of dictionaries, containing each dictionary:
            {escape_route_number,escape_route_name,escape_route_status}
        """

        try:
            # Getting information from GA API:
            r = requests.get(self.escape_route_url)
            data = r.json()
            
            # If GA API returned with success, method returns with list of dictionaries.
            if data[u'status'] == 'Success':

                return data[u'query']

                # Getting information as list of dictionaries, each as such:
                #   {"cO_SEQ_ROTA_FUGA": 6,
                #    "dS_ROTA_FUGA": "(07) EAMN-EVACUAÇÃO",
                #    "sT_ATIVO": "1"}
                #GA_API_matrix = data[u'query']

                # List that will contain [CO_SEQ_ROTA_FUGA, DS_ROTA_FUGA, ST_ATIVO]:
                #matrix = numpy.zeros((len(GA_API_matrix), 3))
                #matrix = []

                ## Getting CO_SEQ_ROTA_FUGA and ST_ATIVO from 'GA_API_matrix' into 'matrix':
                #for ii in range(len(GA_API_matrix)):

                #    matrix.append([
                #        GA_API_matrix[ii]['escape_route_number'],   # Getting CO_SEQ_ROTA_FUGA (int)
                #        GA_API_matrix[ii]['escape_route_name'],     # Getting DS_ROTA_FUGA     (string)
                #        GA_API_matrix[ii]['escape_route_status'],   # Getting ST_ATIVO         (string)
                #        ])

                #return matrix

            else:
                msg = ('Error in method {}.{}. ' +\
                    'API returned unexpected status. ' +\
                    'Error message: {}').format(
                    self.__class__.__name__,
                    sys._getframe().f_code.co_name,
                    err)

                self.logger.error(msg)

                return False

        except Exception as err:
            msg = ('Error in method {}.{}. '+\
                    'Error message: {}').format(
                    self.__class__.__name__,
                    sys._getframe().f_code.co_name,
                    err)
            self.logger.error(msg)

        return None

    def get_equipments_in_escape_route(self, escape_route_number):
        """ Gets equipment list for the Escape Route #escape_route_number.
            Returns list of dictionaries, each dictionary contains:
            {equipment_name, equipment_number, equipment_operation_mode},
        """
        try:
            # Getting information from GA API:
            url = self.escape_route_url + '/' + str(escape_route_number)
            r = requests.get(url)
            data = r.json()
            
            # If GA API returned success, getting key 'status', with the equipment information as list of dictionaries.
            if data[u'status'] == 'Success':
                return data[u'query']
                #GA_API_matrix = data[u'query']  # E.g. {"equipment_name": "Z_PORTA_TESTE_COMM5_1", "equipment_number": 115, "equipment_operation_mode": "2"}

                ## Creating list of equipments that will contain:
                #    # [equipment_number, 
                #    #  equipment_operation_mode, 
                #    #  IP, 
                #    #  Relay Number]
                #equipment_list = []

                ## Getting parameters from 'GA_API_matrix' into 'matrix':
                #for ii in range(len(GA_API_matrix)):

                #    # Seeing if a equipment with this equipment_number is already in equipmentsList:
                #    #eqpt = next((equipment for equipment in equipmentsList if equipment[1] == GA_API_matrix[ii]['equipment_number']), None)
                #    # Changed to code bellow because 'next' kept throwing exceptions even when apparently working fine. It was making debugging difficult.
                #    eqpt = None
                #    for equipment in equipment_list:
                #        if equipment[1] == GA_API_matrix[ii]['equipment_number']:
                #            eqpt = equipment
                #            break

                #    # If equipment is not on equipmentsList, adds it:
                #    if eqpt == None:
                #        equipment_list.append([
                #                                GA_API_matrix[ii]['equipment_name'],
                #                                GA_API_matrix[ii]['equipment_number'],
                #                                GA_API_matrix[ii]['equipment_operation_mode'],
                #                               ])

                #return equipment_list

            else:
                msg = '(data[u"status"] !=  "Success") in EscapeRouteController.get_equipments_in_escape_route().'
                self.logger.error(msg)

        except Exception as err:
            msg = ('Error in method {}.{}. '+\
                    'Error message: {}').format(
                    self.__class__.__name__,
                    sys._getframe().f_code.co_name,
                    err)
            self.logger.error(msg)

        return None

    def activate_escape_route(self, escape_route_number):
        """ Activating equipments in the informed escape route. """

        try:
            # Getting equipments in Escape Route #escape_route_number.
            equipments_in_escape_route = self.get_equipments_in_escape_route(escape_route_number)

            # For each equipment escape route:
            for equipment in equipments_in_escape_route:  

                # Getting module(s), and relay(s) number(s) in module_list.
                modules_list, relay_list = self.module_list.get_modules(equipment_number = equipment['equipment_number'])

                # For each module 'm' and relay 'r', sends command accordingly to 'equipment_operation_mode'.
                for m, r in zip(modules_list, relay_list):
                    if equipment['equipment_operation_mode'] == '2':        # Block.
                        m.passage_block(r, escape_route_number)
                    elif equipment['equipment_operation_mode'] == '3':      # Soft allow.
                        m.passage_allow_soft(r, escape_route_number)
                    elif equipment['equipment_operation_mode'] == '4':      # Hard allow.
                        m.passage_allow_hard(r, escape_route_number)

            success = True

        except Exception as err:
            msg = ('Error in method {}.{}. '+\
                    'Error message: {}').format(
                    self.__class__.__name__,
                    sys._getframe().f_code.co_name,
                    err)
            self.logger.error(msg)

            success = False

        return success

    def deactivate_escape_route(self, escape_route_number):
        """ Deactivating equipments in the informed escape route. """
        try:
            # Getting equipments in Escape Route #escape_route_number.
            equipments_in_escape_route = self.get_equipments_in_escape_route(escape_route_number)

            # For each equipment escape route:
            for equipment in equipments_in_escape_route:  

                # Getting module(s), and relay(s) number(s) in module_list.
                modules_list, relay_list = self.module_list.get_modules(equipment_number = equipment['equipment_number'])

                # For each module 'm' and relay 'r', sends command to normalize operation.
                for m, r in zip(modules_list, relay_list):
                    m.passage_normalize(r, escape_route_number)

            success = True

        except Exception as err:
            msg = ('Error in method {}.{}. '+\
                    'Error message: {}').format(
                    self.__class__.__name__,
                    sys._getframe().f_code.co_name,
                    err)
            self.logger.error(msg)

            success = False

        return success