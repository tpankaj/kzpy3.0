"""
reed to run roslaunch first, e.g.,

roslaunch bair_car bair_car.launch use_zed:=true record:=false
"""

import roslib
import cv2
from cv_bridge import CvBridge,CvBridgeError
import rospy
from sensor_msgs.msg import Image
import scipy
import numpy as np

bridge = CvBridge()


rospy.init_node('listener',anonymous=True)

left_list = []
right_list = []

A = 0
B = 0

def right_callback(data):
	global A
	A += 1
	print (A,B,len(left_list),len(right_list))
	cimg = bridge.imgmsg_to_cv2(data,"bgr8")
	if len(right_list) > 5:
		right_list = right_list[-5:]
	right_list.append(cimg)
	cv2.imshow("Right",right_list[-1]-left_list[-1])#cimg)
	cv2.waitKey(1)

def left_callback(data):
	global B
	B += 1
	cimg = bridge.imgmsg_to_cv2(data,"bgr8")
	if len(left_list) > 5:
		left_list = left_list[-5:]
	left_list.append(cimg)
	#cv2.imshow("Left",cimg)
	#cv2.waitKey(1)


rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_callback)
rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_callback)

rospy.spin()
