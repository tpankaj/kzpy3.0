from kzpy3.utils import *

def load_data_into_model_version_1(solver,data,flip):
	return True

def load_data_into_model_version_2(solver,data,flip):
	if data == 'END' :
		print """data = 'END':"""
		return False
	if 'left' in data:
		if type(data['left'][0]) == np.ndarray:
			target_data = list(data['steer'])
			target_data += list(data['motor'])
			target_data[0] = data['steer'][0]
			target_data[10] = data['motor'][0]

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
				for i in range(len(target_data)/2):
					t = target_data[i]
					t = t - 49
					t = -t
					t = t + 49
					target_data[i] = t
				if data['meta-turn'] > -10:
					t = data['meta-turn']
					t = t - 49
					t = -t
					t = t + 49					
					data['meta-turn'] = t

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

			solver.net.blobs['metadata'].data[0,0,:,:] = data['meta-turn']/100.
			solver.net.blobs['metadata'].data[0,1,:,:] = Caf
			solver.net.blobs['metadata'].data[0,2,:,:] = Follow
			solver.net.blobs['metadata'].data[0,3,:,:] = Direct
			solver.net.blobs['metadata'].data[0,4,:,:] = Play
			solver.net.blobs['metadata'].data[0,5,:,:] = Furtive
			#solver.net.blobs['metadata'].data[0,6,:,:] = target_data[0] #current steer
			#solver.net.blobs['metadata'].data[0,7,:,:] = target_data[len(target_data)/2] #current motor
			#solver.net.blobs['metadata'].data[0,8,:,:] = 0
			#solver.net.blobs['metadata'].data[0,9,:,:] = 0


			for i in range(len(target_data)):
				solver.net.blobs['steer_motor_target_data'].data[0,i] = target_data[i]/99.

		else:
			print """not if type(data['left']) == np.ndarray: """+str(time.time())
	else:
		pass #print """not if 'left' in data: """+str(time.time())
		return 'no data'
	#show_solver_data(solver,data,flip,49.,1.)
	return True

