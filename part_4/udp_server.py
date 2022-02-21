# author : Amrit Pandey, 207907, MCA

# Write a Python Program to implement the UDP Server and Client on Different Machines
# (Note : Instead of always answering to client requests, The server should randomly chooses
# to answer only half of the requests coming in from clients, which will let you see how to build
# reliability into your client code without waiting what might be hours for a real dropped packet
# to occur on your network).

import socket

addr = "localhost"
port = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((addr, port))

flip = 0 # flip (send/not send)

print('Server is now running...')

while True:
    msg, client = server.recvfrom(1024)
    ad, prt = client
    msg = msg.decode('utf-8')
    print(msg)
    if flip % 2 == 0:
        # only going to respond if the flip is 0
        # this way only half the request will be
        # answered to the client
        server.sendto(f"msg received.{flip}".encode('utf-8'), (ad,prt))
    flip = abs(flip - 1)


