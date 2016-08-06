from kzpy3.vis import *

import rospy
import rosbag
import sensor_msgs.msg
import cv_bridge
from cv_bridge import CvBridge, CvBridgeError

A = {}

image_topics = ['left_image','right_image']
single_value_topics = ['steer','state','motor','encoder','sonar']
vector_topics = ['gps','gyro']
all_topics = image_topics + single_value_topics # + vector_topics
for topic in all_topics:
    A[topic] = {}


bridge = cv_bridge.CvBridge()

bag_files = sorted(glob.glob('/home/karlzipser/Desktop/rosbag_2Aug/*.bag'))
#bag_files = ['/home/karlzipser/Desktop/rosbag_2Aug/bair_car_2016-08-02-18-23-29_74.bag',
#            '/home/karlzipser/Desktop/rosbag_2Aug/bair_car_2016-08-02-18-23-58_75.bag']

for b in bag_files:
    print b
    bag = rosbag.Bag(b)

    for topic in single_value_topics:
        for m in bag.read_messages(topics=['/bair_car/'+topic]):
            A[topic][m.timestamp.to_time()] = m[1].data

    #for m in bag.read_messages(topics=['/bair_car/state']):
    #    A['state'][m[2].to_time()] = m[1].data



    for m in bag.read_messages(topics=['/bair_car/zed/left/image_rect_color']):
        A['left_image'][m.timestamp.to_time()] = 1#imresize(bridge.imgmsg_to_cv2(m[1],"rgb8"),0.25)

    for m in bag.read_messages(topics=['/bair_car/zed/right/image_rect_color']):
        A['right_image'][m.timestamp.to_time()] = 1#imresize(bridge.imgmsg_to_cv2(m[1],"rgb8"),0.25)


def get_sorted_keys_and_data(dict):
    skeys = sorted(dict.keys())
    sdata = []
    for k in skeys:
        sdata.append(dict[k])
    return skeys,sdata

def get_timestamp_intervals(timestamps,ignore_threshold):
    d = []
    for i in range(0,len(timestamps)-1):
        interval = timestamps[i+1] - timestamps[i]
        if interval < ignore_threshold:
            d.append(interval)
        else:
            print d2s("!!!WARNING, inverval =",interval,"s. Ignoring this interval!!! ( timestamp =",timestamps[i],")")
    return d

def hist_topics_timestamp_intervals(A,topics,ignore_threshold=0.1):
    for s in topics:
        k,d = get_sorted_keys_and_data(A[s])
        i = get_timestamp_intervals(k,ignore_threshold)
        plt.figure(s)
        hist(i,bins=100)
        plt.title(d2s(s,"intervals"))
        plt.xlabel("seconds")

def hist_diff_left_right_image_timestamps(A,ignore_threshold=0.1):
    l,_ = get_sorted_keys_and_data(A['left_image'])
    r,_ = get_sorted_keys_and_data(A['right_image'])
    d = np.array(l) - np.array(r)
    dd = []
    for i in range(len(d)):
        if d[i] < ignore_threshold:
            dd.append(d[i])
        else:
            print d2s("!!!WARNING, inverval =",d[i],"s. Ignoring this interval!!!")
    plt.figure('hist_diff_left_right_image_timestamps')
    hist(dd,bins=100)
    plt.title("hist_diff_left_right_image_timestamps")
    plt.xlabel("seconds")

def make_timestamp_diagnostic_histograms(A):
    pass

def plot_topics(A):
    """
    pylab.plot(x, y1, '-b', label='sine')
    pylab.plot(x, y2, '-r', label='cosine')
    pylab.legend(loc='upper left')
    pylab.ylim(-1.5, 2.0)
    pylab.show()
    """
    pass


