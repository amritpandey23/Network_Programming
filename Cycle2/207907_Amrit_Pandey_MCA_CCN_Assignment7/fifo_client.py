msgs = ['myfile.txt', 'hello.txt']

def client():
    with open("fifo_client", "w") as f:
        for msg in msgs:
            f.write(msg)
    pipein = open("fifo_server", "r")
    while True:
        line = pipein.readLine()
        print(line)

client()

