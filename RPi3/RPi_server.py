import sys
sys.path.insert(0, "/home/pi")
from kzpy3.utils import *
print os.path.basename(sys.argv[0])

import RPi.GPIO as GPIO

STEER_PIN = 35
MOTOR_PIN = 37
EYE_PIN = 31
NEUTRAL = 7.0
GPIO_TRIGGER_RIGHT = 13
GPIO_ECHO_RIGHT = 15
GPIO_TRIGGER_LEFT = 19
GPIO_ECHO_LEFT = 21
GPIO_REED = 23

out_pins = [STEER_PIN,MOTOR_PIN,EYE_PIN]
def gpio_setup():
    print('gpio_setup')
    GPIO.setmode(GPIO.BOARD)
    for p in out_pins:
        GPIO.setup(p,GPIO.OUT)

gpio_setup() 
pwm_motor = GPIO.PWM(MOTOR_PIN,50)
pwm_steer = GPIO.PWM(STEER_PIN,50)
pwm_eye = GPIO.PWM(EYE_PIN,50)
pwm_motor.start(NEUTRAL)
pwm_steer.start(0)
pwm_eye.start(0)

GPIO.setup(GPIO_TRIGGER_RIGHT,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO_RIGHT,GPIO.IN)      # Echo
GPIO.setup(GPIO_TRIGGER_LEFT,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO_LEFT,GPIO.IN)      # Echo

GPIO.setup(GPIO_REED, GPIO.IN, pull_up_down=GPIO.PUD_UP)

reed_close = 0
rps = 0

def my_callback(channel):
    global reed_close
    if GPIO.input(GPIO_REED): 
        pass #print "Rising edge detected"  
    else:
        #print "Falling edge detected" 
        reed_close += 1

GPIO.add_event_detect(GPIO_REED, GPIO.BOTH, callback=my_callback)
#
##############



##############
#
import socket
#import select
host = '0.0.0.0'
port = 5000
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((host, port))
serversocket.listen(5) # become a server socket, maximum 5 connections
TIMEOUT_DURATION = 1.0
connection, address = serversocket.accept()
connection.settimeout(TIMEOUT_DURATION)
#
##############

# http://stackoverflow.com/questions/17386487/python-detect-when-a-socket-disconnects-for-any-reason
# http://stackoverflow.com/questions/667640/how-to-tell-if-a-connection-is-dead-in-python


def ultrasonic_range_measure(GPIO_trigger,GPIO_echo):
    #print('ultrasonic_range_measure...')
    GPIO.output(GPIO_trigger, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_trigger, False)
    start = time.time()
    while GPIO.input(GPIO_echo)==0:
      start = time.time()
    while GPIO.input(GPIO_echo)==1:
        stop = time.time()
        if time.time()-start > 0.1:
            break
    elapsed = stop-start
    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34000
    # That was the distance there and back so halve the value
    distance = distance / 2.0
    return int(distance)




def cleanup_and_exit():
    GPIO.cleanup()
    serversocket.close()
    print(os.path.basename(sys.argv[0])+' : cleaned up.')
    time.sleep(1)
    sys.exit()

last_saccade = time.time()
last_eye_pos = 7.8

speed = 0
cruise_control = False
cruise_control_on_t = 0
cruise_speed = 0
cruise_rps = 0

def update_driving(buf):
    global last_saccade
    global last_eye_pos
    global speed
    global cruise_control
    global cruise_control_on_t
    global cruise_speed
    global cruise_rps
    b = buf.split(' ')
    steer = int(b[0])/100.0
    """
    if rps < 1.0:
        speed += 0.003
    elif rps > 1.5:
        speed -= 0.003
    if speed > 1.:
        speed = 1.
    elif speed < 0.:
        speed = 0.
    """
    speed = int(b[1])/100.0
    cruise = int(b[2])
    if cruise:
        print "cruise on!!!!"
        cruise_control = True
        cruise_control_on_t = time.time()
        cruise_rps = rps
        cruise_speed = speed
    if cruise_control:
        if time.time() - cruise_control_on_t > 1:
            if speed > 0.5:
                cruise_control = False
                cruise_control_on_t = 0
                print "CRUISE OFF!!!!!!!"
    if cruise_control:
        if rps > 1.1 * cruise_rps:
            cruise_speed -= 0.003
        elif rps < 0.9 * cruise_rps:
            cruise_speed += 0.003
        else:
            pass
        speed = cruise_speed

    print(steer,speed,cruise)
    servo_ds = 9.43 + 2.0*steer
    eye_ds = 7.8 + 2.0*steer
    motor_ds = 7.0 + 0.75*speed
    pwm_steer.ChangeDutyCycle(servo_ds)
    if time.time()-last_saccade > 0.2:
        if np.abs(last_eye_pos-eye_ds) > 0.2:
            pwm_eye.ChangeDutyCycle(eye_ds)
            last_saccade = time.time()
            last_eye_pos = eye_ds
        else:
            pwm_eye.ChangeDutyCycle(0)
    pwm_motor.ChangeDutyCycle(motor_ds)


reed_close_lst = []
start_t = time.time()
try:
    while True:
        try:
            buf = connection.recv(64)
        except:
            cleanup_and_exit()
        if len(buf) != "":
            if time.time() - start_t >= 1.0:
                d_time = time.time() - start_t
                start_t = time.time()
                rps = reed_close / d_time
                reed_close = 0
            update_driving(buf)
            left_range = ultrasonic_range_measure(GPIO_TRIGGER_LEFT,GPIO_ECHO_LEFT)
            right_range = ultrasonic_range_measure(GPIO_TRIGGER_RIGHT,GPIO_ECHO_RIGHT)
            print(d2s('range,rps =',(left_range,right_range,rps)))
        else:
            print("*** No Data received from socket ***")
            cleanup_and_exit()
            break
except KeyboardInterrupt:
    cleanup_and_exit()

"""
        reed_close = 0
        start_t = time.time()

        time.sleep(1)

        d_time = time.time() - start_t
        if len(reed_close_lst) < 2:
            reed_close_lst.append((reed_close,d_time))
        else:
            advance(reed_close_lst,(reed_close,d_time))
        cnt = 0
        dt = 0
        for r in reed_close_lst:
            cnt += r[0]
            dt += r[1]
        print cnt / dt
"""


