# author : Amrit Pandey, 207907, MCA
# Write a Python Program to implement the UDP Server and Client that make use of the
# localhost IP address.

import socket

server = "localhost"
port = 9000
size = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server, port))

print("Server is now running")

while True:
    msg, client = server_socket.recvfrom(size)
    msg = msg.decode('utf-8')
    addr, port = client
    print(f"[{addr}:{port}] : {msg}")

