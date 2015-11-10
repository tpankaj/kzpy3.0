"""

ipython --pylab osx kzpy3/scratch/keypress_view_RPi.py; reset

ssh pi@192.168.43.20
sudo python kzpy3/scratch/camera_control.py
"""

import sys
sys.path.insert(0, "/home/pi")
from kzpy3.utils import *
import RPi.GPIO as GPIO


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
            print(last_cmd)
            if str_contains(last_cmd,'up'):
                print('GO UP')
            elif str_contains(last_cmd,'down'):
                print('GO DOWN')
            elif str_contains(last_cmd,'left'):
                print('GO LEFT')
            elif str_contains(last_cmd,'right'):
                print('GO RIGHT')
            elif last_cmd[0] == 'q':
                print('Quitting now.')
                sys.exit(1)
    except KeyboardInterrupt:
        print('Quitting now.')
        sys.exit(1)
    except:
        pass
    time.sleep(0.05)
    

while True:
	update()
#########