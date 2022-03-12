# Author: Amrit Pandey, MCA Year 2, 207907
# Experiment 3 (Server code)
# CCN Mid Lab Exam

import socket, string, random
from io import StringIO

SOCKET_ADDR = ("localhost", 8080)
MTU = 200 # bytes (including header)
HEADER_LEN = 20 # for specifying offset, mf, etc.

UDP_PACKET_SIZE = 1000 # bytes

# randomly generated data 
PACKET = ''.join(random.choices(string.ascii_uppercase, k = UDP_PACKET_SIZE))

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(SOCKET_ADDR)

#           ALGORITHM 
# Each msg that's been sent will have
# header and payload. Header will have
# information such as:
#
#   ID (Payload id)
#   Offset
#   MF (More fragment bit)
#   Header len (HL)
#   Total len (TL)
# 
# The big udp packet will then be
# broken off into smaller fragments
# having the above fields and sent
# to client.

while True:
    # receive client request
    msg, client = server.recvfrom(1024)
    addr, port = client
    print(f"Received Request from {addr}:{port}")

    # choosing random starting id
    id = int(random.random() * 1000)
    # initially offet is set to 0
    # i.e. no fragment were sent before
    # first fragment
    offset = 0
    mf = 1 # default an end fragment

    # break large packet to small part of
    # size(mtu - HEADER_LEN)
    strin = StringIO(PACKET)
    read_len = MTU - HEADER_LEN
    part = strin.read(read_len)

    while mf != 0:
        total_len = HEADER_LEN + len(part);
        # Fragment creation
        header = f"{id};{offset};{mf};{HEADER_LEN};{total_len}"
        # pad space for extra len left
        header += " " * (HEADER_LEN - len(header))
        fragment = header + ";" + part
        fragment = fragment.encode('utf-8')
        server.sendto(fragment, (addr, port))

        part = strin.read(read_len)
        # if message over set mf = 0
        if not part:
            mf = 0
        if part:
            offset += total_len
        id += 1
    # after all the data is send we'll send
    # a tailer message to stop listening
    # for new message
    server.sendto("over".encode('utf-8'), (addr,port))
    print(f"Data transmission to {addr}:{port} complete")

