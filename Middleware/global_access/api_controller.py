import requests
import threading
from time import sleep
import json
import websocket
from pprint import pprint
import sys
from websocket import create_connection

from config_files.config_global_access import API_URL, web_socket_url   # Importing configurations.
from controllers.list_controller import ListController
from controllers.log_controller import LogController


class ApiController:
    # This class connects with GA API, which makes the interface with the database.

    # Class variables:
    logger = LogController()            # Log controller.get_eqpt_by_IP_port
    module_list = ListController()      # Controller that will access and manipulate one single list of modules.
    max_try = 2                         # Maximum number of tries between DB requests.
    DBsleepTime = 2                     # Seconds to sleep between DB requests.
    
# Methods that run on each equipment module connection:
# TODO: convert three methods into only one? It may be necessary to standardize data returned from API Core as well.

    def get_eqpt_parameters(self, ip):    
        """Gets equipment parameters from database, through API, based on IP."""

        try:
            url = API_URL + f'Equipment/{ip}'
            msg = None

            # Loop inserted in case DB does not respond timelly in the first try, causing equipment not to work.
            ii = 1
            while ii <= self.max_try:     
                
                r = requests.get(url, verify=False)
                data = r.json()

                if data['status'] == 'Error' and data['message'] == 'Equipment not found':
                    msg = f'IP not found by {self.__class__.__name__}.{sys._getframe().f_code.co_name}. IP: {ip}. Try {ii}/{self.max_try}.'
                    self.logger.warning(msg)
                    sleep(self.DBsleepTime)   # Sleep for some seconds.

                elif data['status'] == 'Success':
                    equipment_number = int(data['equipment_number'])
                    parameters  = data['dict']
                    msg = f'Equipment parameters identified for IP: {ip}'
                    self.logger.info(msg)
                    return equipment_number, parameters, msg

                else:
                    msg = f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. IP: {ip}. Data = {data}. Try {ii}/{self.max_try}.'
                    self.logger.error(msg)
                    sleep(self.DBsleepTime)   # Sleep for some seconds.

                ii += 1

        except Exception as err:
            msg = (
                    f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                    f'Error message: {err}. ' +\
                    f'IP: {ip}.'
                    )
            self.logger.error(msg)
        
        return None, None, msg

    def get_eqpt_parameters_by_IP_port(self, ip, original_port):    
        """Gets equipment parameters from database, through API, based on IP and original serial port."""

        try:
            url = API_URL + f'Equipment/byIPAndPort/{ip}/{original_port}'
            msg = None

            # Loop inserted in case DB does not respond timelly in the first try, causing equipment not to work.
            ii = 1
            while ii <= self.max_try:    

                r = requests.get(url, verify=False)
                data = r.json()                         # Loading data from JSON to a dictionary.

                if data['status'] == 'Error' and data['message'] == 'No itens found in database for the requested query.':
                    msg = f'Equipment not found in method {self.__class__.__name__}.{sys._getframe().f_code.co_name}. IP: {ip}, port: {original_port}'
                    self.logger.error(msg)
                    sleep(self.DBsleepTime)             # Sleep for some seconds.

                elif data['status'] == 'Success':
                    equipment_number = int(data['query']['equipment_number'])
                    relay_number = int(data['query']['relay_number'])
                    access_request_type = int(data['query']['access_request_type'])
                    msg = f'Identified connection. Equipment: {equipment_number} (IP: {ip}, relay: {relay_number}, port: {original_port})'
                    self.logger.info(msg)
                    return equipment_number, access_request_type, relay_number, msg

                else:
                    msg = f'(data[u"status"] !=  "Success") in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. IP: {ip}, port: {original_port}'
                    self.logger.error(msg)
                    sleep(self.DBsleepTime)   # Sleep for some seconds.

                ii += 1

        except Exception as err:
            msg = (
                f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                f'Error message: {err}. '+\
                f'IP: {ip}, port: {original_port}.'
                )
            self.logger.error(msg)

        return None, None, None, msg

    def get_eqpt_parameters_by_IP_relay(self, ip, nu_IO):
        """Gets equipment parameters from database, through API, based on IP and IO number."""

        try:
            url = API_URL + f'Equipment/byIPAndRelay/{ip}/{nu_IO}'
            msg = None

            # Loop inserted in case DB does not respond timelly in the first try, causing equipment not to work.
            ii = 1
            while ii <= self.max_try:     
                
                r = requests.get(url, verify=False)
                data = r.json()

                if data['status'] == 'Error' and data['message'] == 'No itens found in database for the requested query.':
                    msg = f'IP/relay not found by {self.__class__.__name__}.{sys._getframe().f_code.co_name}. IP: {ip}, Relay: {nu_IO}. Try {ii}/{self.max_try}.'
                    self.logger.warning(msg)
                    sleep(self.DBsleepTime)   # Sleep for some seconds.

                elif data['status'] == 'Success':
                    equipment_number    = int(data['query']['equipment_number'])
                    relay_type          = data['query']['relay_type']
                    relay_timing        = data['query']['relay_timing']
                    input_address       = data['query']['input_address']
                    msg = f'IO parameters identified for IP: {ip}, nu_IO: {nu_IO}'
                    self.logger.info(msg)
                    return equipment_number, relay_type, relay_timing, input_address, msg

                else:
                    msg = (
                        f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                        f'IP: {self.IP}. Relay: {nu_IO}.'+\
                        f'Data = {data}. Try {ii}/{self.max_try}.'
                        )
                    self.logger.error(msg)
                    sleep(self.DBsleepTime)   # Sleep for some seconds.

                ii += 1

        except Exception as err:
            msg = (
                f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                f'Error message: {err}. ' +\
                f'IP: {ip}, IO: {nu_IO}.'
                )
            self.logger.error(msg)
        
        return None, None, None, None, msg

# Methods that run on each person access:

    def access_request(self, identifier_number, equipment_number, access_request_type):
        """ Requesting access for the 'identifier_number'
            to the equipment 'equipment_number'.
            Requesting access type number 'access_request_type'.
            Returns access_request_number and access_response_type
        """

        try:
            ii = 1

            url = API_URL + f'AccessRequest/{identifier_number}/{equipment_number}/{access_request_type}'
            
            # Loop inserted on 2019-08 to request DB more than once. Sometimes, DB does not respond, causing equipment not to work.
            # Loop is limited to 5 iterations because Comm5 may have some relays with no equipment associated to them.
            while ii <= self.max_try:     
                
                msg = f'Requesting access: Equipment: {equipment_number}, identifier: {identifier_number}, request: {access_request_type}. Try {ii}/{self.max_try}.'
                self.logger.info(msg)
                
                r = requests.get(url, verify=False)
                data = r.json()

                if data['status'] == 'Success':
                    access_request_number = int(data['access_request_number'])              # Sequential number of request.
                    # person_name = data['person_name']                                     # Person's name.
                    access_response_type = int(data['access_response_type'])                # Response code to access request.
                    access_response_description = data['access_response_description']       # Response description to access request.

                    # Printing and logging response to access request:
                    msg = f'Request number {access_request_number}. Response: {access_response_description}.'
                    self.logger.info(msg)

                    return access_request_number, access_response_type

                else:
                    msg = f'Connection error with database in method {self.__class__.__name__}.{sys._getframe().f_code.co_name}. Equipment: {equipment_number}, try #{ii}'
                    self.logger.error(msg)
                    ii += 1
                    continue                            # Skip the rest of the code inside the loop for the current iteration only. Loop does not terminate but continues on with the next iteration. Ref: https://www.programiz.com/python-programming/break-continue

        except Exception as err:
            msg = (
                f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                f'Error message: {err}' +\
                f'Identifier: {identifier_number}, Equipment: {equipment_number}, Access requested: {access_request_type}.'
                )
            self.logger.error(msg)

        return None, None

    def access_request_register_publish(self, identifier_number, equipment_number, access_request_type):
        """Auxiliary method that requests, register and publishes (to dashboard) access.
        The access register is made with the same access_response_type returned by access_request,
        so this method is to be used by equipment that does not check if access was actually made
        (equipment that assumes access was made).
        """

        # Requesting access:
        access_request_number, access_response_type = self.access_request(identifier_number, equipment_number, access_request_type)

        # Registering access and publishing to dashboard:
        self.access_register_publish_thread(access_request_number, access_request_type, access_response_type)

        return access_response_type

    def access_register_publish_thread(self, access_request_number, access_request_type = None, access_response_type = None, access_made_type = None):
        """Starting as thread to:
            Improve speed on activating equipment.
            If error occours during the access registration, equipment is still activated.
        """
        threading.Thread(target = self.access_register_publish,
                name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}',
                args = (access_request_number, access_request_type, access_response_type, access_made_type)
                ).start()

        return

    def access_register_publish(self, access_request_number, access_request_type = None, access_response_type = None, access_made_type = None):
        """Auxiliary method that register and publishes (to dashboard) access."""

        # Registering info in database table TB_REGISTRO_ACESSO:
        self.access_register(access_request_number, access_request_type, access_response_type, access_made_type)

        # Getting access information and updating dashboard:
        self.get_info_and_photo_and_update_dashboad_thread(access_request_number)

        return

    def access_register(self, access_request_number, access_request_type = None, access_response_type = None, access_made_type = None):
        """ Registering access actually made by person in database, table TB_REGISTRO_ACESSO."""

        try:

            # If neither access_made_type or access_response_type was informed, do nothing and return.
            if not access_made_type and not access_response_type:
                return False

            # If only access_made_type was not explicitly informed, tryes to imply access_made_type from access_response_type:
            if not access_made_type:

                if access_response_type == 3 :                  # If access responded was exit by urn (3), 
                    access_made_type = 2                        # access made by person was regular exit (2).

                elif access_response_type == 6 :                # If access response was entry/exit (6),
                    if access_request_type == 3:                # if access requested was exit by urn (3),
                        access_made_type = 2                    # converts to regular exit (2)
                    else:                                       # If access requested was other (entry (1) or regular exit (2)),
                        access_made_type = access_request_type  # assumes access made was equal to access requested (entry (1) or regular exit (2)).

                else:                                           # If access response was another (entry (1), regular exit (2), button (4), or denied (5, 7 to 21).
                    access_made_type = access_response_type     # assumes access made was equal to access requested.

            # Uses API to register access.
            url = API_URL + f'AccessRegister/{access_request_number}/{access_made_type}'
            r = requests.get(url, verify=False)
            data = r.json()

            if data['status'] == 'Success':
                msg = 'Registered access.'
                self.logger.info(msg)
                return True

        except Exception as err:
            msg = f'Error in method {self.__class__.__name__}.{sys._getframe().f_code.co_name}'
            self.logger.error(msg)

        return False

    def get_person_access_info(self, access_request_number):
        """Getting person and access information for this access request."""
        try:
            # Logging
            msg = f'Getting person and access info for access_request_number: {access_request_number}'
            self.logger.info(msg)
            
            # Getting info from API:
            url = API_URL + 'PersonAccessInfo/{}'.format(access_request_number)
            r = requests.get(url, verify=False)
            data = r.json()

            # If got no data (For instace: when access is requested via button):
            if data['status'] == 'Error' and data['message'] == 'No itens found in database for the requested query.':
                msg = ('Warning in {}.{}. '+\
                        'No data received for access_request_number: {}. ' +\
                        'Access was probably via button.'
                        ).format(
                        self.__class__.__name__,                    # Class name.
                        sys._getframe().f_code.co_name,             # Method name.
                        access_request_number                       # Specific information.
                        )

                self.logger.warning(msg)
                return None

            # If got info with success, sending to Dashboard.
            elif data['status'] == 'Success':
                return data['query'] 

        except Exception as err:
            msg = (
                f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                f'Error message: {err}' +\
                f'access_request_number: {access_request_number}.'
                )
            self.logger.error(msg)

        return None

    def get_person_photo(self, person_number):
        """Getting person photo in base 64 string."""

        try:
            # Logging
            msg = f'Getting photo for person_number: {person_number}'
            self.logger.info(msg)
            
            # Getting info from API:
            url = API_URL + f'Photo/Person/{person_number}'
            r = requests.get(url, verify=False)
            data = r.json()

            # If got info successfully:
            if data['status'] == 'Success':
                return data['photo_base64']

            # If no file was found on database, displays default icon:
            else: 
                # Default icon: Account_Box_Blue_512.png . Conversion: https://www.base64-image.de/
                # 64 x 64 px:
                #default_photo = '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'
                # 256 x 256 px:
                default_photo = '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'
                # 512 x 512 px:
                #default_photo = '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'
                
                return default_photo

        except Exception as err:
            msg = (
                f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                f'Error message: {err}' +\
                f'person_number: {co_pessoa}.'
                )
            self.logger.error(msg)

        return ' '

# Methods to send data via WebSockets to Dashboard:

    def get_info_and_photo_and_update_dashboad_thread(self, access_request_number):
        """Starting method as thread."""

        threading.Thread(target = self.get_info_and_photo_and_update_dashboad,
                name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}',
                args = (access_request_number, )
                ).start()

        return

    def get_info_and_photo_and_update_dashboad(self, access_request_number):
        """Getting person and access information for this access request.
        And updating dashboard.
        """

        try:
            data_dict = self.get_person_access_info(access_request_number)                              # Getting written information.

            if data_dict:                                                                               # If got written information successfully.

                data_dict['person_photo_base64'] = self.get_person_photo(data_dict['person_number'])    # Getting person photo by person key (person_number = CO_SEQ_PESSOA).
                
                # Selecting what id number will appear in dashboard:
                # TODO: Move code below to Django view.
                if data_dict['person_id_cpf']:
                    person_id_description = 'CPF' 
                    person_id_number = data_dict['person_id_cpf']
                elif data_dict['person_id_id']:
                    person_id_description = 'Identidade' 
                    person_id_number = data_dict['person_id_id']
                elif data_dict['person_id_passport']:
                    person_id_description = 'Passaporte' 
                    person_id_number = data_dict['person_id_passport']
                else:
                    person_id_description = 'Documento não consta na base de dados.' 
                    person_id_number = ''

                # Updating dictionary with information.
                data_dict['person_id_description'] = person_id_description
                data_dict['person_id_number'] = person_id_number

                self.update_dashboard_short_lived(data_dict)                    # Sending data to dashboard.

        except Exception as err:
            msg = (
                    f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                    f'Error message: {err}' +\
                    f'access_request_number: {access_request_number}.'
                    )
            self.logger.error(msg)

        return

    def update_dashboard_short_lived(self, data_dict):
        """Sending information to update the dashboard by short-lived one-off send-receive.
        This is if you want to communicate a short message and disconnect immediately when done.
        Ref: https://pypi.org/project/websocket_client/
        """
        
        msg = 'Sending data to dashboard.'
        self.logger.info(msg)

        # Connecting:
        ws = create_connection(web_socket_url)

        # Building JSON to be sent:
        data_json = json.dumps(data_dict)
        
        # Sending data to websocket:
        #print("Sending:")
        #pprint(data_dict)
        ws.send(data_json)
        #print("Sent\n")

        # Receiving data from websocket:
        #print("Receiving...")
        result_json =  ws.recv()
        #result_dict = json.loads(result_json)
        #print('Received:\n')
        #pprint(result_dict)
        #print('')

        ws.close()

        return True

    def update_dashboard_long_lived(self, person_name, identifier_number, equipment_number,
                                    co_requested_access, access_request_type, access_response_description):
        """ Sending information to update the dashboard by long-lived connection.
        It is similar to how WebSocket code looks in browsers using JavaScript.
        Ref: https://pypi.org/project/websocket_client/
        """

        def on_message(ws, message):
            result_json =  ws.recv()
            result_dict = json.loads(result_json)
            pprint(result_dict)

        def on_error(ws, error):
            print(error)
        
        def on_close(ws):
            print("### closed ###")

        def on_open(ws):

            def run(*args):

                data_dict = {'person_name': 'Message from: update_dashboard_2_long_lived'}
                data_json = json.dumps(data_dict)
                    
                ws.send(data_json)

                ws.close()
                print("thread terminating...")
            
            threading.Thread(target = run,
                name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}.run',
                args = ()
                ).start()

        websocket.enableTrace(True)
        ws = websocket.WebSocketApp('ws://localhost:5865/ws/dashboard/',
                                        on_message = on_message,
                                        on_error = on_error,
                                        on_close = on_close)
        ws.on_open = on_open
        ws.run_forever()

        return

# Methods to get access information for reports:
    def get_access_made_info(self, equipment_number, access_made_type, datetime_start, datetime_end):
        """Getting access made info. Specific for report with temperature."""
        try:
            # Logging
            msg = f'Getting person and access info for equipment_number: {equipment_number}, access_made_type: {access_made_type}, from: {datetime_start}, to: {datetime_end}'
            self.logger.info(msg)
            
            # Getting info from API:
            url = API_URL + f'AccessMade/{equipment_number}/{access_made_type}/{datetime_start}/{datetime_end}'
            r = requests.get(url, verify=False)
            data = r.json()

            # If got no data (For instace: when access is requested via button):
            if data['status'] == 'Error' and data['message'] == 'No itens found in database for the requested query.':
                msg = (f'Warning in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. ' +\
                       f'No data received for equipment_number: {equipment_number}, access_made_type: {access_made_type}, from: {datetime_start}, to: {datetime_end}'
                        )

                self.logger.warning(msg)
                return None

            # If got info with success, returns data.
            elif data['status'] == 'Success':
                return data['query']

        except Exception as err:
            msg = (f'Error in {self.__class__.__name__}.{sys._getframe().f_code.co_name}. '+\
                    f'Error message: {err}' +\
                    f'equipment_number: {equipment_number}, access_made_type: {access_made_type}, from: {datetime_start}, to: {datetime_end}.'
                    )
            self.logger.error(msg)

        return None

# Testing:
if __name__ == "__main__":
    api = ApiController()
    received_data = api.update_dashboard_short_lived(27476)
    pprint(received_data)
    pass

