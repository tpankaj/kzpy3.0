# This is used to specifiy caffe mode and data file name information

from kzpy3.utils import *

print "***************** car_run_params.py"

computer_name = "MR_Unknown"
try:  
   computer_name = os.environ["COMPUTER_NAME"]
except KeyError: 
   print """********** Please set the environment variable computer_name ***********
   e.g.,
   export COMPUTER_NAME="Mr_Orange"
   """


####################### general car settings ################
#
for i in range(5):
	print('*************' + computer_name + '***********')
Direct = 1.
Follow = 0.
Play = 0.
Furtive = 0.
Caf = 0.0
Racing = 0.0
Location = 'auto_start'

solver_file_path = "/home/ubuntu/kzpy3/caf5/z2_color/solver_live.prototxt"
#weights_file_path = "/home/ubuntu/kzpy3/caf5/z2_color/z2_color.caffemodel"
weights_file_path = "/home/ubuntu/kzpy3/caf6/z2_color_more/z2_color_more_2.caffemodel"
verbose = True
motor_gain = 0.5
steer_gain = 1.0

GPS2_lat_orig = 37.881404 #-999.99
GPS2_long_orig = -122.2743327 #-999.99
GPS2_radius = 0.0004
#
###################################################################

####################### specific car settings ################
#
if computer_name == 'Mr_Orange':
	pass
if computer_name == 'Mr_Silver':
	pass
if computer_name == 'Mr_Blue':
	pass
if computer_name == 'Mr_White':
	pass
if computer_name == 'Mr_Black':
	pass
if computer_name == 'Mr_Teal':
	pass
if computer_name == 'Mr_Audi':
	pass
if computer_name == 'Mr_Purple':
	pass
if computer_name == 'Mr_LightBlue':
	pass
if computer_name == 'Mr_Yellow':
	pass
#
###################################################################


if Direct == 1:
	task = 'direct'
elif Play == 1:
	task = 'play'
elif Follow == 1:
	task = 'follow'
elif Furtive == 1:
	task = 'furtive'
elif Racing == 1:
	task = 'racing'
else:
	assert(False)


foldername = ''
if Follow == 1:
	foldername = 'follow_'

model_name = solver_file_path.split('/')[-2]

if Caf == 1:
	foldername = foldername + model_name

foldername = foldername + task + '_'

foldername = foldername + Location + '_'

foldername = foldername + time_str() + '_'

foldername = foldername + computer_name






