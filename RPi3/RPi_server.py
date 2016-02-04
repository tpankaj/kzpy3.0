print "RPi_server.py server side"

##############
#

import sys
sys.path.insert(0, "/home/pi")
from kzpy3.utils import *
import RPi.GPIO as GPIO

STEER_PIN = 35
MOTOR_PIN = 37
NEUTRAL = 7.0
GPIO_TRIGGER = 29
GPIO_ECHO = 23

out_pins = [STEER_PIN,MOTOR_PIN]
def gpio_setup():
    print('gpio_setup')
    GPIO.setmode(GPIO.BOARD)
    for p in out_pins:
        GPIO.setup(p,GPIO.OUT)
gpio_setup() 
pwm_motor = GPIO.PWM(MOTOR_PIN,50)
pwm_steer = GPIO.PWM(STEER_PIN,50)
pwm_motor.start(NEUTRAL)
pwm_steer.start(0)

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
TIMEOUT_DURATION = 10.0
connection, address = serversocket.accept()
connection.settimeout(TIMEOUT_DURATION)
#
##############

# http://stackoverflow.com/questions/17386487/python-detect-when-a-socket-disconnects-for-any-reason
# http://stackoverflow.com/questions/667640/how-to-tell-if-a-connection-is-dead-in-python


def ultrasonic_range_measure():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()
    while GPIO.input(GPIO_ECHO)==0:
      start = time.time()
    while GPIO.input(GPIO_ECHO)==1:
      stop = time.time()
    elapsed = stop-start
    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34000
    # That was the distance there and back so halve the value
    distance = distance / 2
    return distance




def cleanup_and_exit():
    GPIO.cleanup()
    serversocket.close()
    print('cleaned up.')
    time.sleep(1)
    sys.exit()

def update_driving(buf):
    b = buf.split(' ')
    steer = int(b[0])/100.0
    speed = int(b[1])/100.0
    #print(steer,speed)
    servo_ds = 9.2 + 2.0*steer
    motor_ds = 7.0 + 0.5*speed
    pwm_steer.ChangeDutyCycle(servo_ds)
    pwm_motor.ChangeDutyCycle(motor_ds)

try:
    while True:
        try:
            buf = connection.recv(64)
        except:
            cleanup_and_exit()
        if len(buf) != "":
            update_driving(buf)
        else:
            print("*** No Data received from socket ***")
            cleanup_and_exit()
            break
except KeyboardInterrupt:
    cleanup_and_exit()



