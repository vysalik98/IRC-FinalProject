
####################################################################
# Internet Relay Chat
# Authors :  Vysali Kallepalli
#            Juhi Augustine Kamaraj Nalli             
# Date    :  11/29/2022 
# Title   :  irc_server.py                        
# Purpose :  Implements 3-tier structure Room -> Chat -> Clients
# Usage   :  python3 -m irc_server.py
####################################################################


import select
from irc_util import IRC_Chat, User
import irc_util

READ_BUFFER = 4096

server_socket = irc_util.create_socket(('127.0.0.1', 4678))
irc_chat = IRC_Chat()
connections = [server_socket]

while True:

    read_sockets, write_sockets, error_sockets = select.select(connections, [], [])
       
    for user in read_sockets:
        if user is server_socket: 
            new_socket, add = user.accept()
            new_user = User(new_socket)
            connections.append(new_user)
            irc_chat.welcome(new_user)
	
        else: 
            message = user.socket.recv(READ_BUFFER)
            if not message:
                irc_chat.remove_user(user)
            if message:
                message = message.decode().lower()
                irc_chat.handle_message(user, message)
            else:
                user.socket.close()
                connections.remove(user)
    
    for error_socket in error_sockets: 
        error_socket.close()
        connections.remove(error_socket)
