from kzpy3.utils import *
import roslib
import std_msgs.msg
import rospy

steer = 0
def steer_callback(msg):
	global steer
	steer = msg.data

motor = 0
def motor_callback(msg):
	global motor
	motor = msg.data

state = 0
def state_callback(msg):
	global state
	state = msg.data

rospy.init_node('listener',anonymous=True)

rospy.Subscriber('/bair_car/steer', std_msgs.msg.Int32, callback=steer_callback)
rospy.Subscriber('/bair_car/motor', std_msgs.msg.Int32, callback=motor_callback)
rospy.Subscriber('/bair_car/state', std_msgs.msg.Int32, callback=state_callback)

timer = Timer(6)

steer_div = 5

while not rospy.is_shutdown():

	while(timer.check() == False):
		steer_lst = []
		for i in range(105/steer_div):
			steer_lst.append(' ')
		steer_lst[int(99/2./steer_div)] = '|'
		steer_lst[max((100-steer)/steer_div,0)] = 'S'
		steer_str = ""
		for s in steer_lst:
			steer_str += s
		print(d2s(steer_str,state,motor,steer))
		time.sleep(0.2)
	rosbag_folder = most_recent_file_in_folder('/media/ubuntu/rosbags')
	bag_files = sgg(opj(rosbag_folder,'*.bag'))
	if len(bag_files) > 0:
		print bag_files[-1]
	else:
		print "No bag files saved yet."
	time.sleep(0.2)
	timer.reset()
