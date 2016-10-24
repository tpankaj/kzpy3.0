

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
BCD = Bair_Car_Data(opjD('bair_car_data_min'),[])#['play','follow','Tilden','Aug','Sep'])

for i in range(7):
	t0 = time.time()
	print d2s("*************** i =",i,"*************************")
	BCD.load_bag_folder_images(100./(30./1000.))
	print d2s("time =",time.time()-t0)




