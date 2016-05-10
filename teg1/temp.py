from kzpy3.utils import *

ports = serial_ports()
slist = []
baud = 115200

for p in ports:
	slist.append(serial.Serial(p,baud))

while True:
	for s in slist:
		print s.readline()
