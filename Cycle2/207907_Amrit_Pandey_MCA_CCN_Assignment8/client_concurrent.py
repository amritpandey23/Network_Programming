import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("localhost", 8080))

client.send("hello".encode("utf-8"))

while True:
    user_msg = input("Enter your message " )
    if user_msg == "end":
        break
    client.send(user_msg.encode("utf-8"))

