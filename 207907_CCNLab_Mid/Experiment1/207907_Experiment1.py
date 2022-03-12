# Author: Amrit Pandey, MCA Year 2, 207907
# Experiment 1
# CCN Mid Lab Exam

import socket

def ip_address(hostname):
    records = socket.getaddrinfo(hostname, 80) # selecting HTTP port as default
    a, b, c, d, e = list(records)[0]
    ip, port = e
    return ip

hostname = input("Enter Hostname: ")
print(f"{hostname} : {ip_address(hostname)}")

