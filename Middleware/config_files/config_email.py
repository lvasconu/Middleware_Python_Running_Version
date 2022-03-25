# Setting personallized scripts to be used for this client:
#   Set clientNumber to 0 (Client[0] = '') to not use any personalized scripts.
client_number  = 0
client  = ['',                  # Client 0
            'CNI-BSB',          # Client 1
            'Fazenda Veredas',  # Client 2
            ]

# Setting e-mails parameters:
send_email                  = False                 # Set True to send e-mails in general. False to not send.
send_email_on_escape_route  = True                  # Set True to send e-mails on Escape Route activation and deactivation.
send_email_on_input_change  = True                  # Set True to send e-mails on input change.
send_email_on_output_change = False                 # Set True to send e-mails on output change.

sender = 'DevOps.GlobalAdvising@gmail.com'          # E-mail from witch e-mails will be sent. Password will be entered when the program is first run.
recipients = [
                'joao.paulo@gaadvising.com',
                'marcelo.marinho@gaadvising.com', 
                'fabio.torres@gaadvising.com',
                ]
