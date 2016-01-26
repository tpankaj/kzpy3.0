print "RPi_server_temp.py server side"

##############
#
ON_RPi = True
if ON_RPi:
    print("*** on RPi ****")
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
else:
    print("*** not RPi ****")
    from kzpy3.utils import *
#
##############

start_t = time.time()

while time.time() - start_t < 30:
    pwm_servo.ChangeDutyCycle(9)
    time.sleep(0.3)
    pwm_servo.ChangeDutyCycle(8)
    time.sleep(0.3)

GPIO.cleanup()
print('cleaned up.')

