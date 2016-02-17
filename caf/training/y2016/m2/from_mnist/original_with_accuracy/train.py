'''
16 Feb 2016

from kzpy3.caf.training.y2016.m2.from_mnist.original_with_accuracy.train import *; #safe_solver_step(solver)

'''

from kzpy3.vis import *
import caffe
plt.ion()
plt.show()
os.chdir(home_path) # this is for the sake of the train_val.prototxt


def setup_solver():
	solver = caffe.SGDSolver(opjh("kzpy3/caf/training/y2016/m2/from_mnist/original_with_accuracy/solver.prototxt"))
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	return solver


solver = setup_solver()

#show_solver_step(solver)


def safe_solver_step(solver):
    while True:
        try:
            solver.step(10000)
        except Exception, e: 
            print e

"""
solver.step(1)
for i in range(9):
    plt.figure(9)
    plt.clf()
    mi(solver.net.blobs['py_image_data'].data[0,i,:,:],9,img_title=d2s(solver.net.blobs['py_target_data'].data[0][:],solver.net.blobs['ip2'].data))
    plt.pause(0.0001)

"""

def show_solver_step(solver):
	solver.net.forward()
	img = np.zeros((224,298,3))
	img[:,:,0] = solver.net.blobs['py_image_data'].data[0,6,:,:]+0.5
	img[:,:,1] = solver.net.blobs['py_image_data'].data[0,7,:,:]+0.5
	img[:,:,2] = solver.net.blobs['py_image_data'].data[0,8,:,:]+0.5
	#plt.figure(1)
	#plt.clf()
	#mi(img,1)
	print( solver.net.blobs['py_target_data'].data[0])
	print( solver.net.blobs['ip2'].data)
	print( solver.net.blobs['identity'].data)
	plt.figure(2)
	#plt.clf()
	plt.plot([0,1],[0,1],'k')
	plt.plot(solver.net.blobs['py_target_data'].data[0][9:].mean(),solver.net.blobs['ip2'].data[0][9:].mean(),'ro')
	plt.plot(solver.net.blobs['py_target_data'].data[0][:9].mean(),solver.net.blobs['ip2'].data[0][:9].mean(),'bo')
	plt.xlim((0,1))
	plt.ylim((0,1))


def test_solver(solver,n,fig=100):
	St_list = []
	Ft_list = []
	Rt_list = []
	So_list = []
	Fo_list = []
	Ro_list = []
	for i in range(n):
		solver.net.forward()
		t = solver.net.blobs['py_target_data'].data[0]
		o = solver.net.blobs['ip2'].data[0]
		St_list.append(t[0])
		So_list.append(o[0])
		Ft_list.append(t[1])
		Fo_list.append(o[1])
		Rt_list.append(t[2])
		Ro_list.append(o[2])
	plt.figure(fig,(5,7))
	plt.clf()
	plt.plot(Ft_list,Fo_list,'gx',label='frames to turn')
	plt.plot(Rt_list,Ro_list,'rx',label='rot')
	plt.plot(St_list,So_list,'bo',label='steer')
	plt.xlim((0,1))
	plt.ylim((0,1))
	plt.legend()
	plt.ion()
	plt.show()



