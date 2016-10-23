

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


