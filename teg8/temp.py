from kzpy3.caf6.cafutils import *
from kzpy3.caf6.protos import *

def print_solver(solver):
	print("")
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	print("")
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		if 'split' not in l[0]:
			print(l)

def setup_solver(solver_file_path):
	solver = caffe.SGDSolver(solver_file_path)
	print_solver(solver)
	return solver

##############################################################################
#
model_path = opjh("kzpy3/caf7/z3_color")
gpu = None
restore_solver = False
base_lr = 0.05
snapshot = 100000
#ignore = [reject_run,left,out1_in2,Smyth,racing] # runs with these labels are ignored
require_one = [] # at least one of this type of run lable is required
use_states = [1]
weights_file_mode = 'most recent' # 'this one' #None #'most recent' #None #'most recent'
weights_file_path =  opjD(fname(model_path)) #opjD('z2_color_trained_12_15_2016') #opjD('z2_color_long_train_21_Jan2017') #None #opjh('kzpy3/caf6/z2_color/z2_color.caffemodel') #None #'/home/karlzipser/Desktop/z2_color' # None #opjD('z2_color')
#
##############################################################################
#
train_val_lst = [
	d2s('#',model_path),
	d2s('#',time_str('Pretty')),

	dummy('left_pool2',(1,12,94,168)),
	dummy('right_pool2',(1,12,94,168)),

	conv("conv1_left",'left_pool2',48,1,3,2,0,"gaussian",std='0.00001'),
	relu("conv1_left"),
	pool("conv1_left","MAX",3,2,0),
	drop('conv1_left_pool',0.0),

	conv("conv1_right",'right_pool2',48,1,3,2,0,"gaussian",std='0.00001'),
	relu("conv1_right"),
	pool("conv1_right","MAX",3,2,0),
	drop('conv1_right_pool',0.0),

	concat('conv1_concat',["conv1_left","conv1_right"],1),
	concat('conv1_pool_concat',["conv1_left_pool","conv1_right_pool"],1),

	conv("conv2a_bi",'conv1_concat',48,1,3,2,0,"gaussian",std='0.00001'),
	relu("conv2a_bi"),
	pool("conv2a_bi","MAX",3,2,0),

	conv("conv2b_bi",'conv1_pool_concat',48,1,3,2,0,"gaussian",std='0.00001'),
	relu("conv2b_bi")
]
"""
	concat('conv2_concat',["conv2a_bi","conv2b_bi"],1),

	conv("conv2_1x1",'conv2_concat',16,1,1,1,0,"gaussian",std='0.00001'),
	relu("conv2_1x1"),
	conv("conv2_3x3",'conv2_concat',16,1,1,1,0,"gaussian",std='0.00001'),
	relu("conv2_3x3"),
	
]
"""
#
##############################################################################
##############################################################################
##############################################################################

unix(d2s('mkdir -p',opjD(fname(model_path))))

if gpu != None:
	caffe.set_device(gpu)
	caffe.set_mode_gpu()

for t in train_val_lst:
	print t
list_of_strings_to_txt_file(opj(model_path,'train_val.prototxt'),train_val_lst)

write_solver(model_path,base_lr=base_lr,snapshot=snapshot)

setup_solver(opj(model_path,'solver.prototxt'))

