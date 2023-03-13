
#################################################################################################################
# Internet Relay Chat
# Authors :  Vysali Kallepalli
#            Juhi Augustine Kamaraj Nalli             
# Date    :  11/29/2022          
# Title   :  irc_util.py                           
# Purpose :  Defined functions such as join, switch and leave a room, and communicate in private or a group.
#################################################################################################################

import socket

MAX_CLIENTS = 25

QUIT_CODE = '<$quit$>'
NAME = 'name:'
JOIN = '<join>'
LIST = '<list>'
MANUAL = '<manual>'
LEAVE = '<leave>'
QUIT = '<quit>'
SWITCH = '<switch>'
PERSONAL = '<personal>'
        
INSTRUCTIONS = b'Instructions:\n'\
    + b'Use [<list>]\t\t\t--> List all rooms\n'\
    + b'Use [<join> room_name]\t\t--> Join/Create/Switch to a room\n' \
    + b'Use [<personal> member_name]\t--> To send a private Message\n'\
    + b'Use [<manual>]\t\t\t--> Display instructions again\n' \
    + b'Use [<switch>]\t\t\t--> Switch to a room\n' \
    + b'Use [<leave>]\t\t\t--> Leave the room\n'\
    + b'Use [<quit>]\t\t\t--> Quit\n' \
    + b'Else, have fun!' \
    + b'\n'

LIST_ROOMS_AND_MEMBERS_MESSAGE = 'List of current rooms and members.\n'
WELCOME_MESSAGE = b'Welcome to Social Intents.\nEnter your name:\n'
LEAVE_ROOM_ERROR = "You’re not a part of the room.\n"
ROOM_DOESNT_EXIST = "Entered room doesn't exist \n"
SWITCH_ROOM_ERROR = "You are not a part of the room.\nJoin the room before switching.\n"
NO_ACTIVE_ROOMS_MESSAGE = 'There are no active rooms. Create your own room!\n' \
                + 'Use [<join> room_name] to create a room.\n'
PERSONAL_MESSAGE_ERROR = "Entered user does not exist!!"
NOT_PART_OF_ANY_ROOM_ERROR = 'You are currently not a part of any room! \n' \
                    + 'Use [<list>] to see available rooms! \n' \
                    + 'Use [<join> room_name] to join a room! \n'

def create_socket(address):
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    new_socket.setblocking(0)
    new_socket.bind(address)
    new_socket.listen(MAX_CLIENTS)
    print("Listening to: ", address)
    return new_socket

class IRC_Chat:
    def __init__(self):
        self.rooms = {} 
        self.room_member_map = {} 
        self.users_map = {} 

    def welcome(self, new_user):
        new_user.socket.sendall(WELCOME_MESSAGE)

    def list_rooms(self, user):
        if len(self.rooms) == 0:
            user.socket.sendall(NO_ACTIVE_ROOMS_MESSAGE.encode())
        else:
            message = LIST_ROOMS_AND_MEMBERS_MESSAGE
            for room in self.rooms:
                if 'personal' not in room:
                    members = self.rooms[room].members
                    print(members)
                    message += room + ': ' + str(len(members)) + ' member(s)\n'
                    for member in members:
                        message += member.name + '\n'
            user.socket.sendall(message.encode())

    def handle_message(self, user, message):

        print(user.name + ': ' + message)
        if NAME in message:
            name = message.split()[1]
            user.name = name
            print("New connection from:", user.name)
            self.users_map[user.name]=user
            user.socket.sendall(INSTRUCTIONS)

        elif JOIN in message:
            different_room = True
            if len(message.split()) >= 2: # error check
                room_name = message.split()[1]
                user.current_room = room_name
                if user.name + '-' + room_name in self.room_member_map:
                    if self.room_member_map[user.name + '-' + room_name] == room_name:
                        user.socket.sendall(b'You are already present in the room: ' + room_name.encode() + b'\n')
                        different_room = False
                if different_room:
                    if not room_name in self.rooms: # new room:
                        new_room = Room(room_name)
                        self.rooms[room_name] = new_room
                    self.rooms[room_name].members.append(user)
                    self.rooms[room_name].welcome(user)
                    self.room_member_map[user.name + '-' + room_name] = room_name
            else:
                user.socket.sendall(INSTRUCTIONS)

        elif LIST in message:
            print(self.rooms)
            print(self.room_member_map)
            self.list_rooms(user) 

        elif MANUAL in message:
            user.socket.sendall(INSTRUCTIONS)
        
        elif LEAVE in message:
            if len(message.split()) >= 2: # error check
                room_name = message.split()[1]
                if not room_name in self.rooms:
                    user.socket.sendall(ROOM_DOESNT_EXIST.encode())
                else:
                    if user.name + '-' + room_name in self.room_member_map:
                        del self.room_member_map[user.name + '-' + user.current_room]
                        self.rooms[room_name].remove_user(user)
                        print("User: " + user.name + " has left " + room_name + '\n')
                        if len(self.rooms[room_name].members) == 0:
                            del self.rooms[room_name]
                    else:
                        user.socket.sendall(LEAVE_ROOM_ERROR.encode())
            else:
                user.socket.sendall(INSTRUCTIONS)

        
        elif QUIT in message:
            user.socket.sendall(QUIT_CODE.encode())
            self.remove_user(user)
            
        elif SWITCH in message:
            if len(message.split()) >= 2:
                switchroomname=message.split()[1]
                if user.name+"-"+switchroomname in self.room_member_map:
                    user.current_room = switchroomname
                else:
                    user.socket.sendall(SWITCH_ROOM_ERROR.encode())
            else:
                user.socket.sendall(INSTRUCTIONS)

        elif PERSONAL in message:
            if len(message.split()) >= 2:
                sender_name = user.name
                receiver_name = message.split()[1]
                if receiver_name in self.users_map:
                    sender = user
                    receiver = self.users_map[receiver_name]
                    room_name = "personal-" + sender_name + "-" + receiver_name
                    personal_room = Room(room_name)
                    personal_room.members.append(sender)
                    personal_room.members.append(receiver)
                    self.rooms[room_name] = personal_room
                    self.room_member_map[sender_name + "-" + room_name] = room_name
                    self.room_member_map[receiver_name + "-" + room_name] = room_name
                    sender.current_room = room_name
                    receiver.current_room = room_name
                else:
                    user.socket.sendall(PERSONAL_MESSAGE_ERROR.encode())
            else:
                user.socket.sendall(INSTRUCTIONS)

        elif not message:
            self.remove_user(user)
            
        else:
            # check if in a room or not first
            if user.name + "-" + user.current_room in self.room_member_map:
                self.rooms[self.room_member_map[user.name + "-" + user.current_room]].broadcast(user, message.encode())
            else:
                user.socket.sendall(NOT_PART_OF_ANY_ROOM_ERROR.encode())
    
    def remove_user(self, user):
        if user.name +"-"+user.current_room in self.room_member_map:
            self.rooms[self.room_member_map[user.name + "-" + user.current_room]].remove(user)
            del self.room_member_map[user.name + "-" + user.current_room]
        print("User: " + user.name + " has left\n")
    
class Room:
    def __init__(self, name):
        self.members = []
        self.name = name

    def welcome(self, from_member):
        message = self.name + " welcomes: " + from_member.name + '\n'
        for member in self.members:
            member.socket.sendall(message.encode())
    
    def broadcast(self, from_member, message):
        message = from_member.name.encode() + b":" + message
        for member in self.members:
            member.socket.sendall(message)

    def remove_user(self, member):
        self.members.remove(member)
        leave_msg = member.name.encode() + b" has left the room\n"
        self.broadcast(member, leave_msg)

class User:
    def __init__(self, socket, name = 'new' , current_room = 'new'):
        socket.setblocking(0)
        self.socket = socket
        self.name = name
        self.current_room = current_room
    
    def fileno(self):
        return self.socket.fileno()

    