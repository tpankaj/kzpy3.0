#! /usr/bin/python
#//anaconda/bin/python
#
import caffe
USE_GPU = True
if USE_GPU:
	caffe.set_device(0)
	caffe.set_mode_gpu()
from kzpy3.utils import *
from kzpy3.caf4.load_data_into_model_versions import *
import cv2
os.chdir(home_path) # this is for the sake of the train_val.prototxt

class Caffe_Net:

	def __init__(self,solver_file_path,version,weights_file_mode=None,weights_file_path=None):
		self.version = version
		self.solver = _setup_solver(solver_file_path)
		if weights_file_mode == 'most recent':
			weights_file_path = most_recent_file_in_folder(weights_file_path)
		elif weights_file_mode == 'this one':
			pass
		elif weights_file_mode == None:
			pass
		else:
			assert(False)
		if weights_file_path != None:
			cprint("loading " + weights_file_path,'red','on_yellow')
			solver.net.copy_from(weights_file_path)

	def train_step(self,data):
		if np.random.random() > 0.5:
			flip = False
		else:
			flip = True
		result = _load_data_into_model(self.solver,self.version,data,flip)
		if result:
			self.solver.step(1)




def _setup_solver(solver_file_path):
	solver = caffe.SGDSolver(solver_file_path)
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	return solver



def _load_data_into_model(solver,version,data,flip):
	if version == 'version 1':
		return load_data_into_model_version_1(solver,data,flip)

