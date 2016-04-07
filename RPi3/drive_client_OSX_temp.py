"""

To run:
ssh pi@192.168.43.20
sudo python kzpy3/RPi3/RPi_server.py
python kzpy3/RPi3/osx_client.py

"""
CAFFE_DRIVE = False
from kzpy3.utils import *
print os.path.basename(sys.argv[0])

import serial

ser = serial.Serial('/dev/tty.usbmodem1461',9600)#115200)#
#ser = serial.Serial('/dev/ttyACM0',9600)
#ser = serial.Serial('/dev/tty.usbmodem1411',9600)



ctr = 0
sent_t = time.time()
wait_t = 0.1
while True:
        steer = ser.readline()
        print steer
        #steer = steer.split("""\r""")[-1]
        
        steer = int(steer)
        steer -= 1096
        steer /= (1872.0-1096.0)
        steer *= 180
        steer = int(steer)
        if steer < 0:
            steer = 0
        if steer > 180:
            steer = 180
        print steer
        ser.write(d2s(steer,ctr,'\n'))#,ctr+50,ctr+100))
        ctr += 1

"""
    except KeyboardInterrupt:
        sys.exit()
    except Exception, e:
        print(d2s(os.path.basename(sys.argv[0]),':',e))
"""    


# 1096,1872