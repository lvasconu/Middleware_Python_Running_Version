# This class is meant to be the super class for the other [specific] modules.

# Import section:
import threading
from time import sleep
import importlib
import sys

from config_files import config_email, config_simple_database, config_global_access
from controllers import email_controller, list_controller, log_controller
from global_access import api_controller
from equipment_modules import config_equipment
from sensors import acura

class GenericModule():

    # Class variables:
    global_access = config_global_access.global_access      

    module_list = list_controller.ListController() # Controller that will access and manipulate one single list of modules.
    logger = log_controller.LogController()        # Log controller.

    sleep_time_default = 3                          # Default sleep time, used for temporary relays.
    number_of_IOs = 0                               # Number of IOs (inputs and relays) each to be considered in each module. 
    ping_interval = 3                               # Time between ping messages [s].

    # Default messages:
    msg_beggining = None                            # Message that will be used at the beggining of full messages.
    msg_end = None                                  # Message that will be used at the end of full messages.
    msg_identification_beggining = None             # Message that equipment sends to identify itself.
    msg_ack = None                                  # Message sent to ack.
    msg_ping = 'generic_ping'                       # Message that Middleware will send to equipment to ping.
    msg_ping_response = None                        # Expected message that equipment will send Middleware as response to ping.
    msg_to_ignore = None                            # Message to be ignored when received.

    # Initializing methods:

    def __init__(self, IP):

        # Constant parameters:
        self.IP = IP

        # Controllers:
        self.API = api_controller.ApiController()                   # In GA solution, controller to access to database:
        self.email_controller = email_controller.EmailController()  # E-mail controller. TODO: move to class variables.

        # Arrays and dictionaries:
        # For relays:
        self.blocked_by_route   = [None]    * (self.number_of_IOs + 1)  # Array used to block commands for each relay (used in scape routes).
        self.relay_type         = [None]    * (self.number_of_IOs + 1)  # Array used set the relay type ('NO' or 'NC').
        self.relay_timing       = [None]    * (self.number_of_IOs + 1)  # Array used set the relay timing ('Temporary', 'Mirror' or 'Fixed').
        self.relay_status       = ['Reset'] * (self.number_of_IOs + 1)  # Relay status at each moment.
        # For inputs:
        self.input_addresses    = [None]    * (self.number_of_IOs + 1)  # Input addresses (what relays to set when input is on). Default: relay of same number, in the same module.
        self.input_status       = [0]       * (self.number_of_IOs + 1)  # Input status. Useful when it is needed to know if status changed. E.g. to decide when to send emails. 
        # Sockets:
        self.sockets            = [None]    * (self.number_of_IOs + 1)  # Socket array.
        # For equipment (if in Global Access solution):
        self.equipment_number   = [None]    * (self.number_of_IOs + 1)  # ID of the equipment connected on each relay (if using Global Access complete solution).

        # Variables to avoid multiple connections for same module firing up unnecessary methods repeatedly.
        self.allow_set_initial_settings = True                          # Variable used to not have several threads calling listenToIO. Used by method monitorSetInitialSettings().
        self.lock = threading.Lock()                                    # Lock so that multiple threads not access methods at same time.

        return

    def set_initial_settings_thread(self):
        """ Invoking method as thread to run in parallel."""
        threading.Thread(target = self.set_initial_settings,
                    name = 'setInitialSettings',
                    args = ()
                    ).start()
        return

    def set_initial_settings(self):
        """ Sets and gets initial settings.
            Separated from __init__ so:
            Code runs after putting module in module_list, making possible for 'while self in module_list.list' loops to work.
            Initial settings can be reset in case module went offline and then on again, without time to be removed from module_list.
        """

        try:
            #To avoid multiple clients to call set_initial_settings() method at once (necessary for modules that use several ports, such as Comm5):
            with self.lock:                                     # Locking to avoid parallel calls.
                if self.allow_set_initial_settings == True:     # Variable is True only after some second after previous calling.

                    self.monitor_set_initial_settings_thread()  # Blocking calls of setInitialSettings() for some seconds.

                    self.blocked_by_route   = [None]   * (self.number_of_IOs + 1) # Resetting blocked status in case module was rebooted when Escape Route was active.

                    # If running as basic solution, reloads database to see if there are changes.
                    if self.global_access:
                        importlib.reload(config_simple_database)

                    # Gets IO parameters from database and resets relays.   
                    self.get_eqpt_by_IP_relay_Thread()

                    # Method to watch Socket_controllers and remove module from module_list when necessary.
                    self.remove_from_module_list_thread()
       
        except Exception as err:
            try:
                msg = 'Error in method {}.{}. From: IP: {}. Error message: {}'.format(
                    self.__class__.__name__,                # Ref. for getting class name on 2019-06-26:  https://stackoverflow.com/questions/510972/getting-the-class-name-of-an-instance
                    sys._getframe().f_code.co_name,         # Ref. for getting method name on 2019-06-26: https://stackoverflow.com/questions/251464/how-to-get-a-function-name-as-a-string-in-python
                    self.IP,
                    err)
                self.logger.error(msg)
            except Exception as err:
                msg = 'Exception occurred while treating another exception: {}'.format(err)
                print(msg)

        return
    
    def remove_from_module_list_thread(self):
        """Invoking method as thread to run in parallel."""
        threading.Thread(target = self.remove_from_module_list,
                    name = 'removeFromModuleList' + self.IP,
                    args = ()
                    ).start()

        return

    def remove_from_module_list(self):
        """Removes module of module_list if no socket is online."""
        
        try:
            try_var = 1                             # Number of current verification try.
            try_max = 3                             # Maximum number of verifications that will be made.
            interval = 5                            # Interval (in seconds) between each verification,

            while self in self.module_list.list \
                and try_var <= try_max:             # While module in module_list and not all tries have been made.
                sleep(interval)                     # Sleeps for 'interval' seconds.              
                
                all_sockets_offline = True          # Are all sockets (of this module) offline?
                for sock in self.sockets:
                    if sock != None and sock.online in ('online', 'unknown'):   # If even one of SocketControllers is online or unkown:
                        try_var = 1                                             # Resets number of tries.
                        all_sockets_offline = False                             # Not all sockets are offline.
                        break                                                   # Breaks the for loop (but not the while loop).

                # If all SocketControllers are offline:
                if all_sockets_offline:
                    if try_var < try_max:               # If did not try 'try_max' times yet:
                        msg = 'All SocketControllers offline for module {}, try {}/{}.'.format(self.IP, try_var, try_max)
                        self.logger.warning(msg)
                        try_var += 1                    # If all SocketControllers are offiline, iterates counter.
                    else:                               # If already tried 'try_max' times:
                        self.module_list.remove(self)   # Removes controller from module_list.,
                        msg = 'All SocketControllers offline for module {}, try {}/{}. Module removed from module_list.'.format(self.IP, try_var, try_max)
                        self.logger.warning(msg)
            
        except Exception as err:
            try:
                msg = 'Error in method {}.{}. From: IP: {}. Error message: {}'.format(
                    self.__class__.__name__,                # Ref. for getting class name on 2019-06-26:  https://stackoverflow.com/questions/510972/getting-the-class-name-of-an-instance
                    sys._getframe().f_code.co_name,         # Ref. for getting method name on 2019-06-26: https://stackoverflow.com/questions/251464/how-to-get-a-function-name-as-a-string-in-python
                    self.IP,
                    err)
                self.logger.error(msg)
            except Exception as err:
                msg = 'Exception occurred while treating another exception in Comm5.removeFromModuleList(): {}'.format(err)
                print(msg)

    # Communications methods:
    def listen_to_IO(self, controlledSocket):
        pass

    def monitor_set_initial_settings_thread(self):
        """Invoking method as thread to run in parallel."""
        threading.Thread(target = self.monitor_set_initial_settings,
                    name = 'module.monitorSetInitialSettings',
                    args = ()
                    ).start()
        return

    def monitor_set_initial_settings(self):
        """Method monitors variable allowNewListenToIO, which:
            Is used to not have several threads calling listenToIO in parallel.
            Allows listenToIO when True.
        Method sets variable to False and resets it to True after 'timer' seconds. This is necessary when module is reset quicker than method ping can remove it from module list.
        """

        self.allow_set_initial_settings = False     # Blocking calls of setInitialSettings().

        sleep(10)                                   # Seconds before allowing another call of setInitialSettings() method.

        self.allow_set_initial_settings = True      # Allowing calls of setInitialSettings().

        return

    def start_socket(self, controlled_socket, module_or_reader = None):
        """Initializing settings for controlled socket, such as:
        Passing down modules specific messages.
        """

        # If no specific module_or_reader was informed, use this module's parameters;
        if not module_or_reader :
            module_or_reader = self

        # If messages exist, passing module/reader's begginging and end messages.
        if hasattr(module_or_reader, 'msg_beggining') or hasattr(module_or_reader, 'msg_end') :
            controlled_socket.set_message_beggining_and_end(module_or_reader.msg_beggining, module_or_reader.msg_end)      
            
        # If messages exist, passing module/reader's module's ping messages.
        if hasattr(module_or_reader, 'msg_ping') or hasattr(module_or_reader, 'msg_ping_response') :
            controlled_socket.set_ping_messages(module_or_reader.msg_ping, module_or_reader.msg_ping_response)

        # If messages exist, passing module/reader's ping interval.
        if hasattr(module_or_reader, 'ping_interval') :
            controlled_socket.ping_interval = module_or_reader.ping_interval

        # If messages exist, passing module/reader's ping interval.
        if hasattr(module_or_reader, 'msg_to_ignore') :
            controlled_socket.msg_to_ignore = module_or_reader.msg_to_ignore

        return

    def send(self, msg, socket_index = 0):
        """Auxiliary method to send messages via socket.
        If socket_index is informed, uses informed controlled socket.
        Otherwise, assumes sockets[0]
        """
        self.sockets[socket_index].queue_to_send(msg)
        return

    def communicate(self, socket_index = 0):
        """Auxiliary method to communicate messages via socket.
        If socket_index is informed, uses informed controlled socket.
        Otherwise, assumes sockets[0]
        """
        return self.sockets[socket_index].communicate()

    # Database/API methods:

    def get_eqpt_by_IP_relay_Thread(self):
        """Invoking method as thread to run in parallel."""
        threading.Thread(target = self.get_eqpt_by_IP_relay,
                    name = 'module.get_eqpt_by_IP_relay',
                    args = ()
                    ).start()
        return

    def get_eqpt_by_IP_relay(self):
        """ Gets IO parameters from database and resets relays.
            Relays:
                Gets type: 'NO' or 'NC'.
                Gets activation method: 'Temporary', 'Mirror' or 'Fixed'.
                Resets then to default states.
            Inputs:
                Gets addresses where to send commmands.
        """
        try:
            # Prealocating variables so 'msg' doesn't crash if error occour in previous part of code.
            nu_IO = 'None'

            # If type of solution is Global Access:
            if self.global_access:
                for nu_IO in range(1, self.number_of_IOs + 1):
                    self.equipment_number[nu_IO], self.relay_type[nu_IO], self.relay_timing[nu_IO], self.input_addresses[nu_IO], _ = self.API.get_eqpt_parameters_by_IP_relay(self.IP, nu_IO)

            else:         
                for module in config_simple_database.module_parameters:         # For every module in config file.
                    if module[0] == self.IP :                                   # If IP in that module is the IP of this module.
                        for nu_IO in range (1, self.number_of_IOs + 1):         # For every IO:
                            self.relay_type[nu_IO]       = module[1][nu_IO - 1] # Gets relay type ('NO' or 'NC').
                            self.relay_timing[nu_IO]     = module[2][nu_IO - 1] # Gets relay timing ('Temporary' or 'Fixed').
                            self.input_addresses[nu_IO]  = module[3][nu_IO - 1] # Gets inputs addresses.

                        break   # Breaks the for loop. If it has found the corresponding module, doesn't have to go through all the module list.

            # Resetting input and relays to default status:
            for IO in range (1, self.number_of_IOs + 1):
                #self.inputStatus[IO] = 0
                self.reset_relay(IO)

        except Exception as err:
            try:
                msg = 'Error in method {}.{} for equipment with IP: {}, IO #: {}. Error message: {}'.format(
                    self.__class__.__name__,            # Ref. for getting class name on 2019-06-26:  https://stackoverflow.com/questions/510972/getting-the-class-name-of-an-instance
                    sys._getframe().f_code.co_name,     # Ref. for getting method name on 2019-06-26: https://stackoverflow.com/questions/251464/how-to-get-a-function-name-as-a-string-in-python
                    self.IP,
                    nu_IO,
                    err)
                self.logger.error(msg)
            except Exception as err:
                msg = 'Exception occurred while treating another exception: {}'.format(err)
                print(msg)

        return

    # Escape route methods:

    def passage_block(self, relay_number = 0, escape_route_number = True, test = False):
        """ Blocks equipment.
            Method to be used when Escape Route is activated.
        """
        if self.blocked_by_route[relay_number]:                             # If equipment is already blocked by a escape route.
            return False

        else:
            if not test:
                self.reset_relay(relay_number)                              # Resets relay.
            self.block_equipment(relay_number, escape_route_number)         # Blocks relay to not receive other commands (not even escape routes).
            return True

    def passage_allow_soft(self, relay_number = 0, escape_route_number = True, test = False):
        """ Allow people to pass without identification. 
            Method to be used when Escape Route is activated.
            Difference between modes soft and hard depends on specific equipment module.
        """

        if self.blocked_by_route[relay_number]:                             # If equipment is already blocked by a escape route.
            return False

        else:
            if not test:
                self.set_relay(relay_number)                                # Sets relay
            self.block_equipment(relay_number, escape_route_number)         # Blocks relay to not receive other commands (not even escape routes).
            return True

    def passage_allow_hard(self, relay_number = 0, escape_route_number = True, test = False):
        """ Allow people to pass without identification. 
            Method to be used when Escape Route is activated.
            Difference between modes soft and hard depends on specific equipment module.

            It modules in general, there is no difference between passage_allow_soft and passage_allow_hard. E.g. Comm5.MA, Acura, Impinj.
        """

        return self.passage_allow_soft(relay_number, escape_route_number, test)

    def passage_normalize(self, relay_number = 0, escape_route_number = True, test = False):
        """ Normalize equipment operation, after Escape Route is deactivated.
            Method to be used when Escape Route is activated.
        """
        
        unblocked = self.unblock_equipment(relay_number, escape_route_number)   # Unblocks relay to receive commands.
        if unblocked:                                                           # If successfully unblocked (escape route was the same that blocked).
            if not test:
                self.reset_relay(relay_number)                                  # Resets relay
            #print(f'passage_normalize. blocked by route: {self.blocked_by_route}')
            return True
        else:
            return False

    def block_equipment(self, relay_number = 0, escape_route_number = True):
        """ Blocks equipment.
        Necessary when Escape Route is actived.
        User has to inform:
            Relay number to be blocked, if there is more than one relay.
            Escape route number.
        """

        try:
            relay_number = int(relay_number)

            if not self.blocked_by_route[relay_number]:                     # If relay is not already blocked:
                self.blocked_by_route[relay_number] = escape_route_number   # Blocks it (by this particular escape route).
                return True
            else:
                return False

        except Exception as err:
            msg = 'Error in method {}.{}. From: IP: {}, relay: {}, escape route: {}. Error message: {}'.format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                self.IP, 
                relay_number,
                escape_route_number,
                err)
            self.logger.error(msg)

            return None, msg

    def unblock_equipment(self, relay_number = 0, escape_route_number = True):
        """ Unblocks equipment.
        Necessary when Escape Route is actived.
        User has to inform:
            Relay number to be unblocked, if there is more than one relay.
            Escape route number.
        """
        try:
            relay_number = int(relay_number)

            if self.blocked_by_route[relay_number] == escape_route_number:  # If relay is blocked by this particular escape route:
                self.blocked_by_route[relay_number] = None                  # Unblocks it.
                return True
            else:
                return False

        except Exception as err:
            msg = 'Error in method {}.{}. From: IP: {}, relay: {}, escape route: {}. Error message: {}'.format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                self.IP, 
                relay_number,
                escape_route_number,
                err)
            self.logger.error(msg)

            return None, msg

    # Relay control methods:

    def set_module_relay(self, relay_number):
        pass

    def reset_module_relay(self, relay_number):
        pass

    def set_relay(self, relay_number):
        """Sets relay:
            Closes relay if NO and opens relay if NC.
            If relay is 'Temporary', waits for 'sleepTime' and resets it.
            (if relay is not blocked).
        """
        try:
            relay_number = int(relay_number)

            # If relay is blocked, do nothing.
            if self.blocked_by_route[relay_number]:
                return False

            # If relay is not blocked:
            else:

                # If relay's default state is NC, opens:
                if self.relay_type[relay_number] == 'NC':
                    self.reset_module_relay(relay_number)
                    self.relay_status[relay_number] = 'Set' # Storing relay status:
                    return True, 'NC'

                # Otherwise, relay is assumed to be NO and closes:
                else:
                    self.set_module_relay(relay_number)
                    self.relay_status[relay_number] = 'Set' # Storing relay status:
                    return True, 'NO'

        except Exception as err:
            msg = 'Error in method {}.{}. From: IP: {}, relay: {}. Error message: {}'.format(
            self.__class__.__name__,
            sys._getframe().f_code.co_name,
            self.IP, 
            relay_number,
            err)
        self.logger.error(msg)

        return None, msg

    def reset_relay(self, relay_number):
        """Resets relay:
            (closes relay if NO and opens relay if NC) 
            (if not blocked).
            Default is Normaly Open (if could not read database).
        """
        try:
            relay_number = int(relay_number)

            # If relay is blocked, do nothing.
            if self.blocked_by_route[relay_number]:
                return False

            # If relay is not blocked:
            else:

                # If relay's default state is NC, closes:
                if self.relay_type[relay_number] == 'NC':
                    self.set_module_relay(relay_number)
                    self.relay_status[relay_number] = 'Reset'   # Storing relay status:
                    return True, 'NC'

                # Otherwise, relay is assumed to be NO and opens:
                else:
                    self.reset_module_relay(relay_number)
                    self.relay_status[relay_number] = 'Reset'   # Storing relay status:
                    return True, 'NO'

        except Exception as err:
            msg = 'Error in method {}.{}. From: IP: {}, relay: {}. Error message: {}'.format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                self.IP, 
                relay_number,
                err)
            self.logger.error(msg)

            return None, msg

    def change_relay_status(self, relay_number):
        """Changes the status of fixed relay.
        If it is set, resets it. If it is reset, sets.
        """

        try:
            relay_number = int(relay_number)

            if self.relay_status[relay_number] == 'Reset':
                self.set_relay(relay_number)
                return True, 'Set'
            else:
                self.reset_relay(relay_number)
                return True, 'Reset'

        except Exception as err:
            msg = 'Error in method {}.{}. From: IP: {}, relay: {}. Error message: {}'.format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                self.IP, 
                relay_number,
                err)
            self.logger.error(msg)

            return None, msg
        
    def set_relay_temporarily(self, relay_number = 0, sleep_time = None):
        """Sets relay 
        for duration 'sleep_time' 
        and then resets it.
        """

        # Exception handling in case sleep_time was not informed as number:
        try:
            
            msg = None

            # Workaround to set default sleep time because self.* or class.* can't be passed as default arguments in methods. Ref: https://stackoverflow.com/questions/7371244/using-self-as-default-value-for-a-method
            if sleep_time in (None, False):
                sleep_time = self.sleep_time_default
                msg = 'sleep_time in (None or False)' 

            sleep_time = float(sleep_time) 

        except Exception as err:
            try:
                msg = 'Error in method {}.{}. From IP: {}, IO #: {}, sleep_time: {}. Error message: {}'.format(
                    self.__class__.__name__,
                    sys._getframe().f_code.co_name,
                    self.IP,
                    relay_number,
                    sleep_time,
                    err)
                self.logger.error(msg)

            except Exception as err:
                msg = 'Exception occurred while treating another exception: {}'.format(err)
                print(msg)

            # If error occurred, use sleep_time_default.
            finally:
                sleep_time = self.sleep_time_default
    
        # If error occurred or not, sets relay temporarily.
        finally:

            # Setting relay:
            self.set_relay(relay_number)
    
            # Waiting for sleepTime seconds.
            sleep(sleep_time)
    
            # Reseting relay to default state.
            self.reset_relay(relay_number)

        return True, msg
       
    def set_relay_accordingly_to_inputs(self, relay_number):
        """Sets relays of this module according to relayTiming especifications (Mirror, Fixed or Temporary)."""

        try:
            relay_number = int(relay_number)

            # If relay is blocked (by an escape route):
            if self.blocked_by_route[relay_number]:
                msg = 'On method {}.{}, relay is blocked. From: IP: {}, relay: {}.'.format(
                    self.__class__.__name__,
                    sys._getframe().f_code.co_name,
                    self.IP,
                    relay_number)
                self.logger.info(msg)

                return False, self.blocked_by_route[relay_number]

            # If relay is not blocked:
            else:
                subject = ''    # Auxiliar string for logging message.

                # If relay is of type Mirror, sets relay:
                if isinstance(self.relay_timing[relay_number], str) \
                    and self.relay_timing[relay_number].upper() == 'MIRROR':
                    self.set_relay(relay_number)
                    subject = 'relay was set'
                    
                # If relay is of type Fixed, changes relay status:
                elif isinstance(self.relay_timing[relay_number], str) \
                    and self.relay_timing[relay_number].upper() == 'FIXED':
                    self.change_relay_status(relay_number)
                    subject = 'relay changed status'

                # Else (presumably relay is of type Temporary), sets relay temporarily:
                else:
                    threading.Thread(target = self.set_relay_temporarily,
                         name = 'set_relay_temporarily',
                         args = (relay_number, self.relay_timing[relay_number])
                         ).start()

                    subject = 'relay was set temporarily'

                # Sending email:
                if config_email.send_email_on_output_change and subject:
                    msg = ('On module {}\n' + 
                            'output number {}\n' + 
                            subject + '.'
                            ).format(self.IP, relay_number)
                    self.email_controller.send_gmail_Thread(subject, msg)

                return True, subject

        except Exception as err:
            msg = 'Error in method {}.{}. From: IP: {}, relay: {}. Error message: {}'.format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                self.IP, 
                relay_number, 
                err)
            self.logger.error(msg)
            return None, msg

        return

    def reset_relay_accordingly_to_inputs(self, relay_number):
        """Resets relays of this module according to relayTiming especifications (Mirror, Fixed or Temporary)."""

        try:
            relay_number = int(relay_number)

            # If relay is blocked (by an escape route):
            if self.blocked_by_route[relay_number]:
                msg = 'On method {}.{}, relay is blocked. Module: {}, relay: {}.'.format(
                    self.__class__.__name__,
                    sys._getframe().f_code.co_name,
                    self.IP,
                    relay_number)
                self.logger.info(msg)
                return False, self.blocked_by_route[relay_number]

            # If relay is not blocked:
            else:
                subject = ''    # Auxiliar string for logging message.

                # If relay is of type Mirror, resets relay:
                if isinstance(self.relay_timing[relay_number], str) \
                    and self.relay_timing[relay_number].upper() == 'MIRROR':
                    self.reset_relay(relay_number)
                    subject = 'relay was reset'
                    
                # If relay is of type Fixed, changes do nothing:
                elif isinstance(self.relay_timing[relay_number], str) \
                    and self.relay_timing[relay_number].upper() == 'FIXED':
                    subject = 'Relay is fixed. Did nothing.'

                # Else (presumably relay is of type Temporary), nothing needs to be done:
                else:
                    subject = 'Relay is temporary. Did nothing.'

                # Sending email:
                if config_email.send_email_on_output_change and subject:
                    msg = ('On module {}\n' + 
                            'output number {}\n' + 
                            subject + '.'
                            ).format(self.IP, relay_number)
                    self.email_controller.send_gmail_Thread(subject, msg)

                return True, subject

        except Exception as err:
            msg = 'Error in method {}.{}. From: IP: {}, relay: {}. Error message: {}'.format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                self.IP, 
                relay_number, 
                err)
            self.logger.error(msg)
            return None, msg

        return

    def set_relay_accordingly_to_inputs_thread(self, relay_number):
        """ It is necessary to call as thread in case command must be sent to multiple modules at the same time. """

        threading.Thread(target = self.set_relay_accordingly_to_inputs,
                         name = 'set_relay_accordingly_to_inputs' + self.IP,
                         args = (relay_number, )
                         ).start()
        return

    def reset_relay_accordingly_to_inputs_thread(self, relay_number):
        """ It is necessary to call as thread in case command must be sent to multiple modules at the same time. """

        threading.Thread(target = self.reset_relay_accordingly_to_inputs,
                         name = 'reset_relay_accordingly_to_inputs' + self.IP,
                         args = (relay_number, )
                         ).start()
        return

    def set_relays_local_and_remote(self, nu_input = None):
        """ Sets relays as determined by parameters in database, including relays of this module and of other modules,
        according to input's number (relay_number) and it's specification.
        """
        try:

            # Prealocating variables so 'msg' doesn't crash if error occour in previous part of code.
            remoteIP = 'None'
            relay_number = 'None'

            nu_input = int(nu_input)

            # If input_addresses is was not set.
            if self.input_addresses[nu_input] is None:
                return False, f'set: input_addresses[{nu_input}] is None'

            # If input_addresses is '0', do nothing.
            elif self.input_addresses[nu_input] == '0':
                return False, f'set: input_addresses[{nu_input}] is 0'

            # Cases in which resets, on same module, same relay number: None, '', '1', 'self':
            elif ( self.input_addresses[nu_input] is None
                   or ( isinstance(self.input_addresses[nu_input], str)
                        and (self.input_addresses[nu_input].lower() in ('', '1', 'self'))
                       )
                   ):
                self.set_relay_accordingly_to_inputs_thread(nu_input)
                return True, f'set: input_addresses[{nu_input}] is self'

            # If input is 'All', sets, on all modules, same relay number.
            elif isinstance(self.input_addresses[nu_input], str) \
                and self.input_addresses[nu_input].lower() == 'all':
                for module in self.module_list.list:
                    module.set_relay_accordingly_to_inputs_thread(nu_input)
                return True, f'set: input_addresses[{nu_input}] is all'

            # If input_addresses has one or more addresses, sets other specific module and relay number. May be more than one.
            else:
                addresses = [x.strip() for x in self.input_addresses[nu_input].split(',')]          # Separating addresses by commas.
                for address in addresses:                                                           # For each address (IP, relay).
                    if address != 'None':                                                           # If there are addresses.
                        remoteIP, relay_number =  [x.strip() for x in address.split(':')]           # Splitting address string on [IP] and [relay number] (by :).
                        relay_number = int(relay_number)                                            # Transforming string in integer to use set/reset methods.
                        modules_list, _ = self.module_list.get_modules(IP = remoteIP)               # Getting module from module_list.
                        if  modules_list:                                                           # If there is a module list with modules, 
                            modules_list[0].set_relay_accordingly_to_inputs_thread(relay_number)    # Set relay in 1st module.
                return True, 'set: remotely'

        except Exception as err:
            msg = 'Error in method {}.{}. From: IP: {} input: {}, To: IP: {} relay: {}. Error message: {}'.format(
                self.__class__.__name__,            # Ref. for getting class name on 2019-06-26:  https://stackoverflow.com/questions/510972/getting-the-class-name-of-an-instance
                sys._getframe().f_code.co_name,     # Ref. for getting method name on 2019-06-26: https://stackoverflow.com/questions/251464/how-to-get-a-function-name-as-a-string-in-python
                self.IP, 
                nu_input, 
                remoteIP, 
                relay_number, 
                err)
            self.logger.error(msg)
            return None, msg

        return

    def reset_relays_local_and_remote(self, nu_input = None):
        """Resets relays as determined by parameters in database, including relays of this module and of other modules,
        according to input's number (relay_number) and it's specification.
        """
        try:

            # Prealocating variables so 'msg' doesn't crash if error occour in previous part of code.
            remoteIP = 'None'
            relay_number = 'None'

            nu_input = int(nu_input)

            # If input_addresses is was not set.
            if self.input_addresses[nu_input] is None:
                return False, f'reset: input_addresses[{nu_input}] is None'

            # If input_addresses is '0', do nothing.
            elif self.input_addresses[nu_input] == '0':
                return False, f'reset: input_addresses[{nu_input}] is 0'

            # Cases in which resets, on same module, same relay number: None, '', '1', 'self':
            elif ( self.input_addresses[nu_input] is None
                   or ( isinstance(self.input_addresses[nu_input], str)
                        and (self.input_addresses[nu_input].lower() in ('', '1', 'self'))
                       )
                   ):

                self.reset_relay_accordingly_to_inputs_thread(nu_input)
                return True, f'reset: input_addresses[{nu_input}] is self'

            # If input is 'All', resets, on all modules, same relay number.
            elif isinstance(self.input_addresses[nu_input], str) \
                and self.input_addresses[nu_input].lower() == 'all':
                for module in self.module_list.list:
                    module.reset_relay_accordingly_to_inputs_thread(nu_input)
                return True, f'reset: input_addresses[{nu_input}] is all'

            # If input_addresses has one or more addresses, sets other specific module and relay number. May be more than one.
            else:
                addresses = [x.strip() for x in self.input_addresses[nu_input].split(',')]          # Separating addresses by commas.
                for address in addresses:                                                           # For each address (IP, relay).
                    if address != 'None':                                                           # If there are addresses.
                        remoteIP, relay_number =  [x.strip() for x in address.split(':')]           # Splitting address string on [IP] and [relay number] (by :).
                        relay_number = int(relay_number)                                            # Transforming string in integer to use set/reset methods.
                        modules_list, _ = self.module_list.get_modules(IP = remoteIP)               # Getting module from module_list.
                        if  modules_list:                                                           # If there is a module list with modules, 
                            modules_list[0].reset_relay_accordingly_to_inputs_thread(relay_number)  # Set relay in 1st module.
                return True, 'reset: remotely'

        except Exception as err:
            msg = 'Error in method {}.{}. From: IP: {} input: {}, To: IP: {} relay: {}. Error message: {}'.format(
                self.__class__.__name__,            # Ref. for getting class name on 2019-06-26:  https://stackoverflow.com/questions/510972/getting-the-class-name-of-an-instance
                sys._getframe().f_code.co_name,     # Ref. for getting method name on 2019-06-26: https://stackoverflow.com/questions/251464/how-to-get-a-function-name-as-a-string-in-python
                self.IP, 
                nu_input, 
                remoteIP, 
                relay_number, 
                err)
            self.logger.error(msg)
            return None, msg

        return

