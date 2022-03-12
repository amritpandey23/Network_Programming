# Author: Amrit Pandey, MCA Year 2, 207907
# CCN Mid Lab Exam
# Experiment 2 (Client code)

import socket

server_addr = ("localhost", 8080)
SIZE = 1024 # bytes

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    user_msg = input("Enter Message: ")
    if user_msg == "kill":
        client.sendto(user_msg.encode('utf-8'), server_addr)
        break
    user_msg = user_msg.encode("utf-8")
    client.sendto(user_msg, server_addr)
    msg, s = client.recvfrom(SIZE)
    print("Message Received: ", msg.decode('utf-8'))

