# Author: Amrit Pandey, MCA Year 2, 207907
# Experiment 2 (Server code)
# CCN Mid Lab Exam

import socket

server_addr = ("localhost", 8080)
SIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(server_addr)

while True:
    client_msg, client = server.recvfrom(SIZE)
    client_msg = client_msg.decode('utf-8')
    if client_msg == "kill":
        break
    addr, port = client
    print(f"Received from {addr}:{port} = ", client_msg)
    server.sendto(client_msg.encode('utf-8'), (addr, port))

