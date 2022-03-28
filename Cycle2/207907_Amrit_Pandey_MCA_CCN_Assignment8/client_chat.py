import socket


server_addr = "localhost"
server_port = 8080


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_addr, server_port))


while True:
    msg = client.recv(1024)
    print(f"SERVER: {msg.decode('utf-8')}")
    sender_msg = input()
    client.send(sender_msg.encode('utf-8'))

