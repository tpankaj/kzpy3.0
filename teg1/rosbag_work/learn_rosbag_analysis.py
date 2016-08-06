from kzpy3.vis import *

import rospy
import rosbag
import sensor_msgs.msg
import cv_bridge
from cv_bridge import CvBridge, CvBridgeError



b = '/home/karlzipser/Desktop/rosbag_2Aug/bair_car_2016-08-02-18-23-29_74.bag'
bag = rosbag.Bag(b)

A = {}
A['steer'] = {}

for m in bag.read_messages(topics=['/bair_car/state']):
    print m

for m in bag.read_messages(topics=['/bair_car/steer']):
    n=m[1].data;print (n,type(n))


for m in bag.read_messages(topics=['/bair_car/steer']):
    n=m[1].data;print (n,type(n))


for m in bag.read_messages(topics=['/bair_car/steer']):
    A['steer'][m[2].to_time()] = m[1].data
    print (m[0],m[1].data,m[2].to_time())



dt = []
t0 = -1
for m in bag.read_messages(topics=['/bair_car/zed/left/image_rect_color']):
        t = m.timestamp.to_nsec()
        if t0 > 0:
                d = t-t0
                if d < 15936582564:     
                        dt.append(d)
        t0 = t
hist(dt,bins=100);


bridge = cv_bridge.CvBridge()
a = bridge.imgmsg_to_cv2(m[1],"rgb8")
mi(a,2,img_title=d2s(m[0],m[2].to_time()))


