# Author: Amrit Pandey, MCA Year 2, 207907

# id
# offset
# mf
# header len
# total len

import socket

SERVER_ADDR = ("localhost", 8080)
MTU = 200

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
msg = "connect".encode('utf-8')

# connect to server to receive message
client.sendto(msg, SERVER_ADDR)

# recieve first fragment
msg, server = client.recvfrom(MTU)
frag_id, offset, mf, hl, tl, data = msg.decode('utf-8').split(';')

# if more fragments are incoming
while True:
    print(f"ID:{frag_id}\nOFFSET:{offset}\nMF:{mf}\nHL:{hl}\nTL:{tl}\nDATA:{data}")
    print("\n")
    msg, server = client.recvfrom(MTU)
    if mf == '0':
        break
    try:
        frag_id, offset, mf, hl, tl, data = msg.decode('utf-8').split(';')
    except ValueError as e:
        break

