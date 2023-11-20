# Internet Relay Chat (IRC)

### Overview
This project is an implementation of a simplified version of the Internet Relay Chat protocol (IRC) that facilitates inter-client communication. The IRC system comprises a single-server architecture, allowing users to create, enter, and exit rooms, as well as engage in private messaging. The primary goal is to provide a simple and efficient means of communication for multiple clients.

### Key Features
One-to-one, one-to-many, and one-to-all communication modes
Support for multiple rooms
Private messaging between users
Room creation and destruction
User presence tracking
Error handling

### Usage
To run the IRC application, you will need to clone the repository, start the server and connect to it using a client.

1. Clone the repository
```git clone https://github.com/<your-username>/irc.git```

2. Start the server
```python server.py```

3. Start the client
```python client.py```

## Specifications

### Modes of Communication
The IRC system supports one-to-one, one-to-many, and one-to-all communication modes through rooms and private conversations. Messages are distributed within rooms, resembling dynamic multicasting, with the sender excluded.

### Character Codes
There is no limit on the number of ASCII characters in a message, and spaces act as delimiters.

### Messages
Communication involves payloads, transaction IDs, and instruction names, separated by spaces. Transaction IDs increment for each client message, while server-to-client messages maintain a constant 0 ID.

### Replies
Every message to the server generates a numerical response, indicating transaction ID and request status. A status of 0 denotes success, while non-zero values signify errors.

### Client Message Infrastructure

### Create Room
Clients can initiate a room using the "$join room_name" command. Other users can then view and join this room for conversation.

### Join a Room
The "$list" command displays available rooms, and "$join room_name" lets users join or create rooms. Users within a room can be listed using appropriate commands.

### Leave Room
Clients can exit a room with "$leave room_name." The room persists if other users are present; otherwise, it is automatically deleted.

### Switch Rooms
Users part of multiple rooms can switch between them using "$switch room_name" to communicate with specific groups.

### IRC Concepts
One-to-One Communication
Clients can engage in private conversations visible only to the sender and recipient.

### One-to-Many Communication
Users within a room can communicate with each other.

### One-to-All Communication
Clients can broadcast messages to every client and server.

### Error Handling
The system includes error messages for various scenarios, such as attempting to send messages to unjoined rooms or leaving non-existent rooms.

### Additional Notes

To connect to the IRC server, use the provided IP address: 127.0.0.1.
The server runs on port 5000 by default.
The server handles communication between clients, who can create rooms, join existing ones, and exchange messages. 
Clients are identified by unique names, limited to 20 alphanumeric characters, including underscores.
The client can use the $help command to get a list of available commands.
