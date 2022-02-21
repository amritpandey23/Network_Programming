# author: Amrit Pandey, 207907, MCA
# Write a Python Program to Send a Large UDP Packet from Server to Client using
# Fragmentation

import socket

server = "localhost"
port = 9090

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

msg = "get data".encode('utf-8')

client.sendto(msg, (server,port))

msg, server = client.recvfrom(512)

while msg != 'over':
    print(msg)
    msg, server = client.recvfrom(512)
    msg = msg.decode('utf-8')

