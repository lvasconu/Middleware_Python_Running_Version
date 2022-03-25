import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import sys
import inspect
from cryptography.fernet import Fernet  # Necessary: on cmd: pip install cryptography
import getpass                          # Ref. on 2018-10-16: https://stackoverflow.com/questions/43673886/python-2-7-how-to-get-input-but-dont-show-keys-entered/43673912
import socket
import struct
    
from config_files import config_email
from controllers import log_controller

class EmailController:
    
    # Class variables:
    logger = log_controller.LogController()            # Log controller.

    def __init__(self):
        try:
            self.sender          = config_email.sender               
            self.recipients      = config_email.recipients

            # Verifying/getting password for sender email.
            _, self.psw  = self.get_password(self.sender)

        except Exception as err:
            msg = 'Error in method email_controller.__init__(). Error message: {}'.format(err)
            self.logger.error(msg)

        return

    def send_gmail(self, subject, message):
        ''' Sends email using gmail account.
        Refs:
        http://naelshiab.com/tutorial-send-email-python/
        https://stackoverflow.com/questions/8856117/how-to-send-email-to-multiple-recipients-using-python-smtplib
        '''

        try:
            if config_email.send_email == True:

                msg = MIMEMultipart()
                msg['From']     = self.sender
                msg['To']       = ', '.join(self.recipients)    # The msg['To'] needs to be a string.

                # Subject:
                if config_email.client[config_email.client_number] != '':
                    sbj = config_email.client[config_email.client_number] + ' - ' + subject
                else:
                    sbj = subject
                msg['Subject'] = sbj
             
                body = message
                msg.attach(MIMEText(body, 'plain'))
             
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(self.sender, self.psw)
                text = msg.as_string()
                server.sendmail(self.sender, self.recipients, text) # While the recipients in sendmail(sender, recipients, message) needs to be a list.
                server.quit()

                return True

        except Exception as err:
            msg = 'Error in method email_controller.SendGmail(). Error message: {}'.format(err)
            self.logger.error(msg)

            return False
        
        return None

    def send_gmail_Thread(self, subject, message):
        threading.Thread(target = self.send_gmail,
                        name = 'send_gmail', 
                        args = (subject, message)
                    ).start()
        return

    def get_password(self, sender):
    # Getting password to send email.

        try:

        # Ref. on 2018-10-16:
            # https://www.mssqltips.com/sqlservertip/5173/encrypting-passwords-for-use-with-python-and-sql-server/
            # https://stackoverflow.com/questions/7585435/best-way-to-convert-string-to-bytes-in-python-3

            # Getting current file path:
            filepath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            filename = 'a.bin'
    
            # Unique key. To generate key: key = Fernet.generate_key()
            key = b'iVdwGOHlc08hGiBqzC3wYpOuPqnbU9_nO2Br84pCTF4='
            cipher_suite = Fernet(key)
    
            # If file with password doesn't exist yet:
            if not os.path.isfile(filepath + '/' + filename): # Ref. on 2018-10-16: https://stackabuse.com/python-check-if-a-file-or-directory-exists/
                #psw = input ('Entre com a senha do e-mail a ser usado como remetente: ')
                psw = getpass.getpass('Enter password for the email account ' + sender + ': ')  # Ref. on 2018-10-16: https://stackoverflow.com/questions/43673886/python-2-7-how-to-get-input-but-dont-show-keys-entered/43673912
                psw_bites = psw.encode('utf-8') #required to be bytes
                ciphered_text1 = cipher_suite.encrypt(psw_bites)       # First encryptation.
                ciphered_text2 = cipher_suite.encrypt(ciphered_text1)  # Second encryptation.

                # Writing encrypted password in bin file:
                with open(filepath + '/' + filename, 'wb') as file_object:
                    file_object.write(ciphered_text2)
    
            # Reading encrypted password from bin file:
            with open(filepath + '/' + filename, 'rb') as file_object:
                for line in file_object:
                    encryptedpwd = line
                    uncipher_text1 = cipher_suite.decrypt(encryptedpwd)   # First decryptation.
                    uncipher_text2 = cipher_suite.decrypt(uncipher_text1) # Second decryptation.
                    psw = uncipher_text2.decode("utf-8") #convert to string
                    #print(plain_text_encryptedpassword)
            
                    #print(encryptedpwd)
                    #print(uncipher_text1)
                    #print(uncipher_text2)
                    #print(psw)
            
                return True, psw 

        except Exception as err:
            msg = ('Error in {}.{}. '+\
                    'Error message: {}').format(
                    self.__class__.__name__,
                    sys._getframe().f_code.co_name,
                    err)
            self.logger.error(msg)

            return False
        
        return None

    def get_ip_address(self):
        # Gets IP of this machine.

        # Source on 2018-08-24:
        # https://circuitdigest.com/microcontroller-projects/display-ip-address-of-raspberry-pi

        ip_address = '';
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip_address = s.getsockname()[0]
        s.close()

        return ip_address

if __name__ == '__main__':
    e = EmailController()
    e.send_gmail('Assunto teste','Testando send_gmail()')
