import os

os.mkfifo("./fifo_client", 0o700)
os.mkfifo("./fifo_server", 0o700)

msgs = ['myfile.txt', 'hello.txt']

def client():
    with open("fifo_client", "w") as f:
        for msg in msgs:
            f.write(msg)
    
    pipein = open("fifo_server", "r")
    while True:
        line = pipein.readLine()
        print(line)

def server():
    pipeout = open("fifo_server", "w")
    with open("fifo_client", "r") as f:
        for line in f:
            pipeout.write(line) 
