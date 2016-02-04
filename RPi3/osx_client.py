"""

To run:
ssh pi@192.168.43.20
sudo python kzpy3/RPi2/RPi_server.py
sudo python kzpy3/RPi2/camera_control3.py
ipython --pylab osx kzpy3/RPi2/osx_gui_client.py ; reset

"""

from kzpy3.utils import *

print "Client Side:"
import socket
host = '192.168.43.20'
#host = 'localhost'
port = 5000
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((host, port))

while True:
    clientsocket.send(d2s(time.time()))
    time.sleep(0.1)

