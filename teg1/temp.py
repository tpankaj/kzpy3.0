from kzpy3.utils import *

ports = serial_ports()
print ports
slist = []
BAUD = 115200
TIMEOUT = 0.01

for p in ports:
	if 'tty.usbmodem' in p or 'ttyACM' in p:
		slist.append(serial.Serial(p,BAUD,timeout=TIMEOUT))

if len(slist) > 0:
	while True:
		for s in slist:
			d = s.readline()
			#print  (len(d),type(d))
			if '(' in d:#len(d) > 1:
				print d
			time.sleep(0.0)
else:
	print 'no ports!!!'


for s in slist:
    s.close()