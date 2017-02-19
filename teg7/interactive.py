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

i_variables = ['steer','motor','run_','runs','run_labels','meta_path','rgb_1to4_path','B_','left_images','right_images','unsaved_labels']

i_labels = ['play','racing','multicar','campus','night','Smyth','left','notes','local','Tilden','reject_run','reject_intervals','snow','follow','only_states_1_and_6_good']

i_functions = ['function_close_all_windows','function_set_plot_time_range','function_set_label','function_current_run','function_help','function_set_paths','function_list_runs','function_set_run','function_visualize_run','function_animate','function_run_loop']
for q in i_variables + i_functions + i_labels:
	exec(d2n(q,' = ',"\'",q,"\'")) # I use leading underscore because this facilitates auto completion in ipython

i_label_abbreviations = {play:'P',racing:'R',multicar:'M',campus:'C',night:'Ni',Smyth:'Smy',left:'Lf',notes:'N',local:'L',Tilden:'T',reject_run:'X',reject_intervals:'Xi',snow:'S',follow:'F',only_states_1_and_6_good:'1_6'}

I = {}

I[unsaved_labels] = False





def function_close_all_windows():
	plt.close('all')
CA = function_close_all_windows



def function_help():
	"""
	function_help(q=None)
			HE
			get help.
	"""
	cprint('INTERACTIVE FUNCTIONS:')
	for f in i_functions:
		exec('print('+f+'.__doc__)')
	cprint('INTERACTIVE VARIABLES:')
	tab_list_print(i_variables)
	cprint('\nINTERACTIVE LABELS:')
	tab_list_print(i_labels)
HE = function_help




def blank_labels():
	l = {}
	l[local] = False
	l[Tilden] = False
	l[reject_run] = False
	l[reject_intervals] = False
	l[snow] = False
	l[follow] = False
	l[only_states_1_and_6_good] = False
	return l




def function_set_paths(p=opjD('bair_car_data')):
	"""
	function_set_paths(p=opjD('bair_car_data'))
		SP
	"""
	global I
	I[meta_path] = opj(p,'meta_states_1_6_good')
	I[rgb_1to4_path] = opj(p,'rgb_1to4')
	I[runs] = sgg(opj(I[meta_path],'*'))
	for j in range(len(I[runs])):
		I[runs][j] = fname(I[runs][j])
	I[run_] = I[runs][0]
	cprint('meta_path = '+I[meta_path])
SP = function_set_paths
SP()





def function_current_run():
	"""
	function_current_run()
		CR
	"""
	r=I[run_]
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
	print(I[run_labels][r])
CR = function_current_run




def function_list_runs(rng=None):
	"""
	function_list_runs()
		LR
	"""
	cprint(I[meta_path])
	try:
		run_labels_path = most_recent_file_in_folder(opjD('bair_car_data','run_labels'),['run_labels'])
		I[run_labels] = load_obj(run_labels_path)
	except:
		cprint('Unable to load run_labels!!!!! Initalizing to empty dict')
		I[run_labels] = {}
	if rng == None:
		rng = range(len(I[runs]))
	for j in rng:
		r = I[runs][j]
		if r not in I[run_labels]:
			I[run_labels][r] = blank_labels()
		n = len(gg(opj(I[rgb_1to4_path],r,'*.bag.pkl')))
		labels_str = ""
		ks = sorted(I[run_labels][r])
		for k in ks:
			if I[run_labels][r][k] != False:
				labels_str += d2n(i_label_abbreviations[k],':',I[run_labels][r][k],' ')
		cprint(d2n(j,'[',n,'] ',r,'\t',labels_str))
	
LR = function_list_runs
LR()




def function_set_label(k,v=True):
	"""
	function_set_label(k,v)
		SL
	"""
	if not I[run_] in I[run_labels]:
		I[run_labels][I[run_]] = {}
	I[run_labels][I[run_]][k] = v
	I[unsaved_labels] = True
	if I[unsaved_labels]:
		save_obj(I[run_labels],opjD('bair_car_data','run_labels','run_labels_'+time_str()+'.pkl'))
		I[unsaved_labels] = False
SL = function_set_label



def function_set_run(j):
	"""
	function_set_run()
		SR
	"""
	global I
	I[run_] = I[runs][j]
	#cprint(run_ + ' = ' + I[run_])
	Bag_Folder_filename = gg(opj(I[meta_path],I[run_],'Bag_Folder*'))[0]
	B = load_obj(Bag_Folder_filename)
	I[B_] = B
	CR()
SR = function_set_run
SR(0)



def function_set_plot_time_range(t0=-999,t1=-999):
	"""
	function_set_plot_time_range
		ST
	"""
	r = I[run_]
	B = I[B_]
	ts = np.array(B['data']['raw_timestamps'])
	tsZero = ts - ts[0]
	if t0 < 0:
		t0 = tsZero[0]
		t1 = tsZero[-1]
	figure(r+' stats')
	plt.subplot(5,1,1)
	plt.xlim(t0,t1)
	plt.xlim(t0,t1)
	plt.subplot(5,1,2)
	plt.xlim(t0,t1)
	plt.subplot(5,1,3)
	plt.xlim(t0,t1)
	plt.subplot(5,1,4)
	plt.xlim(t0,t1)
ST = function_set_plot_time_range



def function_visualize_run(do_load_images=True):
	"""
	function_visualize_run()
		VR
	"""
	
	global I
	r = I[run_]
	#Bag_Folder_filename = gg(opj(I[meta_path],r,'Bag_Folder*'))[0]
	#B = load_obj(Bag_Folder_filename)
	#I[B_] = B
	B = I[B_]
	L = B['left_image_bound_to_data']
	if I[B_] == None:
		cprint('ERROR, first neet to set run (SR)')
		return
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

	figure(r+' stats',figsize=(7,8))
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
	#plt.ylim(0,500)

	plt.subplot(5,2,9)
	plt.ylabel('frame intervals')
	bins=plt.hist(dts_hist,bins=100)
	plt.xlim(0,0.3)
	plt.ylim(0,0.001*bins[0].max())
	plt.pause(0.01)

	if do_load_images:
		left_images_ = {}
		right_images_ = {}
		steer_ = {}
		motor_ = {}
		bag_paths = sgg(opj(I[rgb_1to4_path],r,'*.bag.pkl'))
		n = len(bag_paths)
		pb = ProgressBar(n)
		j =  0
		cprint('Loading images...')
		for b in bag_paths:
			pb.animate(j); j+=1
			bag_img_dic = load_images(b,color_mode="rgb8",include_flip=False)
			for t in bag_img_dic['left'].keys():
				#print t
				if t in L:
					steer_[t] = L[t]['steer']
					motor_[t] = L[t]['motor']
					rt = L[t]['right_image']
					if rt in bag_img_dic['right']:
						left_images_[t] = bag_img_dic['left'][t]
						right_images_[t] = bag_img_dic['right'][rt]
					else:
						pass
						#print "rt not in right"
				else:
					pass
					#print "t not in left"

		pb.animate(n); print('')
		I[left_images] = left_images_
		I[right_images] = right_images_
		I[steer] = steer_
		I[motor] = motor_
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
	s_timer = Timer(1)

	state_one_g_t_zero_dict = {}
	for i in range(len(B['data']['raw_timestamps'])):
		rt = B['data']['raw_timestamps'][i]
		state_one_g_t_zero_dict[rt] = B['data']['state_one_steps'][i]
		#print d2s(rt,state_one_g_t_zero_dict[rt])


	for t in B['data']['raw_timestamps']:
		if t >= T0:
			if s_timer.check():
				print(dp(t-T0+t0,0))
				s_timer.reset()
			if t < T0 + dT:
				rdt = B['data']['raw_timestamp_deltas'][ctr]
				if rdt > 0.1:
					cprint(d2s('Delay between frames =',rdt),'yellow','on_red')
					plt.pause(rdt)
				#mi(left_images[t],preview_fig,[N,N,5],do_clf=False)
				#pause(0.0001)
				img = I[left_images][t]
				#print state_one_g_t_zero_dict[t]
				if state_one_g_t_zero_dict[t] < 1:#t not in B['good_timestamps_to_raw_timestamps_indicies__dic']:
					#img[:,:,0] = img[:,:,1]
					#img[:,:,2] = img[:,:,1]
					img[-10:,:,0] = 255
					img[-10:,:,1:2] = 0
				cv2.imshow('video',cv2.cvtColor(img,cv2.COLOR_RGB2BGR))
				if cv2.waitKey(30) & 0xFF == ord('q'):
					pass
		ctr += 1
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
	pass #RL()



import h5py
def save_hdf5(run_num=None):
	if run_num:
		SR(run_num)
	VR()
	min_seg_len = 30
	seg_lens = []
	B = I[B_]
	L = B['left_image_bound_to_data']
	sos=B['data']['state_one_steps']

	segment_list = []

	in_segment = False

	for i in range(len(sos)):
		t = B['data']['raw_timestamps'][i]
		if sos[i] > 0 and t in I[left_images] and t in I[right_images]:
			if not in_segment:
				in_segment = True
				segment_list.append([])
			segment_list[-1].append(B['data']['raw_timestamps'][i])
		else:
			in_segment = False


	segment_list_with_min_len = []
	for s in segment_list:
		if len(s) >= min_seg_len:
			segment_list_with_min_len.append(s)

	for s in segment_list_with_min_len:
		seg_lens.append(len(s))


	figure(d2s(I[run_],'segment lengths'))
	hist(seg_lens)

	if True:
		F = h5py.File(opjD('temp.hdf5'))
		seg = opj('segments',I[run_])
		group = F.create_group(seg) #,str(i)))
		for l in I[run_labels][I[run_]].keys():
			if I[run_labels][I[run_]][l]:
				group[l] = 1
		for i in range(len(segment_list_with_min_len)):
			segment = segment_list_with_min_len[i]
			left_image_list = []
			right_image_list = []
			steer_list = []
			motor_list = []
			for j in range(len(segment)):
				t = segment[j]
				#print t
				left_image_list.append(I[left_images][t])
				right_image_list.append(I[right_images][t])
				steer_list.append(I[steer][t])
				motor_list.append(I[motor][t])
			group[opj(str(i),'left_timestamp')] = segment
			group[opj(str(i),'left')] = np.array(left_image_list)
			group[opj(str(i),'right')] = np.array(right_image_list)
			group[opj(str(i),'steer')] = np.array(steer_list)
			group[opj(str(i),'motor')] = np.array(motor_list)

		#F.close()

