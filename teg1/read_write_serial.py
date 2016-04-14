"""

To run:
ssh pi@192.168.43.20
sudo python kzpy3/RPi3/RPi_server.py
python kzpy3/RPi3/osx_client.py

"""

from kzpy3.utils import *
from kzpy3.RPi3.caffe_worker_no_py_layers_local import *

import serial

ser = serial.Serial('/dev/tty.usbmodem1461',9600)#115200)#
ctr = 0
t0 = time.time()

motor_null = 1528
servo_null = 1376
servo_max_cpu = 1888
servo_min_cpu = 928
motor_max_cpu = 2012
motor_min_cpu = 1220

cpu_int = -30000

def pwm_to_percent(in_pwm,min_pwm,pwm_null,max_pwm,scale_factor=1.0):
    if in_pwm >= pwm_null:
        out_percent = int(scale_factor*(in_pwm - pwm_null)/(1.0*max_pwm - 1.0*pwm_null)*50 + 49)
    else:
        out_percent = int(scale_factor*(in_pwm - pwm_null)/(1.0*pwm_null - 1.0*min_pwm)*49+49)
    assert(out_percent >=0 and out_percent < 100)
    return out_percent

def encode_int_signal(cpu_mode,cpu_steer,cpu_motor):
    assert(cpu_mode >= -3 and cpu_mode <= 3 )
    assert(cpu_steer >=0 and cpu_steer < 100)
    assert(cpu_motor >=0 and cpu_motor < 100)
    return 10000*cpu_mode + 100*cpu_steer + cpu_motor

while True:
    ctr += 1
    try:
        ser.write(d2s('(',cpu_int,')'))
        s = ser.readline()
        exec('t = ' + s)
        assert(type(t) == tuple)
        print t
        in_steer_pwm = t[1]
        in_motor_pwm = t[0]
        in_button_pwm = t[2]
        cpu_mode = -3
        scale_factor = 1.0
        if abs(in_button_pwm - 1700) < 50:
            cpu_mode = 1 # human control
        elif abs(in_button_pwm - 1000) < 50:
            cpu_mode = 2 # cpu control
        elif abs(in_button_pwm - 888) < 50:
            cpu_mode = 2 # cpu control
            scale_factor = 0.25

######################
        steer = 0
        try:
            img_lst = get_caffe_input_target()
            for i in range(len(img_lst)):
                solver.net.blobs['py_image_data'].data[0,i,:,:] = img_lst[i]
            solver.net.forward();
        except Exception, e:
            print(d2s(os.path.basename(sys.argv[0]),':',e))
        try:
            steer = solver.net.blobs['ip2'].data[0][0]
            steer -= 0.5
            steer *= 100
            steer = int(steer)
            print (steer,int(100*(solver.net.blobs['ip2'].data[0][1])),int(100*(solver.net.blobs['ip2'].data[0][2])))
        except Exception, e:
            print(d2s(os.path.basename(sys.argv[0]),':',e))
        if len(img_dic) > 100:
            del img_dic
            img_dic = {}
#########################






        out_steer = 49+steer #pwm_to_percent(in_steer_pwm,servo_min_cpu,servo_null,servo_max_cpu)
        out_motor = in_motor_pwm #pwm_to_percent(in_motor_pwm,motor_min_cpu,motor_null,motor_max_cpu,scale_factor)
       #print (out_steer,out_motor)
        cpu_int = encode_int_signal(cpu_mode,out_steer,out_motor)
    except Exception,e:
        print e

 