from kzpy3.teg7.data.preprocess_bag_data import *
from kzpy3.teg7.data.Bag_File import *
from kzpy3.misc.progress import *
from kzpy3.vis import *

i_variables = ['state','steer','motor','run_','runs','run_labels','meta_path','rgb_1to4_path','B_','left_images','right_images','unsaved_labels']

i_labels = ['out1_in2','direct','home','furtive','play','racing','multicar','campus','night','Smyth','left','notes','local','Tilden','reject_run','reject_intervals','snow','follow','only_states_1_and_6_good']
not_direct_modes = ['out1_in2','left','furtive','play','racing','follow']

i_functions = ['function_close_all_windows','function_set_plot_time_range','function_set_label','function_current_run','function_help','function_set_paths','function_list_runs','function_set_run','function_visualize_run','function_animate','function_run_loop']
for q in i_variables + i_functions + i_labels:
	exec(d2n(q,' = ',"\'",q,"\'")) # I use leading underscore because this facilitates auto completion in ipython

i_label_abbreviations = {out1_in2:'o1i2', direct:'D' ,home:'H',furtive:'Fu',play:'P',racing:'R',multicar:'M',campus:'C',night:'Ni',Smyth:'Smy',left:'Lf',notes:'N',local:'L',Tilden:'T',reject_run:'X',reject_intervals:'Xi',snow:'S',follow:'F',only_states_1_and_6_good:'1_6'}

I = {}






def function_load_hdf5(path):
	F = h5py.File(path)
	Lb = F['labels']
	S = F['segments']
	return Lb,S




def load_animate_hdf5(path,start_at_time=0):
	start_at(start_at_time)
	l,s=function_load_hdf5(path)
	img = False
	for h in range(len(s)):
		if type(img) != bool:
			img *= 0
			img += 128
			mi_or_cv2(img)
		pause(0.5)
		n = str(h)
		for i in range(len(s[n]['left'])):
			img = s[n]['left'][i]
			#print s[n][state][i]
			bar_color = [0,0,0]
			
			if s[n][state][i] == 1:
				bar_color = [0,0,255]
			elif s[n][state][i] == 6:
				bar_color = [255,0,0]
			elif s[n][state][i] == 5:
				bar_color = [255,255,0]
			elif s[n][state][i] == 7:
				bar_color = [255,0,255]
			else:
				bar_color = [0,0,0]
			if i < 2:
				smooth_steer = s[n][steer][i]
			else:
				smooth_steer = (s[n][steer][i] + 0.5*s[n][steer][i-1] + 0.25*s[n][steer][i-2])/1.75
			#print smooth_steer
			apply_rect_to_img(img,smooth_steer,0,99,bar_color,bar_color,0.9,0.1,center=True,reverse=True,horizontal=True)
			apply_rect_to_img(img,s[n][motor][i],0,99,bar_color,bar_color,0.9,0.1,center=True,reverse=True,horizontal=False)
			mi_or_cv2(img)
A5 = load_animate_hdf5

N = 30
label_segment_dic = {}
for i in range(len(run_codes)):
	run_name = run_codes[i].replace('.pkl','')
	hdf5_path = opjD('bair_car_data/hdf5')
	labels,segments = function_load_hdf5(opj(hdf5_path,'runs',run_name+'.hdf5')))
	label_segment_dic[run_name] = (labels,segments)

run_name = high_steer[0][0]
seg = high_steer[0][0]
elm = high_steer[0][0]
labels,segments = label_segment_dic[run_name]
label_dic = make_label_dic(labels[seg])
segment = segments[seg][elm:(elm+N)]


def load_hdf5_steer_hist(path,dst_path):
	print path
	unix('mkdir -p '+dst_path)
	low_steer = []
	high_steer = []
	l,s=function_load_hdf5(path)
	pb = ProgressBar(len(s))
	for h in range(len(s)):
		pb.animate(h)
		#print h
		n = str(h)
		for i in range(len(s[n]['left'])):
			if i < 2:
				smooth_steer = s[n][steer][i]
			else:
				smooth_steer = (s[n][steer][i] + 0.5*s[n][steer][i-1] + 0.25*s[n][steer][i-2])/1.75
			if smooth_steer < 43 or smooth_steer > 55:
				high_steer.append([h,i,int(round(smooth_steer))])
			else:
				low_steer.append([h,i,int(round(smooth_steer))])
	pb.animate(h)
	assert(len(high_steer)>0)
	assert(len(low_steer)>0)

	save_obj(high_steer,opj(dst_path,fname(path).replace('hdf5','high_steer.pkl')))
	save_obj(low_steer,opj(dst_path,fname(path).replace('hdf5','low_steer.pkl')))
