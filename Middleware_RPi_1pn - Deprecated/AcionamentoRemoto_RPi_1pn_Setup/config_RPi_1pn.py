# Setting the role off this Raspberry (1 for sender, 2 for receiver):
role = 2

# Setting network parameters:
# IPs for each RPi:
IP = ['10.19.1.250',
      '10.19.217.250'
     ]
# Port to be used
Port = 5000

# Setting parameters to send e-mails:
Send_Email = 1                                      # 1 to send e-mails. 0 to not send.
email_address = 'circuito.televisao@cni.org.br'     # E-mail from witch e-mails will be sent. Password will be entered when the program is first run.
email_recipients = ['joao.paulo@gaadvising.com','marcelo.marinho@gaadvising.com', 'fabio.torres@gaadvising.com']
email_preamble = 'CNI EAMN Elevadores - Botão de pânico'