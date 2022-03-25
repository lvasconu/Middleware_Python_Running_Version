import socket
import threading

from controllers import list_controller, log_controller, socket_controller
from equipment_modules import config_equipment, comm5, wolpac

class ServerController:

    # Class variables:
    lock = threading.Lock()                             # Lock for multiple servers make alterations one at a time.
    module_list = list_controller.ListController()     # Controller that will access and manipulate one single list of equipment modules.
    logger = log_controller.LogController()            # Log controller.

    def __init__(self, port):
        """
        Creates a server to listen to any IP on 'port'.
        Being a separeted object, allows multiple servers to be created on different threads (to listen on diferent ports).
        """
           
        self.host = ''                                                                  # Host defines from what IP a connection should be awaited from. '' makes it accepts connections from any IP. Refs. on 2019-03-13: http://alissonmachado.com.br/socket-em-python/, https://docs.python.org/2/library/socket.html 
        self.original_port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)          # Creating server socket.
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)        # Setting socket to be reusable. Ref: https://docs.python.org/3/library/socket.html, https://www.youtube.com/watch?v=CV7_stUWvBQ
        self.server_socket.bind((self.host, self.original_port))                        # Binding this socket to a specific IP and port.
        self.server_socket.listen(5)                                                    # Listening. Parameter: Maximum number of queued connections. Ref. on 2018-10-19: https://docs.python.org/2/library/socket.html
        self.logger.info('Server listening on port {}.'.format(self.original_port))

        # Accepts connection, starts thread to communicate with client, repeats to accept next connection. 
        while True:
            module_socket, module_adress = self.server_socket.accept()                  # Accepts connection from module. Returns new socket and it's address (IP, port). Port is different from 'self.port', which is the original port, received as argument.
            
            threading.Thread(target = self.process_connection,
                                name = 'Server.processModule' + str(self.original_port), 
                                args = (module_socket, module_adress)
                                ).start()

        return

    def process_connection(self, module_socket, module_adress):
        """ Code below was separeted and invoked as thread so __init__ can return to accept new connections as soon as possible."""
        
        module_IP, module_port = module_adress                                          # Separating address into IP and port.
        self.logger.info('Client connected, address: ' + 
                                      '{}:{}'
                                      .format(module_IP, self.original_port))           # Logging.
        
        with self.lock:                                                                 # Locking so that multiple servers do not check and create multiple modules at the same time.
            
            module, _ = self.module_list.get_modules(IP = module_IP)                    # Checking to see if module already exists in list.

            if not module:                                                              # If module does not exist in module_list:
                module_model = config_equipment.server_ports[self.original_port][0]     # Verifying what kind of module connected (according to port number).
                
                # Creating new module object:
                if module_model == 'Comm5.MA':
                    module = comm5.MA(module_IP)
                elif module_model == 'Wolpac.Waffer':
                    module = wolpac.Waffer(module_IP)
                else: 
                    return

                # Adding new module to list:
                self.module_list.append(module)

            else:                                                                       # If module exists in module_list, get first (and only) module of array.
                module = module[0]
        
        """ Code below put outside lock because ServerController has to be locked for the smallest amount of time possible.
            ServerController must return quickly to accept and process new coonections. 
            The problem emerged when 2 Waffers tryed to connect simoutanously. Only one successfully connected. The other was put in the the module_list, but was inoperative. It was also not removed from module_list.
        
        """
        controlled_socket = socket_controller.SocketController(module_socket, self.original_port)      # Creating socket controller.
        module.start_socket(controlled_socket)                                          # Passes socket to existig module and starts it.
            
        self.logger.info(self.module_list.to_string())                                  # Printing updated module_list.
             
        # Setting or resetting module every new connection (if new connection is after some seconds).
        # For resetting purposes, it's better to leave it outside 'if module == None'. For instance, if module is turned off and on quickly, before being removed from module list.
        module.set_initial_settings_thread()

        return