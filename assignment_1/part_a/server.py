# a. Create a simple topology of two nodes (Node1, Node2) separated by a point-to-point link.

import socket

server_addr = "localhost" # seerver address
port = 8000 # port for hosting application
backlog = 5 # total number of connections to accept 
size = 1024 # size limit of message in bytes

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a server
server.bind((server_addr, port)) # bind address and port to server

print("Server is now running ... ")
server.listen(backlog) # start server
while True: # keep listening for new connections (infinitely)
    client, addr = server.accept() # accept connections
    msg = client.recv(size).decode("utf-8") # read message
    print(f"Message Received : {msg}")
    client.send(msg.encode("utf-8")) # send back a response
    client.close() # close connection
