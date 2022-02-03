# Now add another client application to Node1 and a server instance to Node2. What do
# you need to configure to ensure that there is no conflict?

import socket
from time import sleep
from port_busy_check import is_busy

server_addr = "localhost"
data_rate = 2 # 5 messages / second

# udp client socket
udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = input("Enter your message : ")
server_port = int(input("Destination server port: "))

counter = 1

while True: # keep echoing data to server
    udp_client_socket.sendto(f"{message} : {counter}".encode("utf-8"), (server_addr, server_port))
    counter += 1
    sleep(1/data_rate)

