from kzpy3.teg4.data.preprocess.preprocess_bag_data import *

#preprocess_bag_data('/media/karlzipser/rosbags/direct_racing_Tilden_24Dec16_21h11m31s_Mr_Blue'  )
#L = load_obj('/media/karlzipser/rosbags/direct_racing_Tilden_24Dec16_18h53m06s_Mr_Blue/.preprocessed2/left_image_bound_to_data.pkl' )
#L = load_obj('/home/karlzipser/Desktop/bair_car_data/new_meta_23/caffe_z2_direct_Tilden_23Dec16_15h22m12s_Mr_Orange/left_image_bound_to_data.pkl')
#L = load_obj('/media/karlzipser/rosbags/direct_racing_Tilden_24Dec16_21h11m31s_Mr_Blue/.preprocessed2/left_image_bound_to_data.pkl')
#preprocess_bag_data('/media/karlzipser/rosbags/direct_local_25Dec16_21h46m56s_Mr_X')
#L = load_obj('/media/karlzipser/rosbags/direct_local_25Dec16_21h46m56s_Mr_X/.preprocessed2/left_image_bound_to_data.pkl')

#preprocess_bag_data('/media/karlzipser/bair_car_data_8/bcd2/caffe_direct_local_26Dec16_16h27m57s_Mr_Blue_original_clone')
L = load_obj('/media/karlzipser/rosbags1/direct_local_29Dec16_16h15m39s_Mr_Black_with_Mr_Silver/.preprocessed2/left_image_bound_to_data.pkl')

ts = sorted(L.keys())

dts = []

for i in range(1,len(ts)):
	dt = ts[i]-ts[i-1]
	#if dt > 0.08:
	#	dt = 0.08
	dts.append(dt)

plot(ts[1:],dts)
figure(5);hist(dts)