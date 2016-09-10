"""



"""
import rospy
import rosbag
from kzpy3.vis import *
import cv2
import cv_bridge
from cv_bridge import CvBridge, CvBridgeError
bridge = cv_bridge.CvBridge()

class Bair_Car_Recorded_Data:
    """ """
    def __init__(self, bag_folder_path, num_data_steps, target_topics, num_frames):
        self.bag_folder_path = bag_folder_path
        self.bag_files = sorted(glob.glob(opj(self.bag_folder_path,'*.bag')))
        file_path = opj(bag_folder_path,'.preprocessed','left_image_bound_to_data')
        print "loading "+file_path+'.pkl'
        self.left_image_bound_to_data = load_obj(file_path)
        self.bag_file_num = 0 # not the same as the number in the bag file name
        self.timestamp_num = 0 # refers to timestamp count within a bag file
        self.bag_img_dic = None
        self.timestamps = None
        self.data_dic = None
        self.num_data_steps = num_data_steps
        self.target_topics = target_topics
        self.num_frames = num_frames

    def get_data(self,color_mode="rgb8"):
        if self.bag_img_dic == None:
            self.bag_img_dic = load_images_from_bag(self.bag_files[self.bag_file_num],color_mode)
            self.timestamp_num = 0
            self.timestamps = sorted(self.bag_img_dic['left'].keys())
        t = self.timestamps[self.timestamp_num]
        self.data_dic = {}

        if t in self.left_image_bound_to_data:
            #print (self.left_image_bound_to_data[t]['state_one_steps'],self.left_image_bound_to_data[t]['steer'])
            if self.left_image_bound_to_data[t]['state_one_steps'] > self.num_data_steps:
                if self.timestamp_num+self.num_data_steps <= len(self.timestamps):
                    for topic in self.target_topics:
                        target_data = []
                        left_list = []
                        right_list = []
                        ctr = 0
                        for tn in range(self.timestamp_num,self.timestamp_num+self.num_data_steps):
                            data = self.left_image_bound_to_data[self.timestamps[tn]][topic]
                            target_data.append(data)
                            if ctr < self.num_frames:
                                left_list.append(self.bag_img_dic['left'][self.timestamps[tn]])
                                right_list.append(self.bag_img_dic['right'][self.left_image_bound_to_data[self.timestamps[tn]]['right_image']])
                                ctr += 1
                        self.data_dic[topic] = target_data
                    self.data_dic['left'] = left_list
                    self.data_dic['right'] = right_list

            else:
                pass

        self.timestamp_num += 1
        if self.timestamp_num >= len(self.timestamps):
            self.bag_img_dic = None
            self.bag_file_num += 1
        if self.timestamp_num >= len(self.left_image_bound_to_data.keys()):
            return 'END'
        return self.data_dic




def load_images_from_bag(bag_file_path,color_mode="rgb8"):
    print "loading " + bag_file_path
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


def save_grayscale_quarter_images(bag_folder,bag_filename):
    b = load_images_from_bag(bag_file_path,color_mode="rgb8")
    for s in ['left','right']:
        for t in b[s]:
            b[s][t] = b[s][t][:,:,1]
            b[s][t] = imresize(b[s][t],0.25)
    unix('mkdir -p '+opj(bag_folder,'.preprocessed'))
    save_obj(b,opj(bag_folder,'.preprocessed',bag_filename))

"""
bag_folder_path = '/home/karlzipser/Desktop/bair_car_data/direct_7Sept2016_Mr_Orange_Tilden'

d = Bair_Car_Recorded_Data(bag_folder_path,10,['steer','motor','encoder','acc','gyro','sonar'])

for i in range(500):
    data = d.get_data()
"""
