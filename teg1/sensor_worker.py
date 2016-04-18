from kzpy3.utils import *
import serial





if '/Users/' in home_path:
    ser = serial.Serial('/dev/tty.usbmodem1461',9600) #115200)
else:
    ser = serial.Serial('/dev/ttyACM0',9600)
ctr = 0
t0 = time.time()

f = open(opjD('teg_data',time_str()+'.GPS_acc.txt'), 'w')

while True:
    ctr += 1
    try:
        s = ser.readline()
        exec('t = ' + s)
        assert(type(t) == tuple)
        f.write(d2s(time.time(),t,'\n'))
        print t
        
    except Exception,e:
        print e

