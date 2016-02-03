import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

def test_pin(p):	
	GPIO.setup(p,GPIO.OUT)
	for i in range(5):
		GPIO.output(p, True)
		time.sleep(1/40.0)		
		GPIO.output(p, False)
		time.sleep(1/2.0)
