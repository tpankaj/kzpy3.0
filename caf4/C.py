from kzpy3.teg3.data.access.access_bag_files import *
from kzpy3.caf4.Caffe_Net import *

caffe_net = Caffe_Net('/home/karlzipser/kzpy3/caf3/z2/solver_live.prototxt','version 1')

		    
loaded_bag_files_names = {}
played_bagfile_dic = {}

BF_dic = load_Bag_Folders(opjD('runs'))

threading.Thread(target=bag_file_loader_thread,args=(BF_dic,5*60,loaded_bag_files_names,played_bagfile_dic)).start()

"""
for i in range(40):
	print "waiting..."
	time.sleep(1)
"""

while True:
	data = get_data(BF_dic,played_bagfile_dic)
	if data != None:
		for i in range(len(data['left'])):
			img = data['left'][i].copy()
			steer = data['steer'][i]
			motor = data['motor'][i]
			gyro_x = data['gyro_x'][i]
			gyro_yz_mag = data['gyro_yz_mag'][i]

			apply_rect_to_img(img,steer,0,99,steer_rect_color,steer_rect_color,0.9,0.1,center=True,reverse=True,horizontal=True)
			apply_rect_to_img(img,motor,0,99,steer_rect_color,steer_rect_color,0.9,0.1,center=True,reverse=True,horizontal=False)
			apply_rect_to_img(img,gyro_yz_mag,-150,150,steer_rect_color,steer_rect_color,0.13,0.03,center=True,reverse=True,horizontal=False)
			apply_rect_to_img(img,gyro_x,-150,150,steer_rect_color,steer_rect_color,0.16,0.03,center=True,reverse=True,horizontal=False)

			cv2.imshow('left',cv2.cvtColor(img,cv2.COLOR_RGB2BGR))#.astype('uint8')
			if cv2.waitKey(33) & 0xFF == ord('q'):
			    break
		caffe_net.train_step(data)			    


