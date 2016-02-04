#!/usr/bin/python
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|-|S|p|y|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# ultrasonic_1.py
# Measure distance using an ultrasonic module
#
# Author : Matt Hawkins
# Date   : 09/01/2013

# Import required Python libraries
import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BOARD)

# Define GPIO to use on Pi
GPIO_TRIGGER = 29
GPIO_ECHO = 23
GPIO_LED = 31

print "Ultrasonic Measurement"

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo
GPIO.setup(GPIO_LED,GPIO.OUT)      # Echo
pwm_LED = GPIO.PWM(GPIO_LED,3)
pwm_LED.start(0.1)


# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)

# Allow module to settle
time.sleep(0.5)
for i in range(100):
	# Send 10us pulse to trigger
	GPIO.output(GPIO_TRIGGER, True)
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)
	start = time.time()
	while GPIO.input(GPIO_ECHO)==0:
	  start = time.time()

	while GPIO.input(GPIO_ECHO)==1:
	  stop = time.time()

	# Calculate pulse length
	elapsed = stop-start

	# Distance pulse travelled in that time is time
	# multiplied by the speed of sound (cm/s)
	distance = elapsed * 34000

	# That was the distance there and back so halve the value
	distance = distance / 2
	pwm_LED.ChangeFrequency(1/distance * 100.0)
	print "Distance : %.1f cm" % distance
	time.sleep(0.1)

# Reset GPIO settings
GPIO.cleanup()