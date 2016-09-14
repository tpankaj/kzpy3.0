"""
reed to run roslaunch first, e.g.,

roslaunch bair_car bair_car.launch use_zed:=true record:=false
"""

########################################################
#          CAFFE SETUP SECTION
import caffe
from kzpy3.utils import *
from kzpy3.teg1.rosbag_work.get_data_from_bag_files2 import *
import cv2
os.chdir(home_path) # this is for the sake of the train_val.prototxt

solver_file_path = opjh("kzpy3/caf3/z1/solver_live.prototxt")
weights_file_path = None #opjD('z1/z1_iter_510000.caffemodel') #
def setup_solver():
	solver = caffe.SGDSolver(solver_file_path)
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	return solver
solver = setup_solver()
if weights_file_path != None:
	print "loading " + weights_file_path
	solver.net.copy_from(weights_file_path)
#
########################################################


########################################################
#          ROSPY SETUP SECTION
import roslib
import cv2
from cv_bridge import CvBridge,CvBridgeError
import rospy
from sensor_msgs.msg import Image
bridge = CvBridge()
rospy.init_node('listener',anonymous=True)

left_list = []
right_list = []
A = 0
B = 0

def right_callback(data):
	global A,B, left_list, right_list, solver
	A += 1
	print (A,B,len(left_list),len(right_list))
	cimg = bridge.imgmsg_to_cv2(data,"bgr8")
	if len(right_list) > 5:
		right_list = right_list[-5:]
	right_list.append(cimg)
	cv2.imshow("Right",cimg)
	cv2.waitKey(1)

def left_callback(data):
	global A,B, left_list, right_list
	B += 1
	cimg = bridge.imgmsg_to_cv2(data,"bgr8")
	if len(left_list) > 5:
		left_list = left_list[-5:]
	left_list.append(cimg)
	#cv2.imshow("Left",cimg)
	#cv2.waitKey(1)
#
########################################################


rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_callback)
rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_callback)

while True:
	if len(left_list) > 4:
		l0 = left_list[-2]
		l1 = left_list[-1]
		r0 = right_list[-2]
		r1 = right_list[-1]

		solver.net.blobs['ZED_data'].data[0,0,:,:] = l0[:,:,1]#/255.0-.5
		solver.net.blobs['ZED_data'].data[0,1,:,:] = l1[:,:,1]#/255.0-.5
		solver.net.blobs['ZED_data'].data[0,2,:,:] = r0[:,:,1]#/255.0-.5
		solver.net.blobs['ZED_data'].data[0,3,:,:] = r1[:,:,1]#/255.0-.5

		#solver.step(1)




#rospy.spin()
