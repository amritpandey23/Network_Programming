# author: Amrit Pandey, 207907, MCA

import socket
import string
import random
from io import StringIO

addr = "localhost"
port = 9090
client_mtu = 200
header_len = 20

data_len = 1024
BIG_MESSAGE = ''.join(random.choices(string.ascii_uppercase, k = data_len))

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((addr, port))

# Each fragment will have following fields
# ID
# Offset
# MF
# Header len
# Total len

while True:
    msg, client = server.recvfrom(1024)
    ads, prt = client
    print(f"Received Request from {ads}:{prt}")
    id = int(random.random() * 1000)
    offset = 0
    mf = 1
    str = StringIO(BIG_MESSAGE)
    read_len = client_mtu - header_len
    chunk = str.read(read_len)
    while chunk:
        chunk = str.read(read_len)
        total_len = header_len + len(chunk);
        if not chunk:
            mf = 0
        header = f"{id};{offset};{mf};{header_len};{total_len}"
        header += " " * (header_len - len(header))
        data = header + ";" + chunk
        server.sendto(data.encode('utf-8'), (ads, prt))
        if chunk:
            offset += total_len
            total_len = header_len + len(chunk)
    # after all the data is send we'll send
    # a trailer message to stop listening
    # for new message
    server.sendto("over".encode('utf-8'), (ads,prt))
    print(f"Data transmission to {ads}:{prt} complete")

