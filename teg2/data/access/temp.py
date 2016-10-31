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


