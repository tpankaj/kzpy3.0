import RPi.GPIO as GPIO
import time
import sys
sys.path.insert(0, "/home/pi")
from kzpy3.utils import *

GPIO.setmode(GPIO.BOARD)
pin = input('Enter GPIO pin: ')
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

reed_close = 0

start_time = 0

def my_callback(channel):
	global reed_close
	if GPIO.input(pin): 
		pass #print "Rising edge detected"  
	else:
		#print "Falling edge detected" 
		reed_close += 1
		if start_time = 0:
			start_time = time.time()
		if time.time() -  start_time > 10:
			print(d2s(reed_close,'counts in',time.time() -  start_time,'seconds'))
			start_time = time.time()
			reed_close = 0

# when a changing edge is detected on port 25, regardless of whatever   
# else is happening in the program, the function my_callback will be run  
GPIO.add_event_detect(pin, GPIO.BOTH, callback=my_callback)  



def cleanup_and_exit():
    GPIO.cleanup()
    print(os.path.basename(sys.argv[0])+' : cleaned up.')
    time.sleep(1)
    sys.exit()


try:
    while True:
		print(time.time())
    		time.sleep(1)
except KeyboardInterrupt:
    cleanup_and_exit()



