from kzpy3.utils import *
import serial





if '/Users/' in home_path:
    ser = serial.Serial('/dev/tty.usbmodem1461',9600) #115200)
else:
    ser = serial.Serial('/dev/ttyACM1',9600)
ctr = 0
t0 = time.time()

f = open(opjD('teg_data','_'+time_str()+'.GPS_acc.txt'), 'w')

while True:
    ctr += 1
    try:
        s = ser.readline()
        exec('t = ' + s)
        assert(type(t) == tuple)
        t = list(t)
        t.append(time.time())
        if t[0] == 456:
            t[0] = 'acc'
        elif t[0] == 123:
            t[0] = 'GPS'
        f.write(d2s(t,'\n'))
        #print t
        
    except Exception,e:
        print e

