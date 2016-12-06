from kzpy3.teg3.data.preprocess.preprocess_bag_data import *

bfp = '/media/karlzipser/rosbags/caffe_direct_local_sidewalks_05Dec16_15h03m35s_Mr_Blue'

preprocess_bag_data(bfp,[]);


L=load_obj('/home/karlzipser/Desktop/direct_home_06Dec16_08h10m47s_Mr_Blue/.preprocessed2/left_image_bound_to_data.pkl')
ts = sorted(L.keys())
dts = [0]
for i in range(1,len(ts)):
	dts.append(ts[i] - ts[i-1])
figure(1)
plot(ts,dts)
figure(2)
hist(dts)


"""
L=load_obj('/media/karlzipser/bair_car_data_7/rosbags14/direct_racing_Tilden_27Nov16_10h41m05s_Mr_Blue/.preprocessed2/left_image_bound_to_data.pkl')
ts = sorted(L.keys())
dts = [0]
for i in range(1,len(ts)):
	dts.append(ts[i] - ts[i-1])
figure(3)
plot(ts,dts)
figure(4)
hist(dts)

"""

pass
