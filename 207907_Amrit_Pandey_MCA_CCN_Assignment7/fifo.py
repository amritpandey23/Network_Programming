def server():
    pipeout = open("fifo_server", "w")
    with open("fifo_client", "r") as f:
        for line in f:
            pipeout.write(line)

server()
