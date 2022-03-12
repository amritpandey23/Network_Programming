# Author: Amrit Pandey, MCA Year 2, 207907
# Experiment 1
# CCN Mid Lab Exam

import socket

def ip_address(hostname):
    records = socket.getaddrinfo(hostname, 80) # selecting HTTP port as default
    return list(records)[0]

hostname = input("Enter Hostname: ")
print(ip_address(hostname))

