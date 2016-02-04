print "RPi_server.py server side"

##############
#

import sys
sys.path.insert(0, "/home/pi")
from kzpy3.utils import *
import RPi.GPIO as GPIO
"""
SERVO_IN = 38
MOTOR_IN = 40
out_pins = [SERVO_IN,MOTOR_IN]
def gpio_setup():
    print('gpio_setup')
    GPIO.setmode(GPIO.BOARD)
    for p in out_pins:
        GPIO.setup(p,GPIO.OUT)
gpio_setup() 
pwm_motor = GPIO.PWM(40,50)
pwm_servo = GPIO.PWM(38,50)
pwm_motor.start(0)
pwm_servo.start(0)
"""

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

def cleanup_and_exit():
    #GPIO.cleanup()
    serversocket.close()
    print('cleaned up.')
    time.sleep(1)
    sys.exit()


try:
    while True:
        try:
            buf = connection.recv(64)
        except:
            cleanup_and_exit()
        if len(buf) != "":
            print buf
        else:
            print("*** No Data received from socket ***")
            cleanup_and_exit()
            break

except KeyboardInterrupt:
    cleanup_and_exit()



