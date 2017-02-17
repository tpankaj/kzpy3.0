from kzpy3.teg7.data.preprocess_bag_data import *
from kzpy3.teg7.data.Bag_File import *
from kzpy3.misc.progress import *
from kzpy3.vis import *

"""
Interactive data viewer for model car project.

Expects to find ~/Desktop/bair_car_data/ by default.

Change path with SP(), i.e., function_set_paths()

e.g., in ipython type:

from kzpy3.teg7.interactive import *

or from command line type:

python kzpy3/teg7/interactive.py

Then type:

VR()

This will visualize run data.

Type:

AR(600,610)

This will animate 10s of data. Note, frames that are not considered data are in grayscale.

Type:

LR()

to list runs. The first number is simply a count (starting with 0), the second number
is the number of bag files in the run. A bag file is 1GB of raw data (much less here)
and take up about 30s, although this varies with image complexity.

To choose a new run (say, run 53), type:

SR(53)
VR()

Note that the prompt on the command line lists the current run. Note that run 0 is selected by default.

Now try:

AR(900,920)

This will show going from non-data to data.

Note, sometimes there is a gap in the frames, as in this example.
The program will report this and pause during this time.
Using the TX1 dev. board cleans this up dramatically.
"""

i_variables = ['run_','runs','run_labels','meta_path','rgb_1to4_path','B_','left_images']
#i_functions = ['HE','SP','LR','SR','VR','AR','RL']
i_functions = ['function_current_run','function_help','function_set_paths','function_list_runs','function_set_run','function_visualize_run','function_animate','function_run_loop']
for q in i_variables + i_functions:
	exec(d2n(q,' = ',"\'",q,"\'")) # I use leading underscore because this facilitates auto completion in ipython



I = {}
   


run_labels_path = opjD('bair_car_data','run_labels.pkl')


def function_help(q=None):
	"""
	function_help(q=None)
			HE
			get help.
	"""
	cprint('INTERACTIVE FUNCTIONS:')
	for f in i_functions:
		exec('print('+f+'.__doc__)')
	if q == None:
		cprint('INTERACTIVE VARIABLES:')
		tab_list_print(i_variables)

#I[help] = function_help
HE = function_help




def function_set_paths(p=opjD('bair_car_data')):
	"""
	function_set_paths(p=opjD('bair_car_data'))
		SP
	"""
	global I
	I[meta_path] = opj(p,'meta_states_1_5_6_7_good')
	I[rgb_1to4_path] = opj(p,'rgb_1to4')
	I[runs] = sgg(opj(I[meta_path],'*'))
	for j in range(len(I[runs])):
		I[runs][j] = fname(I[runs][j])
	I[run_] = I[runs][0]
	cprint('meta_path = '+I[meta_path])
#I[set_paths] = function_set_paths
SP = function_set_paths
SP()
#I[set_paths]()




def function_current_run(r=I[run_]):
	"""
	function_current_run()
		CR
	"""
	n = len(gg(opj(I[rgb_1to4_path],r,'*.bag.pkl')))
	cprint(d2n('[',n,'] ',r))
	state_hist = np.zeros(8)
	L=I[B_]['left_image_bound_to_data']
	for l in L:
		state_hist[int(L[l]['state'])]+=1
	state_hist /= state_hist.sum()
	state_percent = []
	for i in range(0,8):
		s = state_hist[i]
		state_percent.append(int(100*s))
	print(d2s('State percentges:',state_percent[1:8]))
CR = function_current_run




def function_list_runs():
	"""
	function_list_runs()
		LR
	"""
	try:
		I[run_labels_] = load_obj(run_labels_path)
	except:
		cprint('Unable to load run_labels!!!!!')
	cprint(I[meta_path])
	for j in range(len(I[runs])):
		r = I[runs][j]
		n = len(gg(opj(I[rgb_1to4_path],r,'*.bag.pkl')))
		cprint(d2n(j,'[',n,'] ',r))
	print('')
#I[list_runs] = function_list_runs
LR = function_list_runs
LR()
#I[list_runs]()



def function_set_run(j):
	"""
	function_set_run()
		SR
	"""
	global I
	I[run_] = I[runs][j]
	cprint(run_ + ' = ' + I[run_])
	Bag_Folder_filename = gg(opj(I[meta_path],I[run_],'Bag_Folder*'))[0]
	B = load_obj(Bag_Folder_filename)
	I[B_] = B
	CR()
#I[set_run] = function_set_run
SR = function_set_run
SR(0)



def function_visualize_run(do_load_images=True):
	"""
	function_visualize_run()
		VR
	"""
	
	global I
	r = I[run_]
	Bag_Folder_filename = gg(opj(I[meta_path],r,'Bag_Folder*'))[0]
	B = load_obj(Bag_Folder_filename)
	I[B_] = B
	CR()
	ts = np.array(B['data']['raw_timestamps'])
	tsZero = ts - ts[0]
	dts = B['data']['raw_timestamp_deltas']
	dts_hist = []
	gZero = np.array(B['data']['good_start_timestamps'])
	gZero -= ts[0]

	for j in range(len(dts)):
		dt = dts[j]
		if dt > 0.3:
			dt = 0.3
		dts_hist.append(dt)

	figure(r+' stats',figsize=(7,7))
	clf()
	plt.subplot(5,1,1)
	plt.ylim(-1,8)
	plt.xlim(tsZero[0],tsZero[-1])
	plt.ylabel('state')
	plot(gZero,0.0*array(B['data']['good_start_timestamps']),'gx')
	plot(tsZero,B['data']['state'],'k')
	
	plt.subplot(5,1,2)
	plt.ylim(-5,104)
	plt.xlim(tsZero[0],tsZero[-1])
	plt.ylabel('steer(r) and motor(b)')
	plot(gZero,49+0.0*array(B['data']['good_start_timestamps']),'gx')
	plot(tsZero,B['data']['steer'],'r')
	plot(tsZero,B['data']['motor'],'b')

	plt.subplot(5,1,3)
	plt.xlim(tsZero[0],tsZero[-1])
	plt.ylabel('frame intervals')
	plot(gZero,0.0*array(B['data']['good_start_timestamps']),'gx')
	plot(tsZero,dts)
	plt.ylim(0,0.3)

	plt.subplot(5,1,4)
	plt.xlim(tsZero[0],tsZero[-1])
	plot(gZero,0.0*array(B['data']['good_start_timestamps']),'gx')
	plt.ylabel('state one steps')
	plot(tsZero,array(B['data']['state_one_steps']),'k-')
	plt.ylim(0,500)

	plt.subplot(5,2,9)
	plt.ylabel('frame intervals')
	plt.hist(dts_hist,bins=100)
	plt.xlim(0,0.3)
	plt.pause(0.01)

	if do_load_images:
		left_images_ = {}
		bag_paths = sgg(opj(I[rgb_1to4_path],r,'*.bag.pkl'))
		n = len(bag_paths)
		pb = ProgressBar(n)
		j =  0
		cprint('Loading images...')
		for b in bag_paths:
			pb.animate(j); j+=1
			bag_img_dic = load_images(b,color_mode="rgb8",include_flip=False)
			for t in bag_img_dic['left'].keys():
				left_images_[t] = bag_img_dic['left'][t]
		pb.animate(n); print('')
		I[left_images] = left_images_

		preview_fig = r+' previews'


		figure(preview_fig)
		clf()

		N = 7
		T0 = B['data']['raw_timestamps'][0]
		Tn1 = B['data']['raw_timestamps'][-1]
		dT = (Tn1-T0)/N**2
		img_title = d2s('total time =',dp((Tn1-T0)/60.0,1),'minutes')
		ctr = 0
		for t in B['data']['raw_timestamps']:
			if t > T0 + ctr * dT:
				if t in left_images_:
					ctr += 1
					mi(left_images_[t],preview_fig,[N,N,ctr],do_clf=False)
					if ctr == N/2:
						plt.title(img_title)


#I[visualize_run] = function_visualize_run
VR = function_visualize_run




def function_animate(t0,t1):
	"""
	function_animate(t0,t1)
		AR
	"""
	CR()
	dT = t1 - t0
	assert(dT>0)
	B = I[B_]
	T0 = t0 + B['data']['raw_timestamps'][0]
	ctr = 0
	for t in B['data']['raw_timestamps']:
		if t >= T0:
			if t < T0 + dT:
				rdt = B['data']['raw_timestamp_deltas'][ctr]
				if rdt > 0.1:
					cprint(d2s('Delay between frames =',rdt),'yellow','on_red')
					plt.pause(rdt)
				#mi(left_images[t],preview_fig,[N,N,5],do_clf=False)
				#pause(0.0001)
				img = I[left_images][t]
				if t not in I[B_]['good_timestamps_to_raw_timestamps_indicies__dic']:
					img[:,:,0] = img[:,:,1]
					img[:,:,2] = img[:,:,1]
				cv2.imshow('video',cv2.cvtColor(img,cv2.COLOR_RGB2BGR))
				if cv2.waitKey(30) & 0xFF == ord('q'):
					pass
		ctr += 1

#I[animate] = function_animate
AR = function_animate



def function_run_loop():
	"""
	function_run_loop()
		RL
	"""
	print('')
	while True:
		try:
			CR()
			command = raw_input(I[run_] + ' >> ')
			if command in ['q','quit','outta-here!']:
				break
			eval(command)
		except Exception as e:
			cprint("********** Exception ***********************",'red')
			print(e.message, e.args)




RL = function_run_loop

if __name__ == '__main__':
	pass#RL()