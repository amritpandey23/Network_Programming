import socket
import threading


addr = "localhost"
port = 8080


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((addr, port))


server.listen()


clients = []


def announce(message, conn, addr):
    # send message to all
    for c in clients:
        if conn != c:
            c.send(f"{addr}: {message.decode('utf-8')}".encode('utf-8'))


def handle_client(conn, addr):
    # start new client chat
    clients.append(conn)
    conn.send(">>".encode('utf-8'))
    while True:
        msg = conn.recv(1024)
        if msg.decode("utf-8") == "end":
            break
        announce(msg, conn, addr)
    conn.close()
    clients.remove(conn)


# accept new connection
while True:
    # handle new client
    conn, addr = server.accept()
    conn.send("Welcome to Amrit's chat server".encode('utf-8'))
    print(f"{addr} was connected successfully!")
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()

