from config_files import config_email
from controllers.email_controller import EmailController

e = EmailController()

def test_get_password():
    sender = config_email.sender

    received_data, _ = e.get_password(sender)

    assert received_data == True

def test_send_gmail():
    
    received_data = e.send_gmail('Assunto teste','Testando send_gmail()')

    assert received_data

if __name__ == "__main__":

    a = e.send_gmail('Assunto teste','Testando send_gmail()')
    print('Tested seng_gmail()')