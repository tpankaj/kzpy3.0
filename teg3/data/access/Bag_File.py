from kzpy3.utils import *
import rospy
import rosbag
import cv2
import cv_bridge
from cv_bridge import CvBridge, CvBridgeError
bridge = cv_bridge.CvBridge()

def load_images(bag_file_path,color_mode="rgb8",include_flip=True):
    print "Bag_File.load_images:: loading " + bag_file_path
    bag_img_dic = {}
    sides=['left','right']
    for s in sides:
        bag_img_dic[s] = {}
        if include_flip:
            bag_img_dic[s+'_flip'] = {}
    bag = rosbag.Bag(bag_file_path)
    for side in sides:
        for m in bag.read_messages(topics=['/bair_car/zed/'+side+'/image_rect_color']):
            t = round(m.timestamp.to_time(),3)
            img = bridge.imgmsg_to_cv2(m[1],color_mode)
            bag_img_dic[side][t] = img
            if include_flip:
                bag_img_dic[side+'_flip'][t] = scipy.fliplr(img)
    return bag_img_dic

