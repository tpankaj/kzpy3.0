import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(7)
    if input_state == False:
        print('Button Pressed')
        GPIO.cleanup()
        break
    time.sleep(0.3)
    print(time.time())
