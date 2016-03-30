"""
run "kzpy3/caf/training/y2016/m3/RPi3/train.py"
"""

import caffe
from kzpy3.utils import *
from kzpy3.caf2.protos import *

"""
CAFFE_TRAINING_MODE = 'CAFFE_TRAINING_MODE'
CAFFE_DEPLOY_MODE = 'CAFFE_DEPLOY_MODE'
CAFFE_TRAJECTORY_TRAINING_MODE = 'CAFFE_TRAJECTORY_TRAINING_MODE'
run_mode = CAFFE_TRAINING_MODE
CAFFE_DATA = opjD('RPi3_data/all_runs_dics/runs_scl_25_BW')
CAFFE_FRAME_RANGE = (-15,-6)
"""

#############################################################
#  Standard sort of net
model_name = 'test'
n_targets = 3
run_mode = 'CAFFE_TRAINING_MODE'
CAFFE_DATA = opjD('RPi3_data/all_runs_dics/runs_scl_25_BW')
p = '# ' + model_name + '\n'
p = p + dummy('ddata',(1,9,56,75))
p = p + dummy('ddata2',(1,n_targets))
p = p + python('py_image_data','ddata','kz_layers2','SimpleLayer4')
p = p + python('py_target_data','ddata2','kz_layers2','SimpleLayer5')
p = p + conv_layer_set(
	c_top='conv1',c_bottom='py_image_data',c_num_output=96,c_group=1,c_kernel_size=11,c_stride=3,c_pad=0,
	p_type='MAX',p_kernel_size=3,p_stride=2,p_pad=0,
	weight_filler_type='gaussian',std=0.1)
p = p + conv_layer_set(
	c_top='conv2',c_bottom='conv1_pool',c_num_output=256,c_group=2,c_kernel_size=5,c_stride=3,c_pad=0,
	p_type='MAX',p_kernel_size=3,p_stride=2,p_pad=0,
	weight_filler_type='gaussian',std=0.1)
p = p + ip_layer_set('ip1','conv2_pool',512,'xavier')
p = p + ip_layer_set('ip2','ip1',n_targets,'xavier')
p = p + euclidian('euclidian','ip2','py_target_data')
print p
s = solver('test')
print s

list_of_strings_to_txt_file(opjD('train_val.prototxt'),p.split('\n'))
list_of_strings_to_txt_file(opjD('solver.prototxt'),s.split('\n'))
#
#############################################################

training_path = opjD('.')
solver_name = 'solver.prototxt'

def show_solver(solver):
	print('blobs')
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	print('\nparams')
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)

def setup_solver():
	solver = caffe.SGDSolver(opj(training_path,solver_name))
	show_solver(solver)
	if host_name == 'redwood2':
		caffe.set_device(0)
		caffe.set_mode_gpu()
		print("************** using GPU *************")
	return solver

solver = setup_solver()  
blobs = solver.net.blobs

def safe_solver_step(solver):
	while True:
		try:
			solver.step(10000)
			for k in solver.net.blobs.keys():
				print (k, solver.net.blobs[k].data.max())
		except Exception, e:
			print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
			print e
			print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'





"""
#####################
solver.prototxt file
train_val.prototxt file
model name: this will determine all file names
layer module
trained model files, appropriate directories 
I find that deep directory structures are hard to deal with, better to have just model name folders
#####################


"""


