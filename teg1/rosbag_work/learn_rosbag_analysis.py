"""
Take rosbag files and have the option of doing any of the following:
1) look at timestamp intervals
2) look at difference in timestamps of left and right camera
3) plot data versus timestamps
4) save images to jpegs at reduced resolution
5) bind data to left_image timestamps, so that one stream of timestamps is
   bound to all data types
"""

from kzpy3.vis import *
import rospy
import rosbag
import sensor_msgs.msg
import cv_bridge
from cv_bridge import CvBridge, CvBridgeError

############## bagfile data to dictionary A ##############################
#
A = {}

image_topics = ['left_image','right_image']
single_value_topics = ['steer','state','motor','encoder','sonar']
vector3_topics = ['gyro'] # leave out gps for now.
all_topics = image_topics + single_value_topics + vector3_topics
for topic in all_topics:
    A[topic] = {}


bridge = cv_bridge.CvBridge()

bag_files = sorted(glob.glob('/home/karlzipser/Desktop/rosbag_2Aug/*.bag'))

# bag_files = bag_files[13:15] # TEMP!


for b in bag_files: # we don't assume we are geting them in chronological order
    
    print b

    bag = rosbag.Bag(b)

    for topic in single_value_topics:
        for m in bag.read_messages(topics=['/bair_car/'+topic]):
            t = round(m.timestamp.to_time(),3)
            A[topic][t] = m[1].data

    for topic in vector3_topics:
        for m in bag.read_messages(topics=['/bair_car/'+topic]):
            t = round(m.timestamp.to_time(),3)
            A[topic][t] = (m[1].x,m[1].y,m[1].z)

    for m in bag.read_messages(topics=['/bair_car/zed/left/image_rect_color']):
        t = round(m.timestamp.to_time(),3)
        A['left_image'][t] = 'z' #imresize(bridge.imgmsg_to_cv2(m[1],"rgb8"),0.25)

    for m in bag.read_messages(topics=['/bair_car/zed/right/image_rect_color']):
        t = round(m.timestamp.to_time(),3)
        A['right_image'][t] = 'z' #imresize(bridge.imgmsg_to_cv2(m[1],"rgb8"),0.25)




for img in ['left_image','right_image']:
    ctr = 0
    sorted_timestamps = sorted(A[img].keys())
    for t in sorted_timestamps:
        A[img][t] = ctr
        ctr += 1

#
######################################################################

######################### binding data to left_image timestamps ######
#
def interpolate_single_values(A,topic):
    interp_dic = {}
    k,d = get_sorted_keys_and_data(A[topic])
    for i in range(0,len(k)-1):
        for j in range(int(k[i]*1000),int(k[i+1]*1000)):
            v =  (d[i+1]-d[i])/(k[i+1]-k[i]) * (j/1000.-k[i])  + d[i]
            interp_dic[j/1000.] = v
    return interp_dic

def interpolate_vector_values(A,topic):
    interp_dic = {}
    k,d = get_sorted_keys_and_data(A[topic])
    d = np.array(d)
    dim = len(d[0])
    for i in range(0,len(k)-1):
        for j in range(int(k[i]*1000),int(k[i+1]*1000)):
            v = []
            for u in range(dim):
                v.append(  (d[i+1,u]-d[i,u])/(k[i+1]-k[i]) * (j/1000.-k[i])  + d[i,u] )
            interp_dic[j/1000.] = v
    return interp_dic

def assign_right_image_timestamps(A):
    interp_dic = {}
    k,d = get_sorted_keys_and_data(A['right_image'])
    for i in range(0,len(k)-1):
        a = int(k[i]*1000)
        b = int(k[i+1]*1000)
        c = (a+b)/2
        for j in range(a,b):
            if j < c:
                v = k[i]
            else:
                v = k[i+1]
            interp_dic[j/1000.] = v
    return interp_dic

def bind_left_image_timestamps_to_data(A):

    ms_timestamps = {}

    ms_timestamps['right_image'] = assign_right_image_timestamps(A)

    for topic in single_value_topics:
        ms_timestamps[topic] = interpolate_single_values(A,topic)

    for topic in vector3_topics:
        ms_timestamps[topic] = interpolate_vector_values(A,topic)

    left_image_bound_to_data = {}

    error_log = []

    for k in A['left_image'].keys():
        left_image_bound_to_data[k] = {}
        for l in ms_timestamps.keys():
            try:
                left_image_bound_to_data[k][l] = ms_timestamps[l][k]
            except:
                error_log.append(d2s(k,l))
    print error_log
    return left_image_bound_to_data,error_log

#
######################################################################


######################### diagnostic ####################
#
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
        if np.abs(d[i]) < ignore_threshold:
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
#
######################################################################



