# author : Amrit Pandey, 207907, MCA
# Write a Python Program to implement the UDP Server and Client that make use of the
# localhost IP address.

import socket

server = "localhost"
port = 9000

msg = input("Enter your message : ")

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto(msg.encode('utf-8'), (server, port))

print(client.recvfrom(1024))

