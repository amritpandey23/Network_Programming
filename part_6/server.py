# author: Amrit Pandey, 207907, MCA
#
import socket

addr = "localhost"
port = 8080
size = 1024
backlog = 5

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((addr,port))

print("Server is now running ...")
server.listen(backlog)

while True:
    client, addr = server.accept()
    msg = client.recv(size).decode('utf-8')
    print(f"Message received: {msg}")
    client.send(msg.encode('utf-8'))
    client.close()

