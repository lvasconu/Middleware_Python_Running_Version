# Importing libraries:
import RPi.GPIO as GPIO # Can't load Rpi.GPIO on Windows, only in RPi. Ref on 2019-02-01: https://raspberrypi.stackexchange.com/questions/34119/gpio-library-on-windows-while-developing
import time
import socket
import AuxFunctions
import os
import _thread
import config_RPi_1pn # Configuration file for this specific script and RPi.

# Setting the role off this Raspberry (1 for sender, 2 for receiver):
role = config_RPi_1pn.role

print('Rodando: ' + os.path.basename(__file__))

# Setting network parameters:
# Ref. on 2018-08-21: youtube.com/watch?v=u6kuHMY5pHM
# IPs for each RPi:
IP = config_RPi_1pn.IP
# Getting this RPi's IP and index:
IP_self = AuxFunctions.get_ip_address()
Port = config_RPi_1pn.Port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



# Setting pin parameters:
# Seting pin mode (BOARD or BCM):
GPIO.setmode(GPIO.BCM)
# Setting pins to be used:
read_pin = 10  # BCM 10 = Board pin 19.
write_pin = 23 # BCM 23 = Board pin 16.
# Setting pin directions:
GPIO.setup(read_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # pull_up_down=GPIO.PUD_DOWN grounds read_pin tom avoid floating voltages.
GPIO.setup(write_pin, GPIO.OUT)

# Setting relay methods:
# Method to switch relay on:
def Relay_SwitchOn(): 
    GPIO.setup(write_pin,0) # Relay is on when write_pin is 0.
# Method to switch relay off:
def Relay_SwitchOff():
    GPIO.setup(write_pin,1) # Relay is off when write_pin is 1.
# Setting default value relay to off:
Relay_SwitchOff()



# Setting parameters to send e-mails:
if role==1 and config_RPi_1pn.Send_Email==1:
    email_address = config_RPi_1pn.email_address
    email_password = AuxFunctions.get_password()
    email_recipients = config_RPi_1pn.email_recipients
    email_preamble = config_RPi_1pn.email_preamble



# Main code: loop
    # 1st Raspberry: Reads input every 0.5 seconds.
    # 1st Raspberry: Sends communication with 2nd Raspberry (if input is on)
    # 2nd Raspberry: Receives 1st Raspberry communication and closes relay if told so.
    
# If this Raspberry is the sender:
status_last = 0
while role == 1:
    status_actual = GPIO.input(read_pin)
    
    if status_actual == 1:
        msg_sent = 'Alarme ativado.'
        Relay_SwitchOn()
    else:
        msg_sent = 'Alarme desativado.'
        Relay_SwitchOff()        
    
    msg_sent_encoded = msg_sent.encode('utf-8')
    for ii in range(len(IP)): # For every addressess in IP list.
        if IP[ii] != IP_self: # Except itselt.
            sock.sendto(msg_sent_encoded,(IP[ii], Port)) # Ref. on 2018-08-21: youtube.com/watch?v=u6kuHMY5pHM
            print('Mensagem enviada p/ ' + IP[ii] + ':' + str(Port) + ': ' + msg_sent)
    time.sleep(.5)
    
    # Sending e-mails:
    if config_RPi_1pn.Send_Email:
        if status_actual == 1:
            if status_last == 0:
                email_subject = email_preamble + ' - Ativado'
                email_message = email_subject + ' por ' + IP_self
                status_last = 1
                _thread.start_new_thread (AuxFunctions.SendGmail2, (email_subject,email_message,email_address,email_password,email_recipients)  )
        else:
            if status_last == 1:
                email_subject = email_preamble + ' - Desativado'
                email_message = email_subject + ' por ' + IP_self
                status_last = 0
                _thread.start_new_thread (AuxFunctions.SendGmail2, (email_subject,email_message,email_address,email_password,email_recipients)  )
        
    
    
# If this Raspberry is a receiver:
if role == 2:
    print('Aguardando mensagem.')
    sock.bind((IP_self, Port))  # Ref. on 2018-08-21: youtube.com/watch?v=u6kuHMY5pHM
    
while role == 2:
    msg_received_encoded, addr = sock.recvfrom(1024) # Buffer size of 1024 bytes;
    msg_received = msg_received_encoded.decode('utf-8')
    print('Mensagem recebida:', msg_received)
    
    if msg_received == 'Alarme ativado.':
        Relay_SwitchOn()
    else:      
        Relay_SwitchOff()
        
    time.sleep(.5)