"""

To run:
ssh pi@192.168.43.20
sudo python kzpy3/RPi3/RPi_server.py
sudo python kzpy3/RPi2/camera_control3.py
ipython kzpy3/RPi3/osx_client.py ; reset

"""

from kzpy3.utils import *
print "Client Side:"

import serial
ser = serial.Serial('/dev/tty.usbmodem1411',9600)



import socket
host = '192.168.43.20'
#host = 'localhost'
port = 5000
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((host, port))

sent_t = time.time()
send_wait = 0.1

while True:
    s = ser.readline()
    t = time.time()
    if t - sent_t > send_wait:
        sent_t = t
        clientsocket.send(d2s(t))
        #print(s)

