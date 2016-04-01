from kzpy3.caf2.utils.protos import *
"""
from kzpy3.caf2.models.<MODEL_NAME>.define import *
"""
#############################################################
#  
model_name = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
purpose = """
A model that looks at lower half of scale 50 BW image sequences,
frame range (-15,-6) to predict steer at frame 0.
tested with jitter, reverse contrast, and noise.
###############################
blobs
('ddata', (1, 9, 50, 144))
('ddata2', (1, 3))
('py_image_data', (1, 9, 50, 144))
('py_target_data', (1, 3))
('conv1', (1, 96, 14, 45))
('conv1_pool', (1, 96, 7, 22))
('conv2', (1, 256, 3, 10))
('conv2_pool', (1, 256, 1, 5))
('ip1', (1, 512))
('ip2', (1, 3))
('euclidian', ())
###############################
params
('conv1', (96, 9, 11, 11))
('conv2', (256, 48, 3, 3))
('ip1', (512, 1280))
('ip2', (3, 512))
###############################
"""

c = """
CAFFE_MODE = 'train'
CAFFE_TRAIN_DATA = opjD('RPi3_data/all_runs_dics/runs_scale_50_BW')
CAFFE_TEST_DATA = opjD('RPi3_data/all_runs_dics/runs_scale_50_BW_test')
CAFFE_FRAME_RANGE = (-15,-6)
USE_REVERSE_CONTRAST = True
USE_BOTTOM_HALF = True
USE_NOISE = True
USE_JITTER = True
jitter = 6
input_size = (1,9,56-jitter,150-jitter)
"""
#copy_from = 'latest'
#
#############################################################
#

exec(c)

n_targets = 3
p = '# ' + model_name + '\n'
p = p + '# ' + time_str()
p = p + '\n# '.join(purpose.split('\n'))
p = p + dummy('py_image_data',input_size)
p = p + dummy('py_target_data',(1,n_targets))
p = p + conv_layer_set(
	c_top='conv1',c_bottom='py_image_data',c_num_output=96,c_group=1,c_kernel_size=11,c_stride=3,c_pad=0,
	p_type='MAX',p_kernel_size=3,p_stride=2,p_pad=0,
	weight_filler_type='gaussian',std=0.1)
p = p + conv_layer_set(
	c_top='conv2',c_bottom='conv1_pool',c_num_output=256,c_group=2,c_kernel_size=3,c_stride=2,c_pad=0,
	p_type='MAX',p_kernel_size=3,p_stride=2,p_pad=0,
	weight_filler_type='gaussian',std=0.1)
p = p + ip_layer_set('ip1','conv2_pool',512,'xavier')
p = p + ip_layer_set('ip2','ip1',n_targets,'xavier')
p = p + euclidean('euclidean','ip2','py_target_data')
#
#############################################################
#
s = solver_proto(model_name)
#
#############################################################

#############################################################
#
tmp_path = opjh('kzpy3/caf2/models',model_name,'tmp')
list_of_strings_to_txt_file(opj(tmp_path,'__info__.py'),c.split('\n'))
s_path = opj(tmp_path,'solver.prototxt')
p_path = opj(tmp_path,'train_val.prototxt')
list_of_strings_to_txt_file(p_path,p.split('\n'))
print('Saved '+p_path)
list_of_strings_to_txt_file(s_path,s.split('\n'))
print('Saved '+s_path)
del s,c,p,s_path,p_path
#
#############################################################
#
if True:
	from kzpy3.caf2.utils.train import *
	solver = setup_solver(model_name)
#
#############################################################

blobs = solver.net.blobs
#blobs['py_image_data'].data[:] = np.random.random((1, 9, 50, 144))
# for i in range(9):mi(solver.net.blobs['py_image_data'].data[0,i,:,:]);plt.pause(0.2)
# my_vis_square(solver.net.params['conv1'][0].data)
# solver.net.copy_from('/Users/karlzipser/scratch/caf2_models/m3d31_example_model_iter_2500000.caffemodel')