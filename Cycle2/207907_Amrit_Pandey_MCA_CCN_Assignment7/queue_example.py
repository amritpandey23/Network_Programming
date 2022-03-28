import os
import multiprocessing
from time import sleep

msgs = ['myfile.txt', 'path2']

def client(q):
    for msg in msgs:
        q.put(msg)


def server(q):
    while True:
        while q.empty() is False:
            filename = q.get()
            print(f"Request Received for {filename}")
            if os.path.isfile(filename):
                print(f">> {filename}: exists")
            else:
                print(f">> {filename}: not exist")
        sleep(2)


que = multiprocessing.Queue()
p1 = multiprocessing.Process(target=client, args=(que,))
p2 = multiprocessing.Process(target=server, args=(que,))


p2.start()
p1.start()


p2.join()
p1.join()


