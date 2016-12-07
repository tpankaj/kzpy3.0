from kzpy3.utils import *
import rospy
import rosbag
import cv2
import cv_bridge
from cv_bridge import CvBridge, CvBridgeError
bridge = cv_bridge.CvBridge()

def load_images(bag_file_path,color_mode="rgb8"):
    print "Bag_File.load_images:: loading " + bag_file_path
    bag_img_dic = {}
    bag_img_dic['left'] = {}
    bag_img_dic['right'] = {}
    sides=['left','right']
    bag = rosbag.Bag(bag_file_path)
    for side in sides:
        for m in bag.read_messages(topics=['/bair_car/zed/'+side+'/image_rect_color']):
            t = round(m.timestamp.to_time(),3)
            bag_img_dic[side][t] = bridge.imgmsg_to_cv2(m[1],color_mode)
    return bag_img_dic

