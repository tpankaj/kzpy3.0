if False:

	from kzpy3.teg2.data.access.get_data_from_bag_files6 import * 
	#B=Bag_Folder('/media/karlzipser/ExtraDrive1/bair_car_data_min_disks/bair_car_data_6_min/caffe_z2_direct_local_sidewalks_28Sep16_08h06m57s_Mr_Orange'  )
	B=Bag_Folder('/media/karlzipser/ExtraDrive1/bair_car_data_min_disks/bair_car_data_4_min/caffe_z2_direct_local_Tilden_22Sep16_14h31m11s_Mr_Orange')
	data = 'timecourse data'
	plt.figure(data);plt.clf()
	ts = B.data['timestamps']
	plt.figure(data);
	topics = sorted(B.data.keys())

	ctr = 6.0
	legend_handles = []
	for tp in topics:
		if tp != 'timestamps':
			legend_handles.append(z2o_plot(ts,B.data[tp],ctr,'.',tp)[0])
			ctr -= 0.5
	plt.legend(handles=legend_handles)

	plt.figure('scatter')
	b=B.data['state_one_steps']
	plt.plot(B.data['steer'][b>0],B.data['gyro_x'][b>0],'.')





	from kzpy3.teg2.data.access.get_data_from_bag_files6 import *
	BCD = Bair_Car_Data(opjD('bair_car_data_min'),['caffe','play','follow','Tilden','Aug','Sep'])

	for i in range(7):
		t0 = time.time()
		print d2s("*************** i =",i,"*************************")
		BCD.load_bag_folder_images(250./(30./1000.))
		print d2s("time =",time.time()-t0)

	 

	N=30
	while True:
		bf=an_element(BCD.bag_folders_dic)
		if bf.data['acc_z'].mean() > 5: # the mean should be around 9.5 if acc is in datafile
			break
	indx = random.randint(0,len(bf.data['state_one_steps_1s_indicies'])-1)
	topics = ['steer_z_scored','motor_z_scored','acc_x_z_scored','acc_y_z_scored','acc_z_z_scored','gyro_x_z_scored','gyro_y_z_scored','gyro_z_z_scored',]
	data = []
	target = []
	target2 = []
	for tp in topics:
		zero_topic = False
		if random.random() < 0.2:
			zero_topic = True
		for i in range(N):
			d = bf.data[tp][indx+i]
			target.append(d)
			if i == N-1:
				target2.append(d)
			if zero_topic:
				d *= 0
			data.append(d)
	plt.plot(data)
	plt.plot(target)


	from kzpy3.teg2.data.access.get_data_from_bag_files6 import *
	BF = Bag_Folder('/media/karlzipser/ExtraDrive1/bair_car_data_min_disks/bair_car_data_6_min/caffe_z2_direct_local_sidewalks_02Oct16_15h53m07s_Mr_Orange' )
	BF.load_all_bag_files()
	dd = BF.get_data()

	t0 = time.time()
	for i in range(1000):
		q = an_element(BF.left_image_bound_to_data)
		#dd = BF.get_data()
	print(time.time()-t0)



	from kzpy3.teg2.data.access.get_data_from_bag_files6 import *
	BCD = Bair_Car_Data(opjD('bair_car_data_min'),['play','follow','Tilden','Aug','Sep']) #'campus','caffe'

	BCD.load_bag_folder_images(250./(30./1000.))

	plt.ion()

	t_start()
	for i in range(100000):
		print i
		#try:
		#BF = BCD.bag_folders_dic[a_key(BCD.bag_folders_with_loaded_images)]
		#if len(BF.img_dic['left'])==0:
		#	print "**************** BF.load_all_bag_files() *************"
		#	BF.load_all_bag_files()
		data_dic = BCD.get_data()
		#if np.mod(i,100) == 0:
		#	mi(data_dic['left'])
		#	plt.pause(0.001)
		#except Exception as e:
		#	print d2s("BF.path =,",BF.path,",i =",i,"len(BF.img_dic['left']) = ",len(BF.img_dic['left']))
		#	print e.message, e.args
		#	break
	t_end()



	def get_data(BCD,topics=['steer','motor'],num_topic_steps=10,num_image_steps=2,state_one_steps_indicies_str='state_one_steps_0_5s_indicies'):
		BF = BCD.bag_folders_dic[a_key(BCD.bag_folders_with_loaded_images)]
		return BF.get_data(topics,num_topic_steps,num_image_steps,state_one_steps_indicies_str)





	no_left_ts = []
	for i in range(len(BF.data['timestamps'])):
		t = BF.data['timestamps'][i]
		if np.mod(i,1000)==0:
			print i
		if t not in BF.img_dic['left'].keys():
			print d2s(BF.path,t)
			no_left_ts.append(t)

	plt.figure(1)
	plt.clf()
	plt.plot(a,'o')
	plt.plot(b,'o')


if True:
	from kzpy3.teg2.data.access.get_data_from_bag_files7 import *
	path = opjD('bair_car_data_min/direct_local_sidewalks_27Sep16_16h45m54s_Mr_Orange')# 'bair_car_data_min/play_30Aug2016_Mr_Blue_Tilden_1') #'bair_car_data_min/direct_campus_25Sep16_09h34m37s_Mr_Orange')
	BF=Bag_Folder(path)

	t_start()
	for i in range(100000):
		d=BF.get_data()
		#BF.verify_get_data(d)
	t_end()





from kzpy3.teg2.data.access.get_data_from_bag_files8 import *
f = random.choice(gg(opjD('bair_car_data_min','*')))
f='/home/karlzipser/Desktop/bair_car_data_min/furtive_9August2016'

N_topics = 10
N_frames = N_topics; assert(N_topics >= N_frames)
BF=Bag_Folder(f,N_topics)

t_start()
for i in range(1000):
	d = BF.get_data(['state','steer','motor','encoder','gyro_x','gyro_y','gyro_z','acc_x','acc_y','acc_z'],N_topics,N_frames)
	show_data_dic(d)
	#print "<pause>"
	#plt.pause(0.1)
	plt.title('<pause>')
	BF.incremental_index += N_frames
t_end()

n=10
plt.figure(n)
plt.clf()
mi(d['left'][0],n,[2,2,2],do_clf=False)
mi(d['left'][1],n,[2,2,4],do_clf=False)
mi(d['right'][1],n,[2,2,3],do_clf=False)
mi(d['right'][0],n,[2,2,1],do_clf=False)






from kzpy3.teg2.data.access.get_data_from_bag_files9 import *
path = '/home/karlzipser/Desktop/bair_car_data_min/play_Nino_to_campus_08Oct16_09h00m00s_Mr_Blue_1c'
list0 = []
list1 = ['play','follow','furtive','caffe','direct_from_campus2_08Oct16_10h15m','direct_from_campus_31Dec12_10h00m','direct_to_campus_08Oct16_08h55m37']
#list2 = ['Tilden','play','follow','furtive','play','follow','furtive','caffe','local','Aug','Sep']
list3 = ['direct','caffe','play','follow']
bair_car_data_path = opjD('bair_car_data_min')#'/media/ExtraDrive1/bair_car_data_min'
bair_car_data = Bair_Car_Data(bair_car_data_path,list3)



bf = random.choice(bair_car_data.bag_folders_weighted)
BF = bair_car_data.bag_folders_dic[bf]
BF.path
show_data_dic_sequence(BF)



	self.steer_angle_dic = {}
	for i in range(len(self.data['steer'])):
		steer = self.data['steer'][i]
		steer = int(steer)
		if steer < 0:
			steer = 0
		if steer > 99:
			steer = 99
		if not steer in self.steer_angle_dic:
			self.steer_angle_dic[steer] = []
		self.steer_angle_dic[steer].append(i)
 


	def get_random_steer_equal_weighting(self):
		indx = -99
		steer = np.random.randint(0,100)
		if steer in steer_angle_dic:
			indx = random.choice(steer_angle_dic[steer])
			break
		assert(indx >= 0)
		return indx

from kzpy3.teg2.data.access.get_data_from_bag_files9 import *
bair_car_data_path = opjD('bair_car_data_min')
bair_car_data = Bair_Car_Data_temp(bair_car_data_path,[])


















d=[[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -30, -30, -30, -30],
	[ 11, 9, 6, 12, 11, 16, 23, 21, 23,  14, 20, 29, 26, 32, 31, 36, 40, 35]]

d=[[24, 36, 54, 64, 71, 83, 92, 84,  0, -58, -60, -60, -60, -60, -34, -25, 0],
	[20, 22, 29, 39, 43, 50, 56, 65,  -2, 7, 9, 8, 8, 13, 8, 12, 12]]

[ 10, 27, 51, 87, 90, 90, 112, 114, 120, 14, -30, -60, -60, -60, -60, -60, -60, -60, -90]
[2, 9, 11, 12, 19, 23, 25, 30, 34, 18, -6, -10, -18, -18, -23, -24, -28, -29, -29]

[ 7, 40, 50, 50, 76, 80, 89, 99, 112, 3, 79, 178, 122, 82, 45, -19, -30, -30, -30]
[ -11, -16, -12, -18, -15, -16, -12, -9, -16, 1, 10, 14, 21, 26, 27, 30, 29, 36, 39]












#!/usr/bin/env python
"""
reed to run roslaunch first, e.g.,

roslaunch bair_car bair_car.launch use_zed:=true record:=false
"""

########################################################
#          CAFFE SETUP SECTION
import caffe
caffe.set_device(0)
caffe.set_mode_gpu()
from kzpy3.utils import *
from kzpy3.teg1.rosbag_work.get_data_from_bag_files2 import *
import cv2
os.chdir(home_path) # this is for the sake of the train_val.prototxt

solver_file_path = opjh("kzpy3/caf3/z2/solver_live.prototxt")
weights_file_path = opjD('z2/z2.caffemodel') #
def setup_solver():
	solver = caffe.SGDSolver(solver_file_path)
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	return solver
#solver = setup_solver()
#if weights_file_path != None:
#	print "loading " + weights_file_path
#	solver.net.copy_from(weights_file_path)
#
########################################################





########################################################
#						Caffe
import caffe
caffe.set_device(0)
caffe.set_mode_gpu()
from kzpy3.utils import *
from kzpy3.teg2.data.access.get_data_from_bag_files9 import *
import cv2
os.chdir(home_path) # this is for the sake of the train_val.prototxt
import os, serial, threading, Queue
import threading

img = zeros((94,168,3))
DO_LOADING = False
QUIT = False

def setup_solver():
	solver = caffe.SGDSolver(solver_file_path)
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	return solver

def load_data_into_model(solver,data,flip,show=False):
	global img
	if data == 'END' :
		print """data = 'END':"""
		return False
	if 'left' in data:
		if type(data['left'][0]) == np.ndarray:


			if not flip:
				solver.net.blobs['ZED_data_pool2'].data[0,0,:,:] = data['left'][0][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2'].data[0,1,:,:] = data['left'][1][:,:]/255.0-.5
				#solver.net.blobs['ZED_data_pool2'].data[0,2,:,:] = data['left'][2][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2'].data[0,2,:,:] = data['right'][0][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2'].data[0,3,:,:] = data['right'][1][:,:]/255.0-.5
				#solver.net.blobs['ZED_data_pool2'].data[0,5,:,:] = data['right'][2][:,:]/255.0-.5

			else: # flip left-right
				solver.net.blobs['ZED_data_pool2'].data[0,0,:,:] = scipy.fliplr(data['left'][0][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2'].data[0,1,:,:] = scipy.fliplr(data['left'][1][:,:]/255.0-.5)
				#solver.net.blobs['ZED_data_pool2'].data[0,2,:,:] = scipy.fliplr(data['left'][2][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2'].data[0,2,:,:] = scipy.fliplr(data['right'][0][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2'].data[0,3,:,:] = scipy.fliplr(data['right'][1][:,:]/255.0-.5)
				#solver.net.blobs['ZED_data_pool2'].data[0,5,:,:] = scipy.fliplr(data['right'][2][:,:]/255.0-.5)

			Direct = 0.
			Follow = 0.
			Play = 0.
			Furtive = 0.
			Caf = 0

			#print data['bag_filename']

			if 'follow' in data['path']:
				Follow = 1.0
			if 'direct' in data['path']:
				Direct = 1.0
			if 'play' in data['path']:
				Play = 1.0
			if 'furtive' in data['path']:
				Furtive = 1.0
			if 'caffe' in data['path']:
				Caf = 1.0

			solver.net.blobs['metadata'].data[0,0,:,:] = 0
			solver.net.blobs['metadata'].data[0,1,:,:] = Caf
			solver.net.blobs['metadata'].data[0,2,:,:] = Follow
			solver.net.blobs['metadata'].data[0,3,:,:] = Direct
			solver.net.blobs['metadata'].data[0,4,:,:] = Play
			solver.net.blobs['metadata'].data[0,5,:,:] = Furtive
			#solver.net.blobs['metadata'].data[0,6,:,:] = target_data[0] #current steer
			#solver.net.blobs['metadata'].data[0,7,:,:] = target_data[len(target_data)/2] #current motor
			#solver.net.blobs['metadata'].data[0,8,:,:] = 0
			#solver.net.blobs['metadata'].data[0,9,:,:] = 0

		else:
			print """not if type(data['left']) == np.ndarray: """+str(time.time())
	else:
		pass #print """not if 'left' in data: """+str(time.time())
		return 'no data'
	if show:
		show_solver_data(solver,data,flip,49.,1.)
	return True






########################################################
#          				ROSPY
import roslib
import std_msgs.msg
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge,CvBridgeError
bridge = CvBridge()
rospy.init_node('listener',anonymous=True)
left_list = []
right_list = []
state = 0
def state_callback(data):
	global state
	state = data.data
def right_callback(data):
	global left_list, right_list, solver
	cimg = bridge.imgmsg_to_cv2(data,"bgr8")
	if len(right_list) > 5:
		right_list = right_list[-5:]
	right_list.append(cimg)
def left_callback(data):
	global left_list, right_list
	cimg = bridge.imgmsg_to_cv2(data,"bgr8")
	if len(left_list) > 5:
		left_list = left_list[-5:]
	left_list.append(cimg)
rospy.Subscriber("/bair_car/zed/right/image_rect_color",Image,right_callback,queue_size = 1)
rospy.Subscriber("/bair_car/zed/left/image_rect_color",Image,left_callback,queue_size = 1)
rospy.Subscriber('/bair_car/state',std_msgs.msg.Int32,state_callback)
#
# $ roscore
# $ rosbag play /home/karlzipser/Desktop/bair_car_data_min_disks/bair_car_data_6_min/direct_local_sidewalk_test_data_01Nov16_14h59m31s_Mr_Orange/*.bag
#
#
########################################################



weights_file_path = most_recent_file_in_folder(opjD('z2'),['z2','caffemodel']) 
solver_file_path = opjh("kzpy3/caf3/z2/solver.prototxt")
solver = setup_solver()
solver.net.copy_from(weights_file_path)


while not rospy.is_shutdown():
	
	if len(left_list) > 4:
		l0 = left_list[-2]
		l1 = left_list[-1]
		r0 = right_list[-2]
		r1 = right_list[-1]

		data = {}
		data['left'] = []
		data['right'] = []
		data['left'].append(imresize(l0[:,:,1],0.25)) # on TX1, this is done in model (see tran_val_live.prototxt)
		data['left'].append(imresize(l1[:,:,1],0.25))
		data['right'].append(imresize(r0[:,:,1],0.25))
		data['right'].append(imresize(r1[:,:,1],0.25))
		data['path'] = "/...direct.../"
				
		load_data_into_model(solver, data, flip=False)
		solver.net.forward()
		model_steer = 100*solver.net.blobs['ip2'].data[0,9]
		model_motor = 100*solver.net.blobs['ip2'].data[0,19]

		img = l1
		steer_rect_color = [0,0,255] # red in BGR
		apply_rect_to_img(img,model_steer,0,99,steer_rect_color,steer_rect_color,0.9,0.1,center=True,reverse=True,horizontal=True)
		apply_rect_to_img(img,model_motor,49,99,steer_rect_color,steer_rect_color,0.8,0.05,center=False,reverse=True,horizontal=False)

		cv2.imshow("Left",img)
		cv2.waitKey(1)





