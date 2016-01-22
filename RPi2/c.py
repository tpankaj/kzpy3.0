"Run d.py, then c.py, then b.py"

from kzpy3.utils import *
import socket

print("c.py Server/Client Side:")

host = '127.0.0.1' # 'localhost'
port = 5000



serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((host, port))
serversocket.listen(5) # become a server socket, maximum 5 connections

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((host, 5001))

connection, address = serversocket.accept()
while True:
    buf = connection.recv(64)
    if len(buf) > 0:
        print(buf)
        clientsocket.send(buf+buf)
        if buf == 'q':
            time.sleep(0.1)
            break


	

clientsocket.close()
serversocket.close()

