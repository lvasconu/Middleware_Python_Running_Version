# Setting to work in a Global Access server:

# Setting what kind of solution and database will be used:
#   True for complete Global Access solution, with SQL Server database, API in .Net Core, Dashboard, etc.
#   False for simple solution, in which database is in this same file.
global_access = True

# Parameters to communicate with API:
API_IP = '10.19.1.222' # IP from server where API is installed.
API_Port = 5865
API_URL = f'http://{API_IP}:{API_Port}/GlobalAccess/api/'  # Building API url. E.g.: http://localhost:5865/GlobalAccess/api/

# Parameters to communicate with Front End WebSocket server:
web_socket_server_ip = 'localhost'
web_socket_server_port = 5866
web_socket_url = f'ws://{web_socket_server_ip}:{web_socket_server_port}/ws/dashboard/'    # TODO: add /GlobalAccess/ to URL.