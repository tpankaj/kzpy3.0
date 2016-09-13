"""



"""
from kzpy3.vis import *
import rospy
import rosbag
import cv2
import cv_bridge
bridge = cv_bridge.CvBridge()

class Bag_Folder:
    def __init__(self, path, max_requests, max_subrequests):
        self.files = sorted(glob.glob(opj(self.path,'.preprocessed','*.bag.pkl')))
        file_path = opj(path,'.preprocessed','left_image_bound_to_data')
        print "loading "+file_path+'.pkl'
        self.left_image_bound_to_data = load_obj(file_path)
        self.bag_file = None
        self.requests = 0
        self.max_requests = max_requests

    def get_data(self, num_data_steps, target_topics, num_frames):
        if self.requests >= self.max_requests:
            return None
        if self.bag_file == None:
            self.bag_file = Bag_File(random.choice(self.files), left_image_bound_to_data, max_subrequests)
        data = self.bag_file.get_data(num_data_steps, target_topics, num_frames)
        if data == None:
            self.bag_file == None
                return self.get_data(num_data_steps, target_topics, num_frames)
        self.requests += 1
        return data

class Bag_File:
#                if self.left_image_bound_to_data[t]['state_one_steps'] > self.num_data_steps:
    def __init__(self, path, left_image_bound_to_data, max_requests): #, ):
        self.path = path
        self.img_dic = None
        self.timestamps = None
        self.data_dic = None
        self.left_image_bound_to_data = left_image_bound_to_data
        self.max_requests = 0

    def get_data(self, num_data_steps, target_topics, num_frames):
            if self.ctr > self.max_requests:
                return None
            if self.img_dic == None:
                self.img_dic = load_obj(path.replace('.pkl',''))
                self.timestamps = sorted(self.img_dic['left'].keys())
            timestamp_num = np.random.randint(len(self.timestamps))
            t = self.timestamps[timestamp_num]
            self.data_dic = {}

            if t in self.left_image_bound_to_data:
                if self.left_image_bound_to_data[t]['state_one_steps'] > self.num_data_steps:
                    if self.timestamp_num+self.num_data_steps <= len(self.timestamps):
                        for topic in self.target_topics:
                            target_data = []
                            left_list = []
                            right_list = []
                            fctr = 0
                            for tn in range(self.timestamp_num,self.timestamp_num+self.num_data_steps):
                                data = self.left_image_bound_to_data[self.timestamps[tn]][topic]
                                target_data.append(data)
                                if fctr < self.num_frames:
                                    left_list.append(self.bag_img_dic['left'][self.timestamps[tn]])
                                    right_list.append(self.bag_img_dic['right'][self.left_image_bound_to_data[self.timestamps[tn]]['right_image']])
                                    fctr += 1
                            self.data_dic[topic] = target_data
                        self.data_dic['left'] = left_list
                        self.data_dic['right'] = right_list
            else:
                pass

            self.ctr += 1

            return self.data_dic




class Bair_Car_Recorded_Data:
    """ """
    def __init__(self, bag_folder_path, num_data_steps, target_topics, num_frames):
        self.bag_folder = Bag_Folder(bag_folder_path)

        self.num_data_steps = num_data_steps
        self.target_topics = target_topics
        self.num_frames = num_frames
        """
        self.binned_timestamps = [[],[],[],[],[]]
        for t in self.left_image_bound_to_data:
            if self.left_image_bound_to_data[t]['state_one_steps'] > self.num_data_steps:
                self.good_timestamps.append(t)
                steer = self.left_image_bound_to_data[t]['steer']
                if steer < 0.35:
                    self.binned_timestamps[0].append(t)
                elif steer < 0.45:
                    self.binned_timestamps[1].append(t)
                elif steer < 0.55:
                    self.binned_timestamps[2].append(t)
                elif steer < 0.65:
                    self.binned_timestamps[3].append(t)
                else:
                    self.binned_timestamps[4].append(t)
        """
        self.ctr = 0

    def get_data(self):
        bag_file_num = np.random.randint(len(self.bag_files))
        if self.bag_img_dic == None:
            
            fp = self.bag_files[bag_file_num]
            print "loading " + fp
            self.bag_img_dic = load_obj(fp.replace('.pkl',''))
            self.timestamps = sorted(self.bag_img_dic['left'].keys())
        
        self.timestamp_num = np.random.randint(len(self.timestamps))
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
                        fctr = 0
                        for tn in range(self.timestamp_num,self.timestamp_num+self.num_data_steps):
                            data = self.left_image_bound_to_data[self.timestamps[tn]][topic]
                            target_data.append(data)
                            if fctr < self.num_frames:
                                left_list.append(self.bag_img_dic['left'][self.timestamps[tn]])
                                right_list.append(self.bag_img_dic['right'][self.left_image_bound_to_data[self.timestamps[tn]]['right_image']])
                                fctr += 1
                        self.data_dic[topic] = target_data
                    self.data_dic['left'] = left_list
                    self.data_dic['right'] = right_list

            else:
                pass


        self.ctr += 1
        if self.ctr > 100:
            self.ctr = 0
            self.bag_img_dic = None
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
    b = load_images_from_bag(opj(bag_folder,bag_filename),color_mode="rgb8")
    for s in ['left','right']:
        for t in b[s]:
            b[s][t] = b[s][t][:,:,1]
            b[s][t] = imresize(b[s][t],0.25)
    unix('mkdir -p '+opj(bag_folder,'.preprocessed'))
    save_obj(b,opj(bag_folder,'.preprocessed',bag_filename))

def save_grayscale_quarter_bagfolder(bag_folder_path):
    bag_files = sorted(glob.glob(opj(bag_folder_path,'*.bag')))
    for b in bag_files:
        b = b.split('/')[-1]
        save_grayscale_quarter_images(bag_folder_path,b)

"""
bag_folder_path = '/home/karlzipser/Desktop/bair_car_data/direct_7Sept2016_Mr_Orange_Tilden'

d = Bair_Car_Recorded_Data(bag_folder_path,10,['steer','motor','encoder','acc','gyro','sonar'])

for i in range(500):
    data = d.get_data()
"""
