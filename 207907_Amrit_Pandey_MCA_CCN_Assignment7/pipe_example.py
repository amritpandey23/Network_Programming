# Write a Python Program to implement Client Server example using Pipes, FIFOs, Message
# Queues, Shared Memory
# Part1 : Example using pipes
# The client requests file names to server
# to check if they exist on server and then
# server responds to client using IPC channel
# created using Pipe

from multiprocessing import Pipe, Process
from os import path

# file handles as request
msgs = ["hello.txt", "helloworld.md", "amritpandey.txt", "end"]

def client(conn, msgs):
    for msg in msgs:
        conn.send(msg)
    r = conn.recv()
    while r:
        print(f"SERVER: {r}")
        r = conn.recv()

def server(conn):
    while True:
        file_path = conn.recv()
        if file_path == "end":
            break
        print(f"CLIENT: Request({file_path})")
        if path.isfile(file_path):
            conn.send(f"{file_path} exist on server")
        else:
            conn.send(f"{file_path}: No file with such name found")

parent_conn, child_conn = Pipe()

# Process 1
p1 = Process(target=client, args = (parent_conn, msgs))

# Process 2
p2 = Process(target=server, args = (child_conn,))

try:
    p1.start()
    p2.start()
    p1.join()
    p2.join()
except KeyboardInterrupt:
    print("Cancelled by user")
    sys.exit(0)

