"""

ipython --pylab osx kzpy3/scratch/keypress_view_RPi.py; reset

ssh pi@192.168.43.20

"""

from kzpy3.utils import *

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
            if last_cmd[0] == 'q':
                print('Quitting now.')
                sys.exit(1)
    except KeyboardInterrupt:
        print('Quitting now.')
        sys.exit(1)
    except:
        pass
    time.sleep(0.1)
    

while True:
	update()
