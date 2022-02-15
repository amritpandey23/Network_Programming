# author : Amrit Pandey, 207907, MCA
# Write a Python Program to communicate to google search simple socket. i.e. sending a raw
# text message across the Internet and receiving a bundle of text in return.

import socket

hostname = "www.google.com"
port = 80 # http port

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((hostname, port))

client.send(b'GET google.com/search?q=hello+world HTTP/1.1\n\n')

print(client.recv(4096).decode())

