from kzpy3.utils import *
import serial





if '/Users/' in home_path:
    ser = serial.Serial('/dev/tty.usbmodem1461',115200) #115200)
else:
    ser = serial.Serial('/dev/ttyACM0',115200)
ctr = 0
t0 = time.time()


while True:
    ctr += 1
    try:
        s = ser.readline()
        exec('t = ' + s)
        assert(type(t) == tuple)
        print t
        unix("""echo '""" + str(t)+"""' >> temp.txt""")
    except Exception,e:
        print e

