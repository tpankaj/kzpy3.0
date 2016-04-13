"""

To run:
ssh pi@192.168.43.20
sudo python kzpy3/RPi3/RPi_server.py
python kzpy3/RPi3/osx_client.py

"""

from kzpy3.utils import *

import serial

ser = serial.Serial('/dev/tty.usbmodem1461',9600)#115200)#
ctr = 0
t0 = time.time()
while True:
    ctr += 1
    try:
        #t1 = np.int16(1000*(time.time()-t0))
        #print ctr
        ser.write('(-30000)')
        #ser_line = ser.readline()
        #t2 = int(ser_line.split("""\\""")[0])
        #print (t1,t2,t2-t1)
        #time.sleep(0.001)
        print ser.readline()
    except Exception,e:
        print e

        
