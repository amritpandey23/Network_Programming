# author: Amrit Pandey, 207907, MCA
# Write a Python Program to Send a Large UDP Packet from Server to Client using
# Fragmentation

# id
# offset
# mf
# header len
# total len

import socket

server = "localhost"
port = 9090
mtu = 200

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

msg = "get data".encode('utf-8')

client.sendto(msg, (server,port))

msg, server = client.recvfrom(mtu)
id, offset, mf, hl, tl, data = msg.decode('utf-8').split(';')

while True:
    print(f"ID:{id}\nOFFSET:{offset}\nMF:{mf}\nHL:{hl}\nTL:{tl}\nDATA:{data}")
    msg, server = client.recvfrom(mtu)
    id, offset, mf, hl, tl, data = msg.decode('utf-8').split(';')
    if mf == '0':
        print(f"ID:{id}\nOFFSET:{offset}\nMF:{mf}\nHL:{hl}\nTL:{tl}\nDATA:{data}")
        break


