"""
ipy
import kzpy3.caf2.models.y2016m3.zeroth_model.define
from kzpy3.caf2.utils.train import *
solver = setup_solver('y2016m3.zeroth_model')
"""

from kzpy3.utils import *
import caffe

def setup_solver(model_name,training_path=opjh('kzpy3/caf2/tmp'),solver_name='solver.prototxt'):
	exec('import '+'kzpy3.caf2.models.'+model_name)
	solver = caffe.SGDSolver(opj(training_path,solver_name))
	show_solver(solver)
	if host_name == 'redwood2':
		caffe.set_device(0)
		caffe.set_mode_gpu()
		print("************** using GPU *************")
	return solver

def show_solver(solver):
	print('###############################')
	print('blobs')
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	print('###############################')
	print('params')
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	print('###############################')

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

def my_vis_square(data,padsize=5,padval=0,fig_num='my_vis_square'):
	data = data.copy()
	data = z2o(data)
	n = int(np.ceil(np.sqrt(data.shape[0])))
	fx = np.shape(data)[2]
	fz = np.shape(data)[1]
	img = np.zeros((padsize+(padsize+fx)*n,padsize+(padsize+fx)*n))+0.5
	for x in range(n):
		for y in range(n):
			if y+x*n < data.shape[0]:
				img[(padsize*(1+x)+(x*(fx))):(padsize*(1+x)+((x+1)*fx)),(padsize*(1+y)+(y*fx)):(padsize*(1+y)+((y+1)*fx))] = data[y+x*n,0,:,:]
	mi(img,fig_num)


def scp_weights_from_redwood2(model_path):
	unix(d2s("""scp kzipser@redwood2.dyn.berkeley.edu:'""" + model_path + """' ~/Desktop""" ))



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


