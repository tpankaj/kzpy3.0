from kzpy3.vis import *
import caffe


def show_py_image_data(data,fig=1):
	d = data[0].copy()
	d = z2o(d)
	d[:,0,0] = 1
	d[:,0,1] = 0
	for j in range(1):
	    for i in range(9):

	        mi(d[i,:,:],fig)
	        plt.pause(0.1)


solver = caffe.SGDSolver(opjh("kzpy3/caf/training/y2016/m3/RPi3/solver_kaffe_11px.prototxt"))
f=opjD('train_val_kaffe_11px_iter_2600000.caffemodel')
solver.net.copy_from(f)







for i in range(9):
	solver.net.blobs['ddata'].data[0][i,:,:] = np.random.random(np.shape(solver.net.blobs['ddata'].data[0][1,:,:]))-0.5
#solver.net.blobs['py_image_data'].data[0] = 0*solver.net.blobs['py_image_data'].data[0]
#solver.net.blobs['ddata'].data[0] = 0*solver.net.blobs['ddata'].data[0]


jitter = 3
for j in range(1000):
	ox, oy = np.random.randint(-jitter, jitter+1, 2)
	solver.net.blobs['ddata'].data[0] = np.roll(np.roll(solver.net.blobs['ddata'].data[0], ox, -1), oy, -2) # apply jitter shift
	
	solver.net.forward()#start='ddata')
	p = solver.net.blobs['ip2'].data[0,:]; p = (p*100).astype(int)/100.0; print p
#	print  solver.net.blobs['ip2'].data[:]
	solver.net.blobs['ip2'].diff[0] *= 0
	solver.net.blobs['ip2'].diff[0,3]=1
#	solver.net.blobs['conv1'].diff[0] *= 0
#	solver.net.blobs['conv1'].diff[0,30,8,15] = 1
#	solver.net.blobs['conv2'].diff[0,2,15,15] = 1
	solver.net.backward(start='ip2')
#	solver.net.backward(start='conv2')
	g = solver.net.blobs['ddata'].diff[0]
	solver.net.blobs['ddata'].data[:] += 0.005/np.abs(g).mean() * g
	
	solver.net.blobs['ddata'].data[:] = z2o(solver.net.blobs['ddata'].data[:]) - 0.5
	solver.net.blobs['ddata'].data[:] *= 0.95
	#solver.net.blobs['ddata'].data[0][i,:,:] += 0.001*(np.random.random(np.shape(solver.net.blobs['ddata'].data[0][1,:,:]))-0.5)
	solver.net.blobs['ddata'].data[0] = np.roll(np.roll(solver.net.blobs['ddata'].data[0], -ox, -1), -oy, -2) # unshift image



sample_sequence = np.load(opjD('pid.npy'))

solver.net.blobs['ddata'].data[:] = sample_sequence.copy()
jitter = 3
for j in range(100):
	solver.net.blobs['ddata'].data[0,0,:,:] = sample_sequence[0,0,:,:].copy()
	ox, oy = np.random.randint(-jitter, jitter+1, 2)
	solver.net.blobs['ddata'].data[0] = np.roll(np.roll(solver.net.blobs['ddata'].data[0], ox, -1), oy, -2) # apply jitter shift
	
	solver.net.forward()#start='ddata')
	p = solver.net.blobs['ip2'].data[0,:]; p = (p*100).astype(int)/100.0; print p
#	print  solver.net.blobs['ip2'].data[:]
	solver.net.blobs['ip2'].diff[0] *= 0
	solver.net.blobs['ip2'].diff[0,3]=1
#	solver.net.blobs['conv1'].diff[0] *= 0
#	solver.net.blobs['conv1'].diff[0,30,8,15] = 1
#	solver.net.blobs['conv2'].diff[0,2,15,15] = 1
	solver.net.backward(start='ip2')
#	solver.net.backward(start='conv2')
	g = solver.net.blobs['ddata'].diff[0]
	solver.net.blobs['ddata'].data[:] += 0.005/np.abs(g).mean() * g
	
	#solver.net.blobs['ddata'].data[:] = z2o(solver.net.blobs['ddata'].data[:]) - 0.5
	#solver.net.blobs['ddata'].data[:] *= 0.95
	#solver.net.blobs['ddata'].data[0][i,:,:] += 0.001*(np.random.random(np.shape(solver.net.blobs['ddata'].data[0][1,:,:]))-0.5)
	solver.net.blobs['ddata'].data[0] = np.roll(np.roll(solver.net.blobs['ddata'].data[0], -ox, -1), -oy, -2) # unshift image








show_py_image_data(solver.net.blobs['py_image_data'].data,'py_image_data')

show_py_image_data(solver.net.blobs['conv1'].data,'conv1')



"""
scp kzipser@redwood2.dyn.berkeley.edu:'scratch/2016/2/16/caffe/models/from_mnist/original_with_accuracy_11px/train_val_kaffe_11px_iter_2600000.caffemodel' ~/Desktop
train_val_kaffe_11px_iter_2600000.caffemodel

for 100000, percent correct = 45.3%
for 900000, percent correct = 48.1%
for 2600000, percent correct = 51.4%
chance = 14.2%
"""
n = 2000
n_correct = 0
for i in range(n):
	print i
	solver.net.forward()
	if solver.net.blobs['ip2'].data[0].argmax(axis=0) == solver.net.blobs['py_target_data'].data[0].argmax(axis=0):
		n_correct += 1
print(d2s('percent correct =',n_correct,'/',n,'chance =',int(1/7.0*n),'/',n))
