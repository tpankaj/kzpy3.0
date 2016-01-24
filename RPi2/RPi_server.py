print "RPi_server.py server side"


import socket

#try:
import sys
sys.path.insert(0, "/home/pi")
from kzpy3.utils import *
import RPi.GPIO as GPIO
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
#except:
#print("*** not RPi ****")



host = '0.0.0.0' # 'localhost'
port = 5000

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((host, port))
serversocket.listen(5) # become a server socket, maximum 5 connections

connection, address = serversocket.accept()
while True:
    buf = connection.recv(64)
    if len(buf) > 0:
        try:
            t = eval(buf)
        except:
            t = False
        if t:
            print(d2s('t =',t))
            pwm_servo.ChangeDutyCycle(t[0])
            pwm_motor.ChangeDutyCycle(t[1])
            time.sleep(0.01)
            pwm_motor.ChangeDutyCycle(0)
        else:
            print('['+buf+']')
        #print(d2s(t[0],t[1]))
        #break
        if buf == 'q':
            try:
                GPIO.cleanup()
            except:
                print("*** not RPi ****")
            time.sleep(0.1)
            break

serversocket.close()


