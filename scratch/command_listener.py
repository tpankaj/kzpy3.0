"""

ipython --pylab osx kzpy3/scratch/keypress_view_RPi.py; reset

ssh pi@192.168.43.20
sudo python kzpy3/scratch/camera_control.py
sudo python kzpy3/scratch/command_listener.py
"""

import sys
sys.path.insert(0, "/home/pi")
from kzpy3.utils import *
import RPi.GPIO as GPIO


SERVO_IN = 38
MOTOR_IN = 40
#HB_EN1 = 7
#HB_IN1 = 12
#HB_IN2 = 13

out_pins = [SERVO_IN,MOTOR_IN]#[SERVO_IN, HB_EN1, HB_IN1, HB_IN2]

GPIO.setmode(GPIO.BOARD)
for p in out_pins:
    GPIO.setup(p,GPIO.OUT)

def do_pwm(pin,frequency,duration,duty_cycle):
    pwm = GPIO.PWM(pin,frequency)
    start_time = time.time()
    pwm.start(duty_cycle)
    while time.time() < start_time + duration:
        pass;
    pwm.stop()

def servo(
    duty_cycle=7.5,
    durataion=0.2,
    freqency=50,
    pin=SERVO_IN):
    """
    """
    do_pwm(pin,frequency,duration,duty_cycle)




def onKeyPress(event):
    text.insert('end', '%s ' % (event.char, ))
    if event.char == '1':
        do_pwm(38,50,0.3,7.8)
    if event.char == '2':
        do_pwm(38,50,0.3,9.5)
    if event.char == '3':
        do_pwm(38,50,0.3,11)
    if event.char == '4':
        do_pwm(40,50,0.3,7.20)
    if event.char == '5':
        do_pwm(40,50,0.3,7.18)
    if event.char == 'q':
        GPIO.cleanup()
        root.destroy() #root.quit()




###############
last_cmd ='no command yet'

#command_file_path = '/Users/karlzipser/Desktop/distal_command.txt'
command_file_path = '/home/pi/Desktop/distal_command.txt'

def update():
    global last_cmd

    try:
        cmd_lst = txt_file_to_list_of_strings(command_file_path)    
        if cmd_lst[0] != last_cmd:
            last_cmd = cmd_lst[0]
            #print(last_cmd)
            if last_cmd[0] == ' ':
                print('motor')
                do_pwm(40,50,0.3,7.20)
                
            elif str_contains(last_cmd,'up'):
                print('straight')
                do_pwm(38,50,0.3,9.5)
                
            elif str_contains(last_cmd,'left'):
                print('left')
                do_pwm(38,50,0.3,7.8)
                
            elif str_contains(last_cmd,'right'):
                print('right')
                do_pwm(38,50,0.3,11)
                
            elif last_cmd[0] == 'q':
                list_of_strings_to_txt_file(command_file_path,['done.'])
                print('Quitting now. Press ctrl-C if this does not exit.')
                GPIO.cleanup()
                sys.exit()
    except KeyboardInterrupt:
        print('Quitting now.')
        GPIO.cleanup()
        sys.exit(1)
    except:
        pass
    time.sleep(0.05)
    

while True:
	update()
#########