#! /usr/bin/python
#//anaconda/bin/python

import caffe
from kzpy3.utils import *
from kzpy3.teg2.data.access.get_data_from_bag_files8 import *
import cv2
os.chdir(home_path) # this is for the sake of the train_val.prototxt



loss_timer = time.time()
loss = []


def setup_solver():
	solver = caffe.SGDSolver(solver_file_path)
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	return solver



img = zeros((94,168,3)
def load_data_into_model(solver,data,flip):
	global img
	if data == 'END' :
		print """data = 'END':"""
		return False
	if 'left' in data:
		if type(data['left'][0]) == np.ndarray:
			target_data = list(100*(data['steer']-data['steer'][0]))
			target_data += list(500*(data['motor']-data['motor'][0]))
			target_data[0] = data['steer'][0]-49
			target_data[10] = data['motor'][0]-49

			if not flip:
				solver.net.blobs['ZED_data_pool2'].data[0,0,:,:] = data['left'][0][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2'].data[0,1,:,:] = data['left'][1][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2'].data[0,2,:,:] = data['left'][2][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2'].data[0,3,:,:] = data['right'][0][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2'].data[0,4,:,:] = data['right'][1][:,:]/255.0-.5
				solver.net.blobs['ZED_data_pool2'].data[0,5,:,:] = data['right'][2][:,:]/255.0-.5

			else: # flip left-right
				solver.net.blobs['ZED_data_pool2'].data[0,0,:,:] = scipy.fliplr(data['left'][0][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2'].data[0,1,:,:] = scipy.fliplr(data['left'][1][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2'].data[0,2,:,:] = scipy.fliplr(data['left'][2][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2'].data[0,3,:,:] = scipy.fliplr(data['right'][0][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2'].data[0,4,:,:] = scipy.fliplr(data['right'][1][:,:]/255.0-.5)
				solver.net.blobs['ZED_data_pool2'].data[0,5,:,:] = scipy.fliplr(data['right'][2][:,:]/255.0-.5)
				for i in range(len(target_data)/2):
					t = target_data[i]
					t = -t
					target_data[i] = t

			Direct = 0.
			Follow = 0.
			Play = 0.
			Furtive = 0.
			Caf = 0

			if 'follow' in data['path']:
				if 'direct' in data['path']:
					Direct = -1.0
				if 'play' in data['path']:
					Play = -1.0
				if 'furtive' in data['path']:
					Furtive = -1.0
				if 'caffe' in data['path']:
					Caf = -1.0
			else:
				if 'direct' in data['path']:
					Direct = 1.0
				if 'play' in data['path']:
					Play = 1.0
				if 'furtive' in data['path']:
					Furtive = 1.0
				if 'caffe' in data['path']:
					Caf = 1.0
			
			solver.net.blobs['metadata'].data[0,0,:,:] = target_data[0] #current steer
			solver.net.blobs['metadata'].data[0,1,:,:] = target_data[len(target_data)/2] #current motor
			solver.net.blobs['metadata'].data[0,2,:,:] = Caf
			solver.net.blobs['metadata'].data[0,3,:,:] = Direct
			solver.net.blobs['metadata'].data[0,4,:,:] = Play
			solver.net.blobs['metadata'].data[0,5,:,:] = Furtive

			for i in range(len(target_data)):
				solver.net.blobs['steer_motor_target_data'].data[0,i] = target_data[i]/99.

		else:
			print """not if type(data['left']) == np.ndarray: """+str(time.time())
	else:
		pass #print """not if 'left' in data: """+str(time.time())
		return 'no data'
	#show_solver_data(solver,data,flip)
	return True




def show_solver_data(solver,data,flip):
	caffe_steer_color_color = [1.,0,0]
	human_steer_color_color = [0,0,1.]

	data_img_shape = np.shape(solver.net.blobs['ZED_data_pool2'].data)
	num_frames = (data_img_shape[1])/2
	print num_frames		
	img = np.zeros((data_img_shape[2],data_img_shape[3],3))+0.5
	img[0,0,:]=1
	img[0,1,:]=0
	mi(img)
	plt.pause(0.5)
	for i in range(10):#num_frames):
		#print i
		#if i > 0:
		#    img_prev = img.copy()

		if not flip:
			d = data['left'][i][:,:]/255.0-.5
		else:
			d = scipy.fliplr(data['left'][i][:,:]/255.0-.5)
		d = z2o(d)
		if i < 2:
			img[:,:,0] = z2o(solver.net.blobs['ZED_data_pool2'].data[0,i,:,:])
		else:
			img[:,:,0] = d #z2o(solver.net.blobs['ZED_data_pool2'].data[0,i+2,:,:])
		img[:,:,1] = img[:,:,0].copy()
		img[:,:,2] = img[:,:,0].copy()

		if solver.net.blobs['metadata'].data[0,1,0,0] == 1.0: #caffe is steering
		    steer_rect_color = caffe_steer_color_color
		else:
			steer_rect_color = human_steer_color_color

		steer = 99*solver.net.blobs['steer_motor_target_data'].data[0,0]
		apply_rect_to_img(img,steer,0,99,steer_rect_color,steer_rect_color,0.9,0.1,center=True,reverse=True,horizontal=True)

		mi(img,img_title=d2s(flip,i))#,img_title=(d2s('dt = ', int(1000*dt),'ms')))
		#print solver.net.blobs['steer_motor_target_data'].data
		plt.pause(0.25)



def run_solver(solver, bair_car_data, num_steps,flip):
	global img
	global loss
	#if time.time() - loss_timer > 60*15:
	#	save_obj(loss,opjD('z2_2nd_pass','loss'))
	step_ctr = 0
	ctr = 0
	if True: #try:
		while step_ctr < num_steps:
			imshow = False
			datashow = False
			if np.mod(ctr,100) == 0:
				imshow = True
			if np.mod(ctr,1010) == 0:
				datashow = True


			bf = random.choice(bair_car_data.bag_folders_weighted)
			BF = bair_car_data.bag_folders_dic[bf]
			indx,steer = BF.get_random_steer_equal_weighting()
			data = BF.get_data(num_image_steps=3,good_start_index=indx)
			result = load_data_into_model(solver, data,flip)
			#result = load_data_into_model(solver, bair_car_data.get_data(['steer','motor'],10,10),flip)
			if result == False:
				break
			if result == True:
				solver.step(1)
				a = solver.net.blobs['steer_motor_target_data'].data[0,:] - solver.net.blobs['ip2'].data[0,:]
				loss.append(np.sqrt(a * a).mean())
				ctr += 1
				if imshow:
					#print (ctr,np.array(loss[-99:]).mean())
					img[:,:,0] = solver.net.blobs['ZED_data_pool2'].data[0,0,:,:]
					img += 0.5
					img *= 255.
					img[:,:,1] = img[:,:,0]
					img[:,:,2] = img[:,:,0]
					cv2.imshow('left',img.astype('uint8'))
					#cv2.imshow('right',solver.net.blobs['ZED_data_pool2'].data[0,2,:,:])
					"""
					img[:,:,0] = solver.net.blobs['ZED_data_pool2'].data[0,2,:,:]
					img[:,:,1] = img[:,:,0]
					img[:,:,2] = img[:,:,0]
					cv2.imshow('right',img)
					#cv2.imshow('right',solver.net.blobs['ZED_data_pool2'].data[0,2,:,:])
					"""
					if cv2.waitKey(1) & 0xFF == ord('q'):
					    pass
					#print np.round(solver.net.blobs['steer_motor_target_data'].data[0,:][:3],3)
					#print np.round(solver.net.blobs['ip2'].data[0,:][:3],3)
			

				if datashow:
					print (ctr,np.array(loss[-1000:]).mean())
					print(solver.net.blobs['metadata'].data[0,:,5,5])
					print array_to_int_list(solver.net.blobs['steer_motor_target_data'].data[0,:][:])
					print array_to_int_list(solver.net.blobs['ip2'].data[0,:][:])
			step_ctr += 1
	#except Exception as e:
	#	print "train ***************************************"
	#	print e.message, e.args
	#	print "***************************************"


def array_to_int_list(a):
	l = []
	for d in a:
		l.append(int(d*1000))
	return l


#['play','follow','furtive']


#if __name__ == '__main__':
bair_car_data_path = opjD('bair_car_data_min')#'/media/ExtraDrive1/bair_car_data_min'
assert(len(gg(opj(bair_car_data_path,'*'))) > 5)

list0 = []
list1 = ['play','follow','furtive','caffe','direct_from_campus2_08Oct16_10h15m','direct_from_campus_31Dec12_10h00m','direct_to_campus_08Oct16_08h55m37']
list2 = ['Tilden','play','follow','furtive','play','follow','furtive','caffe','local','Aug','Sep']
list3 = ['follow','furtive','direct_from_campus2_08Oct16_10h15m','direct_from_campus_31Dec12_10h00m','direct_to_campus_08Oct16_08h55m37']


bair_car_data = Bair_Car_Data(bair_car_data_path,list3)
#unix('mkdir -p '+opjD('z2_2nd_pass'))
#bair_car_data = Bair_Car_Data('/home/karlzipser/Desktop/bair_car_data_min/',1000,100)


caffe.set_device(0)
caffe.set_mode_gpu()

solver_file_path = opjh("kzpy3/caf3/z2_2nd_pass/solver.prototxt")
solver = setup_solver()


weights_file_path = most_recent_file_in_folder(opjD('z2_2nd_pass'),['z2_2nd_pass','caffemodel']) 
if weights_file_path == "None":
	weights_file_path = None
if weights_file_path != None:
	print "loading " + weights_file_path
	solver.net.copy_from(weights_file_path)
	



def main():
	weights_file_path = most_recent_file_in_folder(opjD('z2_2nd_pass'),['z2_2nd_pass','caffemodel']) 
	if weights_file_path == "None":
		weights_file_path = None
	if weights_file_path != None:
		print "loading " + weights_file_path
		solver.net.copy_from(weights_file_path)
	while True:
		try:
			t_start()
			bair_car_data.load_bag_folder_images(3400)
			t_end()
			t_start()

			for i in range(150):
				if np.random.random() > 0.5:
					flip = False
				else:
					flip = True
				run_solver(solver,bair_car_data,1000,flip)
			t_end()
			#except KeyboardInterrupt:
			#    print 'Interrupted'
		except Exception as e:
			print "train loop ***************************************"
			print e.message, e.args
			print "***************************************"


"""
except KeyboardInterrupt:
        print 'Interrupted'
"""

