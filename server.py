import socket
from _thread import *
import sys

server = "192.168.1.3"
port =5555
my_socket = socket.socket()
try:
    my_socket.bind((server, port))

except socket.error as e:
    print(str(e))

my_socket.listen(2)
print("waiting for connection,server started")


def thread_client(conn):
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")
            if not data:
                print("disconnect!")
                break
            else:
                print("Received : " + reply)
                print("Sending : " + reply)
            conn.sendall(str.encode(reply))
        except:
            break


while True:
    conn, addr = my_socket.accept()
    print("connected to : ", addr)

    start_new_thread(thread_client, (conn,))
