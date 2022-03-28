# author: Amrit Pandey, 207907, MCA
# Write a Python Program to implement Simple TCP Server and Client
#
import socket

server = "localhost"
port = 8080
size = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server,port))

msg = input("Enter message: ")

client.send(msg.encode('utf-8'))

msg = client.recv(size)

print(f"Response Received: {msg.decode('utf-8')}")

