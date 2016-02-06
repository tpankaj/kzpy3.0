import RPi.GPIO as GPIO
import time
import sys
sys.path.insert(0, "/home/pi")
from kzpy3.utils import *

GPIO.setmode(GPIO.BOARD)
pin = input('Enter GPIO pin: ')
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#
def my_callback(channel):  
    if GPIO.input(pin):     # if port 25 == 1  
        print "Rising edge detected"  
    else:                  # if port 25 != 1  
        print "Falling edge detected"  
  
# when a changing edge is detected on port 25, regardless of whatever   
# else is happening in the program, the function my_callback will be run  
GPIO.add_event_detect(pin, GPIO.BOTH, callback=my_callback)  

while True:
    input_state = GPIO.input(pin)
    if input_state == False:
    	time.sleep(3)
        print('Button Pressed')
        GPIO.cleanup()
        #unix('sudo shutdown -h -P 0')
        break
    time.sleep(0.1)
    print(time.time())
