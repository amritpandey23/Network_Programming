# d. Now add another client application to Node1 and a server instance to Node2. What do
# you need to configure to ensure that there is no conflict?

# we need to create multiple servers with different port numbers
import socket
from port_busy_check import is_busy

server_addr = "localhost"
server_port = 8000
size = 1024

server_nameid = input("Enter server name: ")
server_port = int(input("Enter server port number: "))

while is_busy(server_addr, server_port):
    print(f"{server_port} is busy, please choose another")
    server_port = int(input("Enter server port number"))

udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # udp server
udp_server_socket.bind((server_addr, server_port))

print(f"Server Name : {server_nameid}")
print(f"Server is now running at {server_addr}:{server_port}")

while True:
    msg, udp_client = udp_server_socket.recvfrom(size)
    msg = msg.decode("utf-8")
    addr, port = udp_client
    print(f"Recv([{addr}:{port}]) : {msg}")

