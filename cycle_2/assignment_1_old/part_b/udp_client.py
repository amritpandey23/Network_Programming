# b. Setup a UdpClient on one Node1 and a UdpServer on Node2. Let it be of a fixed data rate Rate1

import socket
from time import sleep

server_addr = "localhost"
server_port = 8000
data_rate = 5 # 5 messages / second

# udp client socket
udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = input("Enter your message : ")
counter = 1

while True:
    udp_client_socket.sendto(f"{message} : {counter}".encode("utf-8"), (server_addr, server_port))
    counter += 1
    sleep(1/data_rate)
