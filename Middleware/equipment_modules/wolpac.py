# Import section:
import threading
import sys
from datetime import datetime
from time import sleep

from controllers import email_controller, socket_controller
from equipment_modules import generic_module

class Waffer(generic_module.GenericModule):
    # Ref: "Instruções para Integração com WKCIV v1.10.25 15/09/2010", available in "Equipamentos\Catracas - Wolpac".

    # Class variables:
    ping_interval = 1                               # Interval between sending each ping message [s]

    # Default messages:
    msg_beggining                   = '\x10\x02'                    # Hex: 10 02,   DLE STX
    msg_end                         = '\x10\x03'                    # Hex: 10 03,   DLE ETX
    msg_identification_beggining    = 'N'                           # Hex: 4E,      UTF-8: N.
    msg_ack                         = 'EE'                          # Hex: 45 45,   UTF-8: EE.
    msg_ping                        = f'{msg_beggining}K{msg_end}'  # Hex: 4B,      UTF-8: K. 
    msg_ping_response               = f'{msg_beggining}K{msg_end}'  # Hex: 4B,      UTF-8: K. 
    msg_code = {
        'mode_default'      : 'eNT0',                               # Middleware C#: UTF-8: eNT0.
        #'mode_block'        : 'eBT0',                               # Middleware C#: Couldn't find a code to block. Probabaly was using same as mode_default. From manual p.39: eBT0.
        'mode_allow_turn'   : 'eL40',                               # Middleware C#: eL40.
        'mode_drop_arm'     : 'eL00',                               # Middleware C#: eL00.
        
        'sync_clock'        : 'VH',                                 # To update clock: msg_beggining + sync_clock + date_time + msg_end
        }
    """ Middleware in C# informs:
        PING_WOLPAC:             4B (K in UTF-8)
        RETORNO_PING_WOLPAC:     6B (k in UTF-8)
        In the logic in Middleware C#, Wolpac pings Middleware with K (PING_WOLPAC) and Middleware responds with k (RETORNO_PING_WOLPAC) ?
    """

    def __init__(self, IP):

        # Initializing generics (super class' __init__):
        super(self.__class__, self).__init__(IP)  # https://stackoverflow.com/questions/3694371/how-do-i-initialize-the-base-super-class
         
        # Getting equipment number and parameters from database:
        self.equipment_number[0], self.parameters, _ = self.API.get_eqpt_parameters(self.IP)

        self.access_request_number = None       # To be used on register access:
        
        self.delayed_send_allowed = False       # Boolean to allow delayed messages to be sent to Waffer or not.

        return

    def start_socket(self, controlled_socket):
        """ Initial setting for controlled socket.
        Super: 
        Starts thread accondingly to this specific socket's function.
        """
        try:
            super().start_socket(controlled_socket)         # Passing module's messages to controlled socket.
            self.sockets[0] = controlled_socket             # Adding socket to modules' array

            msg_received = self.communicate()

            if msg_received and msg_received.startswith(self.__class__.msg_identification_beggining):   # If received connection/identification message,
                self.send(msg_received)                                                                 # sends it to back confirm connection.

            controlled_socket.ping_thread()                 # Starting ping thread. Has to be started after connection confirmation.
            
            threading.Thread(target = self.listen,          # Start listening:
                            name = 'listen', 
                            args = ()
                            ).start()

            # Waffer does not accept some commands right after turning on.
            self.delayed_send_allowed = False               # Boolean to allow delayed messages to be sent to Waffer or not.
            threading.Thread(target = self.send_delayed_timer,
                name = 'send_delayed_timer', 
                args = ()
                ).start()

            threading.Thread(target = self.sync_clock,      # Syncing Waffer clock with Middleware.
                name = 'sync_clock', 
                args = ()
                ).start()

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

    def listen(self):
        """ Starts listening (waiting) for communication.
        and act accordingly.
        """
        try:

            while self in self.module_list.list and self.sockets[0].online in ('online', 'unknown'):    # While module in module_list and socket is online. Necessary for thread not to run indefinitely.
            
                msg_received = self.communicate()
                #print(f'msg_received: {msg_received}')

                if msg_received is False:               # Client gracefully closed connection
                    msg_log = f'{self.IP}: Client gracefully closed connection.'
                    self.logger.warning(msg_log)
                    break

                # WKCIV sent keep alive message.
                elif msg_received == 'k':
                    self.send('k')                      # Sending it back to confirm connection.

                # If message is return to state change command: 
                elif msg_received == 'eS' :
                    msg_log = f'{self.IP}: State change command: Accepted.'
                    self.logger.info(msg_log)

                elif msg_received == 'eN' :
                    msg_log = f'{self.IP}: State change command: Syntax error.'
                    self.logger.error(msg_log)

                # If message has lenght 64 and starts with '11', event occourred. Example: '110123092020170110                 05X            2309201701111 '
                elif len(msg_received) == 64 and msg_received[0:2] == '11' :
                        
                    """ Aswering with ack.
                    Ref. Manual: 'Exceto os eventos de comunicação (60 e 62),
                    todos os demais (eventos reais) devem ser quitados pelo sistema com a mensagem: EE
                    sem a qual não serão retirados da fila de transmissão.'"""
                    if msg_received[16:18] not in ('60', '62'):
                        self.send(self.msg_ack)

                    #time = f'20{msg_received[54:56]}-{msg_received[52:54]}-{msg_received[50:52]} {msg_received[56:58]}:{msg_received[58:60]}:{msg_received[60:62]}'

                    if   msg_received[16:18] == '01':           # Equipment turned on.
                        msg_log = f'{self.IP}: Equipment turned on'
                        self.logger.info(msg_log)
                        
                    elif msg_received[16:18] == '02':           # Equipment connected.
                        msg_log = f'{self.IP}: Equipment connected.'
                        self.logger.info(msg_log)

                    elif msg_received[16:18] == '10':           # Equipment disconnected.
                        msg_log = f'{self.IP}: Equipment disconnected'
                        self.logger.warning(msg_log)

                    elif msg_received[16:18] in ('34'):         # Entry made.
                        msg_log = f'{self.IP}: Entry made'
                        self.API.access_register_publish_thread(self.access_request_number, access_made_type = 1)   # Registering and publishing (to dashboard) access.
                        self.logger.info(msg_log)

                    elif msg_received[16:18] in ('35'):         # Exit made.
                        self.API.access_register_publish_thread(self.access_request_number, access_made_type = 2)   # Registering and publishing (to dashboard) access.
                        msg_log = f'{self.IP}: Exit made'
                        self.logger.info(msg_log)

                    elif msg_received[16:18] == '40':           # Access denied in offline mode. In C# says "Evento de acesso negado em modo off-line recebido"
                        msg_log = f'{self.IP}: Access denied.'
                        self.logger.info(msg_log)

                    elif msg_received[16:18] == '49':           # Timeout.
                        self.API.access_register_publish_thread(self.access_request_number, access_made_type = 14)  # Registering and publishing (to dashboard) access.
                        msg_log = f'{self.IP}: Timed out'
                        self.logger.info(msg_log)

                    elif msg_received[16:18] == '60':           # Received pseudo-ACK.
                        msg_log = f'{self.IP}: Received pseudo-ACK.'
                        self.logger.info(msg_log)

                    elif msg_received[16:18] == '62':           # Received pseudo-NACK.
                        msg_log = f'{self.IP}: Received pseudo-NACK.'
                        self.logger.info(msg_log)

                    else:                                       # Unknown event.
                        msg_log = f'IP {self.IP} sent unknown event message: {msg_received}'
                        self.logger.warning(msg_log)

                # If message has lenght 64 and starts with '00', card was passed in a reader. Example: '004178797349                                      23092016565890'
                elif len(msg_received) == 64 and msg_received[0:2] == '00' :

                    # Getting identifier number:
                    identifier_number_received = msg_received[2:50]             # Identifier number, with length 48.  
                    identifier_number_decimal = int(identifier_number_received) # Converting to decimal.
                    identifier_number_hex = hex(identifier_number_decimal)      # Converting to hex.
                    identifier_number_str = str(identifier_number_hex)[2:]      # converting to string and removing '0x'

                    # Getting reader number in which identifier was passed:
                    reader_number_message_srt = msg_received[-2:]
                    reader_number_message_int = int(reader_number_message_srt)
                    if reader_number_message_int == 70:
                        reader_number = 'Teclado'
                    elif reader_number_message_int == 80:
                        reader_number = '1'
                    elif reader_number_message_int == 90:
                        reader_number = '2'
                    elif reader_number_message_int in (98, 99):
                        reader_number = '3'
                    else:
                        reader_number = None

                    # If got equipment parameters from database:
                    access_response_type = None
                    if self.parameters:

                        # Getting access request type:
                        access_request_type =  self.parameters['TIPO_ACESSO_LEITOR' + reader_number]                                                                   
                        # Requesting access:
                        self.access_request_number, access_response_type = self.API.access_request(identifier_number_str, self.equipment_number[0], access_request_type)  

                        # If equipment is blocked by escape route:
                        if self.blocked_by_route[0]:
                            access_response_type = 20

                        # Getting turn code.
                        turn_code = self.get_turn_code(access_response_type)
                        # Getting LCD messages code.
                        txt_lcd_up , txt_lcd_down = self.get_lcd_texts(access_request_type, access_response_type)
                            
                        # Building string to be sent to Wolpac. 
                        msg_to_send =   'V8{}{}{}{}{}{}{}'.format(                        
                                        identifier_number_received[0:30],                   # Sending identifier number back.
                                        turn_code,                                          # Code that allows turn (or not) (and lights up led).
                                        txt_lcd_up,                                         # LDC message, upper part.
                                        txt_lcd_down,                                       # LDC message, lower part.
                                        str(int(self.parameters['TIMEOUT_ACESSO'])/10),     # Timeout (integer part). Timeout in front end is in tenths of seconds.
                                        str(int(self.parameters['TIMEOUT_ACESSO'])%10),     # Timeout (modulus part)
                                        reader_number_message_srt                           # Message corresponding to reader number.
                                        )                          

                        #print('msg_to_send: ' + str(msg_to_send))
                        self.send(msg_to_send)

                        # If access was denied (5, 7 to 21), register it:
                        if access_response_type == 5 or access_response_type >= 7:
                            self.API.access_register_publish_thread(self.access_request_number, access_response_type = access_response_type)
                    
                # If module sent unexpected message:
                else:
                    msg_log = f'IP {self.IP} sent unknown message: {msg_received}'
                    self.logger.warning(msg_log)

        except Exception as err:
            try:
                msg_log = 'Error in method {}.{}. From: IP: {}. Error message: {}'.format(
                    self.__class__.__name__,
                    sys._getframe().f_code.co_name,
                    self.IP,
                    err)
                
                self.logger.error(msg_log)
            except Exception as err:
                msg_log = 'Exception occurred while treating another exception: {}'.format(err)
                print(msg_log)

        return

    def send_delayed(self, msg):
        """ This auxiliaty method sends message only some seconds after Waffer connected.
        Necessary because Waffer does not accept some commands right after turning on.
        Status is monitored by boolean variable 'delayed_send_allowed', changed by method send_delayed_timer().
        """

        # While delayed sending is not yet allowed, waits:
        while not self.delayed_send_allowed:
            sleep(1)

        # When delayed sending becames allowed, sends message:
        self.send(msg)

        return

    def send_delayed_timer(self):
        """ Changes status of boolean variable 'delayed_send_allowed'
        to True
        after some seconds
        to delay some messages to be sent to Waffer.
        """
        if not self.delayed_send_allowed:
            sleep(5)
            self.delayed_send_allowed = True

        return

    def sync_clock(self):
        """ Syncs Wolpac's clock with middleware. """

        # Building string in format VH150920180345
        msg =  self.msg_code['sync_clock'] + datetime.now().strftime('%d%m%y%H%M%S') # Ref: https://stackoverflow.com/questions/311627/how-to-print-a-date-in-a-regular-format

        # Sending message delayed. If sync command is sent right after connection, causes connection error. Don't  know why.
        self.send_delayed(msg)

        msg_log = f'{self.IP}: Syncing clock on equipment.'
        self.logger.info(msg_log)

        return

    def get_lcd_texts(self, access_request, access_response):
        """ Getting LCD messages to be sent to Wolpac. 
        Each line supports 16 characters.
        """

        if access_response == 1: # Entry.
            txt_lcd_up      = '   BEM VINDO    '
            txt_lcd_down    = 'Entrada autoriza'

        elif access_response in (2, 3): # Exit or exit by urn.
            txt_lcd_up      = '  VOLTE SEMPRE  '
            txt_lcd_down    = 'Saída autorizada'

        elif access_response in (4, 6): # Button or Entry/Exit.
            txt_lcd_up      = '     ACESSO     '
            txt_lcd_down    = '   AUTORIZADO   '

        elif access_response == 12: # Entry already made.
            txt_lcd_up      = ' ACESSO NEGADO  '
            txt_lcd_down    = ' SOLICITE SAIDA '

        elif access_response == 13: # Exit already made.
            txt_lcd_up      = ' ACESSO NEGADO  '
            txt_lcd_down    = 'SOLICITE ENTRADA'

        elif access_response == 18: # Drop card on urn.
            txt_lcd_up      = '    DEPOSITE    '
            txt_lcd_down    = '     CARTAO     '

        elif access_response == 20: # Equipment blocked (by escape route).
            txt_lcd_up      = '   EQUIPAMENTO  '
            txt_lcd_down    = '   BLOQUEADO    '

        else:
            if access_request == 1:
                txt_lcd_up      = '    ENTRADA     '
                txt_lcd_down    = ' NAO AUTORIZADA '
            elif access_request in (2, 3):
                txt_lcd_up      = '     SAÍDA      '
                txt_lcd_down    = ' NAO AUTORIZADA '
            else:
                txt_lcd_up      = '    ACESSO      '
                txt_lcd_down    = ' NAO AUTORIZADO '

        return txt_lcd_up, txt_lcd_down

    def get_turn_code(self, access_response_type):
        """ Gets turn code (to be sento to Wolpac) accordingly to access response type."""

        if access_response_type == 1:           # Entry
            turn_code =  '5'
        elif access_response_type in (2, 3, 4): # Exit, exit by urn, button.
            turn_code =  '6'
        elif access_response_type == 6:         # Entry/exit.
            turn_code =  '7'
        else:                                   # All the others (not allowed)
            turn_code =  '3'

        return turn_code

    # Escape route methods:

    def passage_block(self, relay_number = 0, escape_route_number = True, test = True):
        """ Blocks equipment.
            Method to be used when Escape Route is activated.
        """
        
        if self.blocked_by_route[relay_number]:                         # If equipment is already blocked by a escape route.
            return False

        else:
            self.block_equipment(relay_number, escape_route_number)     # Blocks relay to not receive other commands (not even escape routes).
            #print(f'passage_block. blocked by route: {self.blocked_by_route}')
            return True

    def passage_allow_soft(self, relay_number = 0, escape_route_number = True, test = False):
        """ Allow people to pass without identification. 
            Method to be used when Escape Route is activated.
            Difference between modes soft and hard depends on specific equipment module.

            In Waffer, alows turnstiles to turn, without dropping it's arm.
        """
        if self.blocked_by_route[relay_number]:                         # If equipment is already blocked by a escape route.
            return False

        else:
            if not test:
                self.send_delayed(self.msg_code['mode_allow_turn'])
            self.block_equipment(relay_number, escape_route_number)     # Blocks relay to not receive other commands (not even escape routes).
            #print(f'passage_allow_soft. blocked by route: {self.blocked_by_route}')
            return True

    def passage_allow_hard(self, relay_number = 0, escape_route_number = True, test = False):
        """ Allow people to pass without identification. 
            Method to be used when Escape Route is activated.
            Difference between modes soft and hard depends on specific equipment module.

            In Waffer, sends command to drop turnstile arm.
        """
        if self.blocked_by_route[relay_number]:                         # If equipment is already blocked by a escape route.
            return False

        else:
            if not test:
                self.send_delayed(self.msg_code['mode_drop_arm'])
            self.block_equipment(relay_number, escape_route_number)     # Blocks relay to not receive other commands (not even escape routes).
            #print(f'passage_allow_hard. blocked by route: {self.blocked_by_route}')
            return True

    def passage_normalize(self, relay_number = 0, escape_route_number = True, test = False):
        """ Normalize equipment operation, after Escape Route is deactivated.
            Method to be used when Escape Route is activated.
        """

        unblocked = self.unblock_equipment(relay_number, escape_route_number)   # Unblocks relay to receive commands.
        if unblocked:                                                           # If successfully unblocked (escape route was the same that blocked).
            if not test:
                self.send_delayed(self.msg_code['mode_default'])
            #print(f'passage_normalize. blocked by route: {self.blocked_by_route}')
            return True
        else:
            return False

if __name__ == "__main__":
    # Code for testing
    import socket

    host = ''                                                                       # Host defines from what IP a connection should be awaited from. '' makes it accepts connections from any IP. Refs. on 2019-03-13: http://alissonmachado.com.br/socket-em-python/, https://docs.python.org/2/library/socket.html 
    port = 1234
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)               # Creating server socket.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)             # Setting socket to be reusable. Ref: https://docs.python.org/3/library/socket.html, https://www.youtube.com/watch?v=CV7_stUWvBQ
    server_socket.bind((host, port))                                                # Binding this socket to a specific IP and port.
    server_socket.listen(5)                                                         # Listening. Parameter: Maximum number of queued connections. Ref. on 2018-10-19: https://docs.python.org/2/library/socket.html
    print('Server listening on port {}.'.format(port))

    # Accepts connection, starts thread to communicate with client, repeats to accept next connection. 
    while True:
        module_socket, module_adress = server_socket.accept()                       # Accepts connection from module. Returns new socket and it's address (IP, port). Port is different from 'port', which is the original port, received as argument.
        module_IP, module_port = module_adress                                      # Separating address into IP and port.
        print('Client connected, address: {}:{}. Original port: {}'.format(module_IP, module_port, port))
            
        #controlled_socket = socket_controller.SocketController(module_socket, port, test = True)

        #module = Wolpac_Waffer(controlled_socket)
        
        # Echo server:
        while True:
            msg_received = module_socket.recv(1024)

            if not len(msg_received):                               # Equivalente to: "if len(receivedMessage) == 0".
                msg_received = 'Connection on {}:{} closed remotely but gracefully.'.format(self.IP, self.original_port)

            print(msg_received)
            module_socket.sendall(msg_received)
                
            