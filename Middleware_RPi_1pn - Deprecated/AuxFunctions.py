def get_ip_address():
    # Source on 2018-08-24:
    # https://circuitdigest.com/microcontroller-projects/display-ip-address-of-raspberry-pi
    
    import socket
    
    ip_address = '';
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8',80))
    ip_address = s.getsockname()[0]
    s.close()
    #print(ip_address)
    return ip_address

def get_ip_address2(ifname):
    # Source on 2018-08-28:
    # https://raspberrypi.stackexchange.com/questions/6714/how-to-get-the-raspberry-pis-ip-address-for-ssh
    # http://code.activestate.com/recipes/439094-get-the-ip-address-associated-with-a-network-inter/
    import fcntl
    import struct
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15].encode('utf-8'))
        )[20:24])

def getHwAddr(ifname):
    # Source on 2018-08-28:
    # http://code.activestate.com/recipes/439094-get-the-ip-address-associated-with-a-network-inter/
    # Not working on 2018-08-28.
    import fcntl
    import struct
    import socket
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15].encode('utf-8')))
    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]

def SendGmail(message):
    # Ref on 2018-08-28:
    # http://naelshiab.com/tutorial-send-email-python/
    try:
        # import smtplib # moved to main script to avoid several imports. 2018-10-10 JPO.
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('sender_email@gmail.com', 'password')
             
        #msg = 'YOUR MESSAGE!'
        server.sendmail('receiver_email@gmail.com', message)
        server.quit()
    except:
        print('Um erro ocorreu ao tentar enviar e-mail com SendGmail().')
        
    return

def SendGmail2(subject,message,fromaddr,password,recipients):
    # Ref on 2018-08-28: http://naelshiab.com/tutorial-send-email-python/
    # Ref on 2018-08-29: https://stackoverflow.com/questions/8856117/how-to-send-email-to-multiple-recipients-using-python-smtplib
    try:
        
        #from email.MIMEMultipart import MIMEMultipart
        #from email.MIMEText import MIMEText
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = subject
             
        body = message
        msg.attach(MIMEText(body, 'plain'))
             
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, password)
        text = msg.as_string()
        server.sendmail(fromaddr, recipients, text)
        server.quit()
    except:
        print('Um erro ocorreu ao tentar enviar e-mail com SendGmail2().')
        
    return

def get_password():
# Ref. on 2018-10-16:
    # https://www.mssqltips.com/sqlservertip/5173/encrypting-passwords-for-use-with-python-and-sql-server/
    # https://stackoverflow.com/questions/7585435/best-way-to-convert-string-to-bytes-in-python-3
    import os
    import inspect
    from cryptography.fernet import Fernet
    import getpass # Ref. on 2018-10-16: https://stackoverflow.com/questions/43673886/python-2-7-how-to-get-input-but-dont-show-keys-entered/43673912
    
    # Getting current file path:
    filepath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    filename = 'a.bin'
    
    # Unique key. To generate key: key = Fernet.generate_key()
    key = b'iVdwGOHlc08hGiBqzC3wYpOuPqnbU9_nO2Br84pCTF4='
    cipher_suite = Fernet(key)
    
    # Checking if file with password already exists:
    if not os.path.isfile(filepath + '/' + filename): # Ref. on 2018-10-16: https://stackabuse.com/python-check-if-a-file-or-directory-exists/
        #psw = input ('Entre com a senha do e-mail a ser usado como remetente: ')
        psw = getpass.getpass('Entre com a senha do e-mail a ser usado como remetente: ')  # Ref. on 2018-10-16: https://stackoverflow.com/questions/43673886/python-2-7-how-to-get-input-but-dont-show-keys-entered/43673912
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
            
    return psw



if __name__ == '__main__':
    print(get_ip_address())
    print(get_ip_address2('eth0'))
    #print(get_ip_address2('lo'))
    #print(getHwAddr('eth0'))
    
    SendEmail('Testando SendEmail()')
    SendEmail2('Assunto teste','Testando SendEmail2()')