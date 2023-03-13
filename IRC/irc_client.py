
#####################################################################
# Internet Relay Chat
# Authors :  Vysali Kallepalli
#            Juhi Augustine Kamaraj Nalli             
# Date    :  11/29/2022 
# Title   :  irc_client.py 
# Purpose : Client connection to the server
# Usage   : python3 irc_client.py [host] //hostname is optional
#####################################################################

import select,socket,sys

READ_BUFFER = 1000
QUIT = '<$quit$>'

server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_connection.connect(('127.0.0.1',4678)) #trying to connect to server

print("Connected to server\n")
message_prefix = ''
connections = [sys.stdin, server_connection]

def prompt_user():
	sys.stdout.write('<You>')
	sys.stdout.flush()
try:
	while True:
		read_sockets, write_sockets, error_sockets = select.select(connections, [], [])
		
		for user in read_sockets:
			if user is server_connection: # incoming message 
				message = user.recv(READ_BUFFER)
				if not message:
					print("Server is down!")
					sys.exit(2)
				else:
					if message == QUIT.encode(): #MSG COMING FROM SERVER
						sys.stdout.write('Bye\n')
						sys.exit(2)
					else:
						sys.stdout.write(message.decode())
						if 'Enter your name' in message.decode():
							message_prefix = 'name: ' # identifier for name
						else:
							message_prefix = ''
						prompt_user()

			else:
				message = message_prefix + sys.stdin.readline()
				server_connection.sendall(message.encode())
finally:
	sys.exit(2)
		