from kzpy3.vis import *
import caffe

def mi_diffs(solver):
	print 'py_image_data'
	mi(np.abs(solver.net.blobs['py_image_data'].diff[0,:,:,:]).mean(axis=0),'py_image_data diff')
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
		if len(l[1]) > 2:
			mi(np.abs(solver.net.blobs[l[0]].diff[0,:,:,:]).mean(axis=0),l[0]+' diff')


solver = caffe.SGDSolver(opjh("kzpy3/caf/training/y2016/m3/RPi3/solver_kaffe_11px.prototxt"))



for i in range(9):
	solver.net.blobs['ddata'].data[0][i,:,:] = np.random.random(np.shape(solver.net.blobs['ddata'].data[0][1,:,:]))-0.5

step_size = 0.333
jitter = 1
src = solver.net.blobs['py_image_data']
for j in range(10):

	ox, oy = np.random.randint(-jitter, jitter+1, 2)
	src.data[0] = np.roll(np.roll(src.data[0], ox, -1), oy, -2) # apply jitter shift

	solver.net.forward()

	solver.net.blobs['ip2'].diff[0,0]=1

	solver.net.backward()

	g = src.diff[0]
	
	src.data[:] += step_size/np.abs(g).mean() * g

	src.data[0] = np.roll(np.roll(src.data[0], -ox, -1), -oy, -2) # unshift image

	mi_diffs(solver)
	mi(src.data[0,0,:,:],'py_image_data')
	mi(g[0,:,:],'g')
	plt.pause(1)


