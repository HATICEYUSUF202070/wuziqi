import socket
from _thread import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 5555
server = 'localhost'

server_ip = socket.gethostbyname(server)
try:
    s.bind((server, port))
except socket.error as err:
    print(str(err))

s.listen(2)
print("waiting for a connection")

user_id = "0"
pos = ["0:50,50", "1:100,100"]


def threaded_clint(conn):
    global user_id, pos
    conn.send(str.encode(user_id))
    user_id = "1"
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                print("Recieved:" + reply)
                arr = reply.split(":")
                id = arr[0]
                pos[id] = reply
                if id == "0": n_id = "1"
                if id == "1": n_id = "0"
                reply = pos[n_id][:]
                print("Sending:" + reply)
        except:
            break
    print("Connection Closed")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_clint, (conn,))
