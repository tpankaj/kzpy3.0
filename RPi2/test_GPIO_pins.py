import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

def test_pin(p):	
	GPIO.setup(p,GPIO.OUT)
	for i in range(10):
		GPIO.output(GPIO_TRIGGER, True)
		time.sleep(1/6.0)		
		GPIO.output(GPIO_TRIGGER, False)
		time.sleep(1/2.0)
