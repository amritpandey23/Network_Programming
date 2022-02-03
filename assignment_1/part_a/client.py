# a. Create a simple topology of two nodes (Node1, Node2) separated by a point-to-point link.

import socket

server = "localhost" # address of server
port = 8000 # port of server application
size = 1024 # size limit of data to receive

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # initialized a new client
client.connect((server, port)) # connect to server

message = input("Type message : ")

client.send(message.encode("utf-8")) # send message to server
msg = client.recv(size) # receive back message form server
print(f"Message Received back: {msg.decode('utf-8')}")
