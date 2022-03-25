import socket
from time import sleep
import threading
import requests
import json

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.listen()

    def listen(self):
        print('Listening on {}'.format(self.port))
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(None)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    
    def travarPorta(self, nu_rele, ip_equipamento):
        """TODO: Docstring for liberarPorta.

        :returns: TODO

        """
        com_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        com_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = (ip_equipamento, 5000)
        com_sock.connect(server_address)
        com_sock.recv(1024)
        
        #identify who to send
        message = 'set {}\n'.format(nu_rele)
        #  print(message.encode())
        # send message
        com_sock.send(message.encode())
        com_sock.recv(1024)  
        pass

    def liberarPorta(self, nu_rele, ip_equipamento, t_acionamento = 3):
        """TODO: Docstring for liberarPorta.

        :nu_rele: TODO
        :ip_equipamento: TODO
        :t_acionamento: TODO
        :returns: TODO

        """

        #  print('ip_equipamento: {}'.format(ip_equipamento))
        com_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        com_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = (ip_equipamento, 5000)
        com_sock.connect(server_address)
        com_sock.recv(1024)
        
        #identify who to send
        message = 'set {}\n'.format(nu_rele)
        #  print(message.encode())
        # send message
        com_sock.send(message.encode())
        com_sock.recv(1024)
        #wait for t_acionamento
        sleep(t_acionamento)
        message = 'reset {}\n'.format(nu_rele)
        #  print(message.encode())
        com_sock.send(message.encode())
        com_sock.recv(1024)

        pass


    def registrarAcesso(self, co_solicitacao, co_tipo_acesso):
        """TODO: Docstring for registrarAcesso.

        :arg1: TODO
        :returns: TODO

        """

        url='http://10.19.1.222:5864/GAAPI/api/RegistraAcesso?co_solicitacao={0:d}&co_tipo_acesso={1:d}'.format(int(co_solicitacao), int(co_tipo_acesso))
        r = requests.get(url)
        print('Acesso Registrado')

        pass

    def solicitaAcesso(self, id_equipamento, nu_identificador, tipo_acesso, nu_rele, ip_equipamento):
        """TODO: Docstring for solicitaAcesso.

        :id_equipamento: TODO
        :card: TODO
        :tipo_acesso
        :returns: TODO

        """

        url = "http://10.19.1.222:5864/GAAPI/api/SolicitaAcesso?nu_identificador={0}&co_equipamento={1}&co_tipo_acesso={2}".format(nu_identificador, id_equipamento, tipo_acesso)
        print('Solicitando Acesso nu_rele: {0},  ip_equipamento: {1}'.format(nu_rele, ip_equipamento))
        r = requests.get(url)
        data = r.json()
        co_solicitacao = int(data[u'co_solicitacao'])
        co_tipo_acesso = int(data[u'co_tipo_acesso'])
        if co_tipo_acesso == 1 or co_tipo_acesso == 6 or co_tipo_acesso == 2:
            #Registrar Acesso
            print('Acesso Autorizado para solicitacao numero {}'.format(co_solicitacao))
            # Liberar porta
            self.liberarPorta(nu_rele, ip_equipamento)
            # log access
            self.registrarAcesso(co_solicitacao, co_tipo_acesso)

        pass

    def listenToClient(self, client, address):
        ip, port = address
        print("Client Connected, address: {0}, port: {1}".format(address, self.port))
        #identificar conexao
        url = "http://10.19.1.222:5864/GAAPI/api/IdentificaConexao?ip_equipamento={0}&porta_conexao={1}".format(ip, self.port)
        r = requests.get(url)
        data = r.json()
        
        try:
            if data[u'status'] == 'Success':
                id_equipamento = int(data[u'id_equipamento'])
                tipo_acesso = int(data[u'co_tipo_acesso'])
                nu_rele = int(data[u'nu_rele'])
                print('Conexão identificada {0}'.format(id_equipamento))
                #  self.travarPorta(nu_rele, ip)
            else:
                print('Equipamento desconhecido')
                client.close()
                
        except Exception as err:
            print('Erro de conexão, {}'.format(err))
            client.close()
               

        size = 1024
        array = ""
        while True:
            try:
                data = client.recv(size)
                print('Received from {} at {}:{} card: {}'.format(id_equipamento, ip, self.port, data))
                if data:
                    for b in data:
                        b = "{:02X}".format(b)
                        if b == '1B':
                            nu_identificador = bytes.fromhex(array).decode()
                            array = ""
                            # start access thread
                            print('Received from {} at {}:{} card: {}'.format(id_equipamento, ip, self.port, nu_identificador))
                            threading.Thread(target = self.solicitaAcesso,args = (id_equipamento, nu_identificador, tipo_acesso, nu_rele, ip)).start()

                        elif b == '02':
                            array = ""
                        elif b != '0D' and b != '03':
                            array += b
                    
                else:
                    raise error('Client disconnected')
            except Exception as err:
                client.close()
                print(err)
                return False

if __name__ == "__main__":
    while True:
        port_num = 4001 #input("Port? ")
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass

    threading.Thread(target = ThreadedServer,args = ('',4001)).start()
    threading.Thread(target = ThreadedServer,args = ('',4002)).start()
    threading.Thread(target = ThreadedServer,args = ('',4003)).start()
    threading.Thread(target = ThreadedServer,args = ('',4004)).start()
