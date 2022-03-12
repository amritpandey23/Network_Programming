import sys, socket, time

fd = open("fileinput", "r")

s = socket.fromfd(fd.fileno(), socket.AF_INET, socket.SOCK_STREAM)

s.sendall("Welcome")

