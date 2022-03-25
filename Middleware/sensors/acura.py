# Import section:
import sys

from controllers import log_controller

class AM10():

    # Class variables:
    logger = log_controller.LogController()        # Log controller.
    ping_interval = 0.5

    # Default messages:
    msg_beggining       = '\x02'
    msg_end             = '\r\x03'
    msg_ping            = ':000000\r'               # \r = Carriage return (CR); :000000: Polling. Ref: Acura Guia de Programação.
    msg_ping_response   = ':000000\r:000600\r\n'
    msg_to_ignore       = '\x1b'                    # Message to be ignored when received. Byte Acura sends when card is removed.

    def get_identifier_from_string(self, msg_string):
        """ Gets identifier (card) number from received socket data. 
        Received message 'msg_string' must be string.
        Returns None if no valid data was received.
        """
        try:
            
            # Removing message beggining (In RS232,  02 means the start of the text (STX)):
            msg_beggining = '\x02'
            if msg_string.startswith(msg_beggining) :                   # If message starts with msg_beggining. Ref: https://careerkarma.com/blog/python-startswith-and-endswith/#:~:text=The%20startswith()%20string%20method,otherwise%2C%20the%20function%20returns%20False.
                msg_string = msg_string.replace(msg_beggining, '', 1)   # Removes first occurance of msg_beggining. Ref: https://stackoverflow.com/questions/10648490/removing-first-appearance-of-word-from-a-string

            # Removing byte Acura sends when card is removed:
            msg_end = '\x1b'
            if msg_string.endswith(msg_end) :                           # If message starts with msg_beggining.
                msg_string = msg_string[:-len(msg_end)]                 # Removes last characters.

            # Removing message end (In RS232,  03 means End of text (ETX)):
            msg_end = '\r\x03'
            if msg_string.endswith(msg_end) :                           # If message starts with msg_beggining.
                msg_string = msg_string[:-len(msg_end)]                 # Removes last characters.

            # Returns message if it is not empty
            if msg_string != '':   
                return msg_string

        except Exception as err:
            try:
                msg_string = 'Error in method {}.{}. Error message: {}'.format(
                    self.__class__.__name__,            # Ref. for getting class name on 2019-06-26:  https://stackoverflow.com/questions/510972/getting-the-class-name-of-an-instance
                    sys._getframe().f_code.co_name,     # Ref. for getting method name on 2019-06-26: https://stackoverflow.com/questions/251464/how-to-get-a-function-name-as-a-string-in-python
                    err)
                
                self.logger.error(msg_string)

            except Exception as err:
                msg_string = 'Exception occurred while treating another exception: {}'.format(err)
                print(msg_string)

        return None

    def get_identifier_from_byte_array(self, msg_bytes):
        """ Gets identifier (card) number from received socket data. 
        Received message 'msg_bytes' must be byte array.
        Returns None if no valid data was received.
        """
        try:
            array = ''

            for b in msg_bytes: # For every byte in data.
                # Converting to hex (hexadecimal) format.
                h = "{:02X}".format(b)
   
                # If byte signalizes the end of the string, such as:
                #   03: End of text (ETX) in RS232 protocol,
                #   0A: LF in RS232 protocol, or
                #   0D: Carriage Return (CR) in RS232 protocol, or
                #   1B: Byte sent by Acura when card is removed.
                if h in ('1B', '03'):
                    card_number = bytes.fromhex(array).decode()
                    array = ''
                    if card_number:
                        return card_number
                    else:
                        return None                 # If received only '1B' or '03',  cardNumber is empty.
                # If  byte signalizes the start of the string:
                # (In RS232,  02 means the start of the text (STX).)
                elif h == '02':
                    array = ''
                # In the other cases, if byte is different from CR  (0D) and end of text (03), builds 'array'.
                #elif (b != '03' and b != '0A' and b != '0D' and b != '1B'):
                elif h not in ('0D', '03'):
                        array += h

        except Exception as err:
            try:
                msg = 'Error in method {}.{}. Error message: {}'.format(
                    self.__class__.__name__,            # Ref. for getting class name on 2019-06-26:  https://stackoverflow.com/questions/510972/getting-the-class-name-of-an-instance
                    sys._getframe().f_code.co_name,     # Ref. for getting method name on 2019-06-26: https://stackoverflow.com/questions/251464/how-to-get-a-function-name-as-a-string-in-python
                    err)
                
                self.logger.error(msg)

            except Exception as err:
                msg = 'Exception occurred while treating another exception: {}'.format(err)
                print(msg)

        return None