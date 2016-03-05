"""
run "kzpy3/caf/training/y2016/m3/RPi3/train.py"
f=opjh('scratch/2016/3/RPi3/11px_MC_train_on_first_set/11px_MC_iter_4700000.caffemodel')
solver.net.copy_from('f')
safe_solver_step(solver)
test_solver(solver,200,0)
"""

import caffe
from kzpy3.vis import *

if host_name == 'redwood2':
	caffe.set_device(0)
	caffe.set_mode_gpu()
	print("************** using GPU *************")

os.chdir(home_path) # this is for the sake of the train_val.prototxt

training_path = opjh('kzpy3/caf/training/y2016/m3/RPi3')
#solver_name = 'solver_11px_scl50.prototxt'
#solver_name = 'solver_11px_scl100_RGB.prototxt'
solver_name = 'solver_11px_MC.prototxt'
def setup_solver():
	solver = caffe.SGDSolver(opj(training_path,solver_name))
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	return solver

solver = setup_solver()



"""
m = solver.net.blobs['M_py_image_data'].data
c = solver.net.blobs['C_py_image_data'].data
C = c[0,:,:,:]
C = C.transpose(1,2,0)
 C-=C.min();C/=C.max()
mi(m[0,8,:,:])
mi(c[0,1,:,:],2)
mi(C,3)

"""



def safe_solver_step(solver):
    while True:
        try:
            solver.step(10000)
        except Exception, e: 
            print e


def test_solver(solver,n,fig=100):
	St_list = []
	Ft_list = []
	Rt_list = []
	So_list = []
	Fo_list = []
	Ro_list = []
	start_t = time.time()
	for i in range(n):
		try:
			solver.net.forward()
			t = solver.net.blobs['MC_py_target_data'].data[0]
			o = solver.net.blobs['MC_ip2'].data[0]
			St_list.append(t[0])
			So_list.append(o[0])
			Ft_list.append(t[1])
			Fo_list.append(o[1])
			Rt_list.append(t[2])
			Ro_list.append(o[2])
		except Exception,e:
			print e
	print(d2s('Speed =',n/(time.time()-start_t),'trials per second.'))
	plt.figure(fig,(5,7))
	plt.clf()
	plt.plot(Ft_list,Fo_list,'gx',label='frames to turn')
	plt.plot(Rt_list,Ro_list,'rx',label='rot')
	plt.plot(St_list,So_list,'bo',label='steer')
	plt.xlim((0,1))
	plt.ylim((0,1))
	cS,cF,cR = 0,0,0
	try:
		cS = int(1000.0*np.corrcoef(St_list,So_list)[0,1])/1000.0
	except: pass
	try:
		cF = int(1000.0*np.corrcoef(Ft_list,Fo_list)[0,1])/1000.0
	except: pass
	try:
		cR = int(1000.0*np.corrcoef(Rt_list,Ro_list)[0,1])/1000.0
	except: pass
	plt.title((cS,cF,cR))
	#plt.legend()
	plt.ion()
	plt.show()
	plt.figure(100+fig,(5,7))
	plt.clf()
	a=[]
	b=[]
	for tt,oo in zip(St_list,So_list):
		if tt <0.1:
			a.append(oo)
	for tt,oo in zip(St_list,So_list):
		if tt >0.9:
			b.append(oo)
	plt.hist(a,bins=25,alpha=0.5);
	plt.hist(b,bins=25,alpha=0.5);
	plt.xlim((0,1))
	plt.title((np.median(a),np.median(b),np.median(b)-np.median(a)))
	return (St_list,So_list,Ft_list,Fo_list,Rt_list,Ro_list)





def view_M_filters(solver,fig=1):
	filters = solver.net.params['M_conv1'][0].data
	blnk = np.zeros((27,27*10))
	blnk[0,0] = -0.333/2.0
	blnk[0,1] = 0.333/2.0

	for f in range(96):
		for i in range(0,9): #(8,-1,-1):
			plt.clf()
			blnk[7:18,(1*14+7):(1*14+18)] = filters[f,i,:,:]
			mi(blnk,figure_num=fig,img_title=d2s(f))
			plt.pause(0.05)
		blnk *= 0
		blnk[0,0] = -0.333/4.0
		blnk[0,1] = 0.333/4.0
		#mi(blnk,figure_num=fig,img_title=d2s(f))
		plt.pause(0.5)

def view_C_filters(solver,fig=2):
	filters = solver.net.params['C_conv1'][0].data
	for i in range(96):
		a=filters[i,:,:,:]
		a=np.transpose(a,(1,2,0))
		a -= a.min()
		a /= a.max()
		plt.clf()
		mi(a,img_title=d2s(i))
		plt.pause(0.5)













