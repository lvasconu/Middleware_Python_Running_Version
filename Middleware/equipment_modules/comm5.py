# Import section:
import threading
import sys

from config_files import config_email
from controllers import email_controller
from equipment_modules import generic_module, config_equipment
from sensors import acura

class MA(generic_module.GenericModule):
    # Ref: "MA-5000-2 e variantes, Manual de programação", available in "Equipamentos\Módulo de Acionamento - Comm5"

    # Class variables:
    number_of_IOs = 4               # Number of IOs (inputs and relays) each to be considered in each module. 
    ping_interval = 3               # Interval between sending each ping message [s].

    # Default messages:
    msg_end                         = '\n'
    msg_identification_beggining    = '200 Bem vindo ao modulo io. Digite help para obter ajuda.\r'
    msg_ping                        = f'ping{msg_end}'              # IO port.
    msg_ping_response               = f'210 OK\r{msg_end}'

    # Communications methods:

    def listen_to_IO(self, controlled_socket):
        """Starts listening (waiting) for IO notification.
        Responds accordingly to message received.
        """

        try:
            self.send('notify on')                              # Turning notifications on.

            while self in self.module_list.list and controlled_socket.online in ('online', 'unknown'):    # While module in module_list and socket is online. Necessary for thread not to run indefinitely.

                data = controlled_socket.communicate()          # Communicating via socket.

                if not data:                                    # If socket broke communication, exits while loop.
                    break

                # Separating information for each IO in binary form (trying to).
                try:
                    if type(data) is bytearray:
                        data_str = str(data,'utf-8')                            # Converting data to UTF-8 string.
                    elif type(data) is str:
                        data_str = data
                    else:
                        continue

                    if data_str.startswith(self.__class__.msg_identification_beggining):                            # If received connection/identification message,
                        continue                                                                                    # Do nothing, but continue in the while loop.

                    # TODO: remove if? (Must keep code that is inside else.)
                    if data_str.startswith('210 OK') or data_str.startswith('OK') or data_str.startswith('200'):    # If string begins with ok confirmation.
                        continue                                                                                    # Do nothing, but continue in the while loop.

                    else:
                        data_int = int(data_str[4:8], 16)                       # Converting string digits 4 to 7 (in base 16) to integer (in base 10).
                        binary_format = '{0:0' + str(self.number_of_IOs) + 'b}' # Formating mask with which to convert integer to binary. Ref.: https://stackoverflow.com/questions/10411085/converting-integer-to-binary-in-python
                        data_bin = binary_format.format(data_int)               # Converting to binary representation (it is actually a string of 0's and 1's).

                except Exception as err:
                    msg = ('Error in method {}.{}. From IP: {}. ' +\
                            'Received unexpected message from IO socket: {}. '+\
                            'Error message: {}').format(
                            self.__class__.__name__,
                            sys._getframe().f_code.co_name,
                            self.IP,
                            data_str,
                            err)
                    self.logger.warning(msg)
                    continue    

                # If received data is about inputs:
                if data_str[:3] == '210':
                    self.logger.info(self.IP + ': Input status: ' + data_bin)

                    for input_number in range(1, self.number_of_IOs + 1):       # For every input:
                        if data_bin[-input_number] == '1':                      # If input status is now 1:

                            # If server is GA and equipment was previously identified in database, requests access to database.
                            #access_response_type = 0
                            if self.global_access and self.equipment_number[input_number]:
                                
                                # Requesting access:
                                access_request_type = 4         # Button.
                                identifier_number   = ' '       # Can't be ''.
                                access_request_number, access_response_type = self.API.access_request(identifier_number, self.equipment_number[input_number], access_request_type)

                                # If equipment is blocked by escape route:
                                if self.blocked_by_route[input_number]:
                                    access_response_type = 20       
                                    
                                # Registering access and publishing to dashboard:
                                self.API.access_register_publish_thread(access_request_number, access_request_type, access_response_type)

                            # If server is not GA or if server is GA and request was allowed 4 - button (sensor), sets corresponding relay:
                            if not self.global_access or access_response_type == 4:
                                # Starts as thread to not interrupt the rest of the code (important to read inputs while relay setting is in motion).
                                threading.Thread(target = self.set_relays_local_and_remote,
                                                 name = f'set_relays_local_and_remote {self.IP}, {input_number}',
                                                 args = (input_number,)
                                                 ).start()

                                # Sending e-mail, if configured to do so and if input status changed (is now 1 and wasn't before):
                                if config_email.send_email_on_input_change and self.input_status[input_number] == 0:
                                        
                                    self.input_status[input_number] = 1         # Updating input status before sending email, so information on email is updated.

                                    subject = 'Input was turned on'
                                    msg = (f'On module {self.IP}\n' + 
                                          f'Input number {input_number}\n' + 
                                          f'{subject}.\n' +
                                          f'Input status: {self.input_status[1:]}\n' +
                                          f'Relay status: {self.relay_status[1:]}\n')
                                    self.email_controller.send_gmail_Thread(subject, msg)

                                else:                                           # If not sending email:
                                    self.input_status[input_number] = 1         # Updating input status.

                        elif data_bin[-input_number] == '0':                    # If input status is now 0:

                            # Resets relays (as thread to not interrupt the rest of the code (important to read inputs while relay setting is in motion)).
                            threading.Thread(target = self.reset_relays_local_and_remote,
                                             name = f'reset_relays_local_and_remote {self.IP}, {input_number}',
                                             args = (input_number,)
                                             ).start()

                            # Sending e-mail, if configured to do so and if input status changed (is now 0 and wasn't before):
                            if config_email.send_email_on_input_change and self.input_status[input_number] == 1:

                                self.input_status[input_number] = 0         # Updating input status before sending email, so information on email is updated.

                                subject = 'Input was turned off'
                                msg = (f'On module {self.IP}\n' + 
                                        f'Input number {input_number}\n' + 
                                        f'{subject}.\n' +
                                        f'Input status: {self.input_status[1:]}\n' +
                                        f'Relay status: {self.relay_status[1:]}\n')
                                self.email_controller.send_gmail_Thread(subject, msg)
                            
                            else:                                           # If not sending email:
                                self.input_status[input_number] = 0         # Updating input status.

                # If received data is about outputs (relays):
                elif data_str[:3] == '211':
                    #print(self.IP + 'Active relays: ' + format(data_int,'04b'))
                    pass

        except Exception as err:
            try:
                msg = 'Error in method {}.{}. From: IP: {}. Error message: {}'.format(
                    self.__class__.__name__,            # Ref. for getting class name on 2019-06-26:  https://stackoverflow.com/questions/510972/getting-the-class-name-of-an-instance
                    sys._getframe().f_code.co_name,     # Ref. for getting method name on 2019-06-26: https://stackoverflow.com/questions/251464/how-to-get-a-function-name-as-a-string-in-python
                    self.IP,
                    err)
                
                self.logger.error(msg)
            except Exception as err:
                msg = 'Exception occurred while treating another exception: {}'.format(err)
                print(msg)

        return

    def listen_to_serial(self, controlled_socket, conected_device):
        """Listens to serial, awaiting for RFID number.
        Should be called as thread to stay listening to client (or multiple clients) without interrupting code.
        """
        try:
            if self.global_access:
                # Identifying (only once) what equipment each port corresponds to:
                equipment_number, access_request_type, relay_number, _ = self.API.get_eqpt_parameters_by_IP_port(self.IP, controlled_socket.original_port)

            while self in self.module_list.list and controlled_socket.online in ('online', 'unknown'):   # While module in module_list and socket is online. Necessary for thread not to run indefinitely.
               
                # Listens for a string sent by this module and serial:
                msg_received = controlled_socket.communicate()      # Communicating via socket.

                if msg_received is False:                           # If socket broke communication, exits while loop.
                    break
                elif msg_received is None:                          # If received invalid message. 
                    continue                                        # Do nothing, but continue in the while loop.
                
                # Not necessary anymore because socket already treats message received. 
                ## Building string accordingly to device's specific behaviour.
                #msg_received = conected_device.get_identifier_from_string(msg_received)
                #if msg_received is None:                            # If any error
                #    continue                                        # Do nothing, but continue in the while loop.

                if self.global_access:
                    # If solution is GA, requests access:
                    if msg_received is not None and equipment_number is not None :

                        # Requesting access:
                        access_request_number, access_response_type = self.API.access_request(msg_received, equipment_number, access_request_type)

                        # If equipment is blocked by escape route:
                        if self.blocked_by_route[relay_number]:
                            access_response_type = 20       
                                    
                        # Registering access and publishing to dashboard:
                        self.API.access_register_publish_thread(access_request_number, access_request_type, access_response_type)

                        # If request was allowed (1 - entry, 2 - exit, 3 - exit by urn, 4 - button (sensor), 6 - entry/exit), sets relay:
                        if access_response_type in (1, 2, 3, 4, 6):

                            # If relay is already set and relay type is Mirror or Fixed, relay will be reset:
                            if self.relay_status[relay_number] == 'Set' and self.relay_timing[relay_number].upper() == 'MIRROR':
                                self.reset_relays_local_and_remote(relay_number)
                            # Otherwise (relay is not set) (of any type) or it is set, but it's type is temporary, relay will be set:
                            else:
                                self.set_relays_local_and_remote(relay_number)

                else:
                    # If solution is not GA, just prints received message:
                    if msg_received:   # If differente from None.
                        msg_error = 'Received message from {}:{}: {}.'.format(
                                self.IP, 
                                controlled_socket.original_port, 
                                msg_received)
                        self.logger.info(msg_error)

        except Exception as err:
            try:
                msg_error = 'Error in method {}.{}. From: IP: {}, Original port: {}. Error message: {}'.format(
                    self.__class__.__name__,            # Ref. for getting class name on 2019-06-26:  https://stackoverflow.com/questions/510972/getting-the-class-name-of-an-instance
                    sys._getframe().f_code.co_name,     # Ref. for getting method name on 2019-06-26: https://stackoverflow.com/questions/251464/how-to-get-a-function-name-as-a-string-in-python
                    self.IP, 
                    controlled_socket.original_port, 
                    err)
                
                self.logger.error(msg_error)
            except Exception as err:
                msg_error = 'Exception occurred while treating another exception: {}'.format(err)
                print(msg_error)

        return

    def start_socket(self, controlled_socket):
        """Initial setting for controlled socket.
        Super: 
        Starts thread accondingly to this specific socket's function.
        """
        try:
            _, socket_function, conected_device_description = config_equipment.server_ports[controlled_socket.original_port]  # Verifying port's function and connected device.

            if socket_function == 'IO':                                     # If this socket's function is IO:
                super().start_socket(controlled_socket)                     # Passing module's messages to controlled socket.
                controlled_socket.ping_thread()                             # Starting ping thread.
                self.sockets[0] = controlled_socket                         # Adding socket to modules' array.
                threading.Thread(target = self.listen_to_IO,                # Start listening to serial:
                                 name = 'listen_to_IO', 
                                 args = (controlled_socket,)
                                 ).start()

            elif socket_function.startswith('Serial'):                      # If this socket's function is to transmit serial.

                if conected_device_description == 'Acura AM-10':            # Getting kind of reader connected to module.
                    conected_device = acura.AM10()
                else:
                    msg = 'Error in method {}.{} for equipment with IP: {}, port #: {}. Unknown device connected to module.'.format(
                        self.__class__.__name__,
                        sys._getframe().f_code.co_name,
                        self.IP,
                        controlled_socket.original_port)
                    self.logger.error(msg)
                    return

                super().start_socket(controlled_socket, conected_device)    # Passing reader's messages to controlled socket.
                controlled_socket.ping_thread()                             # Starting ping thread.

                self.sockets[int(socket_function[-1])] = controlled_socket  # Adding socket to modules' dictionary.
                threading.Thread(target = self.listen_to_serial,            # Start listening to serial:
                                 name = 'listen_to_serial',
                                 args = (controlled_socket, conected_device)
                                 ).start()

            else:
                msg = 'Error in method {}.{} for equipment with IP: {}, port #: {}. Unknown port function.'.format(
                        self.__class__.__name__,
                        sys._getframe().f_code.co_name,
                        self.IP,
                        controlled_socket.original_port)
                self.logger.error(msg)
        
        except Exception as err:
            try:
                msg = 'Error in method {}.{} for equipment with IP: {}, port #: {}. Error message: {}'.format(
                    self.__class__.__name__,
                    sys._getframe().f_code.co_name,
                    self.IP,
                    controlled_socket.original_port,
                    err)
                self.logger.error(msg)
            except Exception as err:
                msg = 'Exception occurred while treating another exception: {}'.format(err)
                print(msg)

        return

    # Relay control methods:

    def set_module_relay(self, relay_number):
        """Sets Comm5 relay.
        (closes it, since they are Normally Open).
        """

        try:
            if self.sockets[0]:
                relay_number = int(relay_number)
                message = 'set {}'.format(relay_number)     # Building string to send, e.g., 'set 2'.
                self.send(message)

        except Exception as err:
            msg = 'Error in method Comm5.setModuleRelay(). IP: {}, relay: {}. Error message: {}'.format(self.IP, relay_number, err)
            self.logger.error(msg)

        return

    def reset_module_relay(self, relay_number):
        """Resets Comm5 relay
        (opens it, since they are Normally Open).
        """

        try:
            if self.sockets[0]:
                relay_number = int(relay_number)
                message = 'reset {}'.format(relay_number) # Building string to send, e.g., 'reset 2'.
                self.send(message)

        except Exception as err:
            msg = 'Error in method Comm5.resetModuleRelay(). IP: {}, relay: {}. Error message: {}'.format(self.IP, relay_number, err)
            self.logger.error(msg)

        return
