import socket
import select
import sys
import struct
from time import sleep
import threading

from controllers import log_controller

# Global attributes:
buffer_size = 256       # Buffer size for TCP communication, in bytes. Wolpac standard message: 68 bytes. Comm5 welcome message: 59 bybtes
socketTimeOut = 5       # Timeout of socket [s]

class SocketController:

    # Class variables:
    logger = log_controller.LogController()                    # Log controller.

    def __init__(self, simple_socket, original_port, test = False):
        
        self.controlled_socket = simple_socket              # Making object variable to be able to manipulate socket in other methods.
        self.original_port = original_port                  # Storing module's original port for error messages.
        self.test = test                                    # Variable to be set to True during testing.
        
        self.send_list = []                                 # List to store strings to be sent to this socket.

        self.controlled_socket.settimeout(socketTimeOut)    # Establishing socket timeout.
        self.IP, _ = simple_socket.getpeername()            # Storing module's IP for error messages. Ref: https://stackoverflow.com/questions/41250805/how-do-i-print-the-local-and-remote-address-and-port-of-a-connected-socket
        self.online = 'unknown'                             # Monitoring connection:  online, unknown (probably online), offline.
        
        self.ping_count = 1                                 # Reseting ping count.
        self.ping_interval = 1                              # Interval between sending each ping message [s]

        self.msg_beggining = None 
        self.msg_end = None    
        self.msg_ping = None                                # Message to be send to module and/or reader as ping.
        self.msg_ping_response = None                       # Message expected from module and/or reader as ping response.

        # Refs on select.select:
        # https://pythonprogramming.net/server-chatroom-sockets-tutorial-python-3/
        # https://pythonprogramming.net/client-chatroom-sockets-tutorial-python-3/
        # https://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method
        # https://docs.python.org/3/howto/sockets.html

        return
    
    def communicate(self):
        """ Returns message, if received (other than ok messages, triggered by ping messages).
            Sends messages, if there are any in self.send_list.
            Returns False and updates self.online accordingly.
        """

        try:
            while self.online in ('online', 'unknown'):                         # While socket is online or unkown:
                # Waiting for any sockets to be ready to be receive messages, send messages or in exception for a maximum period of 'ping_time' seconds.
                ready_receive_sockets, ready_send_sockets, sockets_in_exception = select.select([self.controlled_socket], [self.controlled_socket], [self.controlled_socket], self.ping_interval)

                # If socket is ready to receive message:
                if ready_receive_sockets:
                    received_message = self.controlled_socket.recv(buffer_size)   # Receiving 1st message chunk.

                    # Seing if entire message was received or if there is more:
                    ready_receive_sockets, _, _ = select.select([self.controlled_socket], [], [], .1)      # Seeing if there is still data in buffer to be received until limit of 0.1 seconds.
                    while ready_receive_sockets and len(received_message):                                 # If there is still data in buffer and data is not empty.
                        received_message = received_message + self.controlled_socket.recv(buffer_size)     # Concatenating next message chunk.
                        ready_receive_sockets, _, _ = select.select([self.controlled_socket], [], [], .1)  # Seeing if there is still data in buffer to be received until limit of 0.1 seconds.
                    
                    # If received no data (empty string), client gracefully closed connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR). Ref: https://pythonprogramming.net/server-chatroom-sockets-tutorial-python-3/
                    if not received_message:                                    # Equivalente to: if not len(received_message) / if len(receivedMessage) == 0
                        msg = 'Connection on {}:{} closed remotely but gracefully.'.format(self.IP, self.original_port)
                        SocketController.logger.warning(msg)
                        ready_receive_sockets[0].close()                        # Closing connection at this end.
                        self.online = 'offline'                                 # Socket is offline.
                        return False

                    # If there is data:
                    else:
                        # Decoding message.
                        received_message = received_message.decode()

                        # Treating received message:
                        received_message = self.treat_received_message(received_message)

                        if received_message:                                    # If, after message was treated, there is still data,
                            return received_message                             # Returns message.
                
                # If the socket is ready to send (Actually, any reasonably healthy socket will return as writable - it just means outbound network buffer space is available. Ref: https://docs.python.org/3/howto/sockets.html )
                elif ready_send_sockets: 
                    #  And there is something to send in send_list:
                    if self.send_list:

                        self.controlled_socket.sendall(self.send_list[0])         # Sending 1st element on send_list.
                        
                        if self.test: # Code for testing:
                            print('Sent message: ' + str(self.send_list[0], 'utf-8'))
                        
                        del self.send_list[0]                                    # Removing item from list. Ref: https://stackoverflow.com/questions/11520492/difference-between-del-remove-and-pop-on-lists/11520540
                    
                    # And there is nothing to send:
                    else:
                        sleep(.05)                                              # Waits some time.

                # If exception occurred in socket:
                elif sockets_in_exception:
                    msg = 'Socket {}:{} in exception.'.format(
                           self.IP,
                           self.original_port)
                    SocketController.logger.error(msg)
                    self.controlled_socket.close()                              # Closes socket connection.
                    self.online = 'offline'                                     # Socket is offline.
                    return False                                                # Returning False.

                # If all lists are empty, timeout occourred (of 'self.ping_time' seconds):
                elif len(readyreceivesockets) == 0 and len(readysendsockets) == 0 and len(socketsinexception) == 0 :
                    msg = 'Socket {}:{} : ping # {} failed.'.format(
                           self.IP,
                           self.original_port,
                           self.ping_count)
                    SocketController.logger.warning(msg)

                    if self.ping_count >= 3:
                        msg = 'Socket {}:{} changed to offline after 3 ping fails.'.format(
                               self.IP,
                               self.original_port)
                        SocketController.logger.error(msg)
                        self.controlled_socket.close()                          # Closes socket connection.
                        self.online = 'offline'                                 # Socket is offline.
                        return False                                            # Returning False.

                    self.ping_count += 1
            
        except Exception as err:
            try:
                self.controlled_socket.close()
            except Exception as e2:
                msg = 'Error in {}.{}. Error message: {}'.format(
                    self.__class__.__name__,
                    sys._getframe().f_code.co_name,
                    e2)
                SocketController.logger.error(msg)

            msg = 'Error in {}.{}. Error message: {}'.format(
                self.__class__.__name__,                                # Ref. for getting class name on 2019-06-26:  https://stackoverflow.com/questions/510972/getting-the-class-name-of-an-instance
                sys._getframe().f_code.co_name,                         # Ref. for getting method name on 2019-06-26: https://stackoverflow.com/questions/251464/how-to-get-a-function-name-as-a-string-in-python
                err)
            SocketController.logger.error(msg)
            self.online = 'offline'                                     # Socket is offline.
            return False                                                # Returning False.
    
    def queue_to_send(self, msg_to_send):
        """ Puts 'msg_to_send' in queue to be sent via socket, in bytes format.
            Input must be string or bytes.
        """

        # Including begginging and end strings.
        msg_to_send = self.include_message_beggining_and_end(msg_to_send)
        #print('Mensagem em fila: ' + msg_to_send)

        # Encoding strings to bytes in utf-8 (default). Ref: https://www.programiz.com/python-programming/methods/string/encode
        if type(msg_to_send) is str:                
            msg_to_send = msg_to_send.encode()  

        # If message is in bytes format, appends msg to list to be sent:
        if type(msg_to_send) is bytes:
            self.send_list.append(msg_to_send)     

        return

    def ping_thread(self):
        """ Invoking queue_ping() as thread to not interrupt the rest of the code. """
        threading.Thread(target = self.ping,
                    name = 'SocketController.queue_ping_thread',
                    args = ()
                    ).start()

    def ping(self):
        """ Puts ping message in queue to be sent. """

        while self.online in ('online', 'unknown'):             # While socket is online or unknown:
            sleep(self.ping_interval)                           # Sleeps for some seconds.
            self.queue_to_send(self.msg_ping)                   # Puts ping message in queue to be sent.
            
        return

    def include_message_beggining_and_end(self, msg):
        """ Includes message start and end to message, if they exist. """

        # Including  message start, if it exists:
        if self.msg_beggining:
            msg = self.msg_beggining + msg

        # Including  message end, if it exists:
        if self.msg_end:
            msg = msg + self.msg_end

        return msg

    def treat_received_message(self, msg):
        """ Checks if ping message was concatenated, in the beggining or end of the main message.
            Removes message start and end, if they exist.
        """
        # Removing msg_to_ignore, if they occur.
        if self.msg_to_ignore:
            msg = msg.replace(self.msg_to_ignore, '')

        # Checking if ping message is concatenated:
        checked_ping = [False, False]                                                           # Ping message in the beggining, Ping message in the end.
        while False in checked_ping:
            if self.msg_ping_response:                                                          # If there is a known ping response string for this module/reader:

                # Removing ping at the beggining:
                if msg.startswith(self.msg_ping_response) :                                     # If message starts with it.
                    self.online = 'online'                                                      # Socket is online.
                    self.ping_count = 1                                                         # Reseting ping count.
                    msg = msg.replace(self.msg_ping_response, '', 1)                            # Removes first occurance of it.
                    checked_ping = [False, False]                                               # If removal was needed, loop has to be redone, resets variable.

                else:
                    checked_ping[0] = True                                                      # If removal was not needed, criteria is met.

                # Removing ping at the end:
                if msg.endswith(self.msg_ping_response) :                                       # If message ends with it.
                    self.online = 'online'                                                      # Socket is online.
                    self.ping_count = 1                                                         # Reseting ping count.
                    msg = msg[:-len(self.msg_ping_response)]                                    # Removes last characters.
                    checked_ping = [False, False]                                               # If removal was needed, loop has to be redone, resets variable.
                else:
                    checked_ping[1] = True                                                      # If removal was not needed, criteria is met.

            else:                                                                               # If there is no message, it is as if the criteria was met.
                checked_ping[0] = checked_ping[1] = True
        
        # As sometimes socket receives message concatenated with others
        # (case is specifically serious in Acura AM-10, in which identifier number is received in the middle of ping response),
        # it is necessary to search for message beggining and end, and return message inbetween.

        # Removing message beggining (and anything before):
        if self.msg_beggining :                                     # If there is a known beggining string for this module/reader:
            index = msg.find(self.msg_beggining)                    # Getting (1st) beggining message's index. Ref: https://www.geeksforgeeks.org/python-string-find/#:~:text=The%20find()%20method%20returns,found%20then%20it%20returns%20%2D1.
            if index != -1 :                                        # If found beggining:
                msg = msg[index + len(self.msg_beggining):]         # Removes beggining and previous.

        # Removing message end (and anything after):
        if self.msg_end:                                            # If there is a known end string for this module/reader:
            index = msg.find(self.msg_end)                          # Getting (1st) end message's index. Ref: https://www.geeksforgeeks.org/python-string-find/#:~:text=The%20find()%20method%20returns,found%20then%20it%20returns%20%2D1.
            if index != -1 :                                        # If found end:
                msg = msg[:index]                                   # Removes beggining and previous.

        # Simpler code, that verified only beggining and end of received messages:
        ## Removing message beggining
        #if self.msg_beggining :                                     # If there is a known beggining string for this module/reader:
        #    if msg.startswith(self.msg_beggining) :                 # If message starts with it. Ref: https://careerkarma.com/blog/python-startswith-and-endswith/#:~:text=The%20startswith()%20string%20method,otherwise%2C%20the%20function%20returns%20False.
        #        msg = msg.replace(self.msg_beggining, '', 1)        # Removes first occurance of it. Ref: https://stackoverflow.com/questions/10648490/removing-first-appearance-of-word-from-a-string

        ## Removing message end, at the end of message:
        #if self.msg_end:                                            # If there is a known end string for this module/reader:
        #    if msg.endswith(self.msg_end) :                         # If message ends with it.
        #        msg = msg[:-len(self.msg_end)]                      # Removes last characters.

        if msg != '':
            return msg
        else:
            return None
    
    def set_message_beggining_and_end(self, msg_beggining = None, msg_end = None):
        """ Setting message begginging and end, accordingly to module and/or reader.
            msg_ping and msg_ping_response must be strings, array of strings or dict of strings.
        """

        # Beginning of message:
        self.msg_beggining = msg_beggining

        # End of message:
        self.msg_end = msg_end

        return

    def set_ping_messages(self, msg_ping = None, msg_ping_response = None):
        """ Setting ping messages (to send and expected to receive), accordingly to module and/or reader.
            msg_ping and msg_ping_response must be strings, array of strings or dict of strings.
        """

        # Message to be sent:
        self.msg_ping = msg_ping

        # Expected messages:
        self.msg_ping_response = msg_ping_response

        return

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
            
        controlled_socket = SocketController(module_socket, port, test = True)

        while controlled_socket.online in ('online', 'unknown'):
            msg = controlled_socket.communicate()
            
            if msg :
                print('In main: ' + str(msg))
                controlled_socket.queue_to_send(msg)
            
                
            
            

