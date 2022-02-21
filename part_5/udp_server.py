# author: Amrit Pandey, 207907, MCA

import socket
import string
import random
from io import StringIO

addr = "localhost"
port = 9090
data_len = 5000 
response_msg = ''.join(random.choices(string.ascii_uppercase, k = data_len))

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((addr, port))

while True:
    msg, client = server.recvfrom(1024)
    ads, prt = client
    print(f"Received Request from {ads}:{prt}")
    str = StringIO(response_msg)
    chunk = str.read(512)
    while chunk:
        server.sendto(chunk.encode('utf-8'), (ads, prt))
        chunk = str.read(512)
    # after all the data is send we'll send
    # a trailer message to stop listening
    # for new message
    server.sendto("over".encode('utf-8'), (ads,prt))
    print(f"Data transmission to {ads}:{prt} complete")

