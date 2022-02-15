import socket

def is_busy(location, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    check = s.connect_ex((location, port))
    if check == 1:
        return True
    return False

print(is_busy("localhost",8080))
