

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
