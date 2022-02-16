# author: Amrit Pandey, 207907, MCA
import socket
from time import sleep

server = "localhost"
port = 8080
timeout = 2 # seconds
total_requests = 10 # of 10 requests only 5 will be answered

msg = input("Enter your messge: ")

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# if the response is not received the
# client will keep waiting for it
# infinitely, so we need to fix this.

client.settimeout(timeout)

while total_requests > 0:
    # here I've tried to build some
    # form of reliability into the
    # client code. The client will
    # only wait for 2 seconds before
    # skipping the response from
    # server
    try:
        client.sendto(msg.encode('utf-8'), (server, port))
        print(f'Message({total_requests}) sent: OK')
        m, s = client.recvfrom(1024)
        print(m.decode('utf-8'))
    except socket.timeout:
        print(f'response({total_requests}) not received, skipping ...')
    total_requests -= 1
    sleep(1)

