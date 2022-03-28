# author : Amrit Pandey, 207907, MCA
# Write a Python program to ask the operating system (Linux, Mac OS, and Windows) for
# resolving the hostname (www.google.com.org.) into IP address using the particular network
# service, called the Domain Name System. i.e (Hostname into an IP Address);

import socket

hostname = "www.google.com"

print(f"IP address of {hostname} : {socket.gethostbyname(hostname)}")

