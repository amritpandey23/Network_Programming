import socket, threading

server_address = "localhost"
server_port = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_address, server_port))

def handle_client(conn, addr):
    while True:
        msg = conn.recv(1024)
        print(f"{addr}: {msg.decode('utf-8')}")
        conn.send("message received".encode('utf-8'))
        if msg.decode('utf-8') == 'end':
            break
    conn.close()

server.listen()
print(f"Server is started at {server_address}:{server_port}")

while True:
    conn, addr = server.accept()
    # handle client
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print(f"{addr} is been handled concurrently")

