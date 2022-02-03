import socket

server_addr = "localhost"
server_port = 8000
size = 1024

udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # udp server
udp_server_socket.bind((server_addr, server_port))

print("Server is now running...")
while True:
    msg, udp_client = udp_server_socket.recvfrom(size)
    msg = msg.decode("utf-8")
    addr, port = udp_client
    print(f"[{addr}:{port}] : {msg}")
