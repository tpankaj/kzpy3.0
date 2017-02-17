import caffe
from kzpy3.vis import *
os.chdir(home_path) # this is for the sake of the train_val.prototxt

########################################################
#          SETUP SECTION
#
solver_file_path = opjh("kzpy3/caf6/z3_start/solver.prototxt")
#
########################################################

def setup_solver():
	solver = caffe.SGDSolver(solver_file_path)
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	return solver

solver = setup_solver()
weights_file_path = opjD('z3_start')
#weights_file_path = '/home/karlzipser/Desktop/z2_color/z2_color_0_a_iter_11900000.caffemodel'
weights_file_path = most_recent_file_in_folder(weights_file_path,['z3_start','caffemodel'])
solver.net.copy_from(weights_file_path)
plt.ion()
figure('conv1',figsize=(1.5,4))
for n in range(96):
	width = 11
	img = np.zeros((2*width+7,2*width+7,3))
	for c in range(3):
		img[2:width+2,2:width+2,c] = solver.net.params['conv1'][0].data[n,0+4*c,:,:]
		img[2:width+2,-(width+2):-2,c] = solver.net.params['conv1'][0].data[n,2+4*c,:,:]
		img[-(width+2):-2,2:width+2,c] = solver.net.params['conv1'][0].data[n,1+4*c,:,:]
		img[-(width+2):-2,-(width+2):-2,c] = solver.net.params['conv1'][0].data[n,3+4*c,:,:]

	mi(z2o(img),'conv1',img_title=d2s('conv1 channel',n))
	imsave(opjD('temp',d2n(n,'.png')),img)
	if n == 0:
		pause(5)
	plt.pause(1)

