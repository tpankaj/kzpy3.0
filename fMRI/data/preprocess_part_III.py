from kzpy3.utils import *
"""
9 November 2015

This module provides coninues preprocessing from module preprocess_part_I_and_II.



Part III: processing stats (masks, r_volumes, averages)

Up to now, run data have been preprocessed with FEAT so that they are in usable form, and linked together
in the experiments folder to be easily accessible. Now the goal is to do processing that brings
separate runs.

"mask"s are needed to define what part of the volumns are valid, taking into consideration that this
is not identical for each run. Thus, consensus masks are created.

"r_volumes" (brain volumes that contain cross-run correlation values) are to be found. These are very
useful in finding what voxels code information that is consistenly relevant to the experiment performed
in a given set of runs.

average volumes combine data from separate runs.

"""

#######################################################################################################
############### PART III: stats (masks, r_volumes, averages) #####
#
'''
work_path = '/Volumes/30June2015_4TB_fMRI_data_drive/Desktop'
to_do = [	'S1_2014/2015/6/20/0/func_runs/pp_a0']
'''
if False:
	Mask_Making_Dic = {}
	#subject_func_runs_paths = []
	#subject_stats_paths = []
	rootDir = opj(work_path,'Research/data/subjects')
	for dirName, subdirList, fileList in os.walk(rootDir):
		if str_contains_one(dirName, to_do):
			if not str_contains(dirName,['pp_a0/']):
				if not str_contains(dirName,['pp_b0/']):
					print dirName
					subject_func_runs_path = dirName
					subject_stats_path = str(dirName).replace('func_runs','stats')
					print(subject_func_runs_path,subject_stats_path)
					kzpy.fMRI.data.check_data.create_and_save_session_consensus_mask(subject_func_runs_path, Mask_Making_Dic, subject_stats_path, ref_nii_name='')

import re
p1 = re.compile('\S*subjects')
p2 = re.compile('\S*func_runs')
p3 = re.compile('\S*stats')
def extract_session_from_func_run_path(path_str):
	session_str = path_str[p1.match(path_str).span()[1]+1:]
	session_str = session_str[:(p2.match(session_str).span()[1]-10)]
	return session_str
def extract_session_from_stats_path(path_str):
	session_str = path_str[p1.match(path_str).span()[1]+1:]
	session_str = session_str[:(p3.match(session_str).span()[1]+6)]
	return session_str


if False:
	to_do_func_runs = [	'S7_2015/2015/7/13/0/func_runs/pp_b0']
	to_do_stats = [	'S7_2015/2015/7/13/0/stats/pp_b0']
	experiment_func_runs_paths = []
	subject_stats_paths = []
	rootDir = opj(work_path,'Research/data/experiments')
	for dirName, subdirList, fileList in os.walk(rootDir):
		if str_contains(dirName, to_do_func_runs):#['func_runs/pp_']):
			experiment_func_runs_paths.append(dirName)
	rootDir = opj(work_path,'Research/data/subjects')
	for dirName, subdirList, fileList in os.walk(rootDir):
		if str_contains(dirName, to_do_stats):#['stats/pp_']):
			subject_stats_paths.append(dirName)
	
	All_subject_stats_Dic = {}
	for s in subject_stats_paths:
		kzpy.fMRI.data.check_data.load_stats_dir(s,All_subject_stats_Dic)
	experiment_func_runs_paths.sort(key=kzpy.utils.natural_keys)
	for f in experiment_func_runs_paths:
		Func_runs_Dic = {}
		session_str = extract_session_from_func_run_path(f)
		cm = All_subject_stats_Dic[kzpy.utils.select_keys(All_subject_stats_Dic,[session_str,'consensus_mask.nii.gz:data'])[0]]
		kzpy.fMRI.data.check_data.load_func_runs(f,Func_runs_Dic,['filtered_func_data.nii.gz','mean_func.nii.gz','mask.nii.gz'])
		dst_path = f.replace('func_runs','stats')
		print f
		print dst_path
		os.system('mkdir -p ' + dst_path)
		with open(opj(os.path.expanduser("~"),'Desktop/correlation_errors.txt'), "a") as myfile:
							myfile.write('\n'+f+'\n')
		kzpy.fMRI.data.check_data.get_run_averages_and_r_volume(cm,Func_runs_Dic,'','',dst_path)
#
#########################################################################################################
################### PART IV: average r_volumes for Wedge_annulus, and sorted xyz list ###################
#
if False:
	r_volume_paths = []
	rootDir = opj(work_path,'Research/data/experiments')
	for dirName, subdirList, fileList in os.walk(rootDir):
		if str_contains(dirName, ['Wedge_annulus','stats/pp_']):
			r_volume_paths.append(dirName+'/r_volume.nii.gz')
	subject_stats_paths = []
	rootDir = opj(work_path,'Research/data/subjects')
	for dirName, subdirList, fileList in os.walk(rootDir):
		if str_contains(dirName, ['stats/pp_']):
			subject_stats_paths.append(dirName)
	for ssp in subject_stats_paths:
		print('subject_stats_paths=' + ssp)
		r_vols = []
		for r in r_volume_paths:
			if extract_session_from_stats_path(ssp) in r:
				print('\t'+r)
				nii = nib.load(r)
				img = nii.get_data()
				r_vols.append(img)
		if len(r_vols)>0:
			r_vols = np.array(r_vols)
			print(np.shape(r_vols))
			r_vol_avg = np.mean(r_vols,axis=0)
			print(np.shape(r_vol_avg))
			header = nii.get_header()
			affine = nii.get_affine()
			r_vol_avg_img = nib.Nifti1Image(r_vol_avg, affine, header)
			nib.save(r_vol_avg_img, opj(ssp,'r_volume.Wedge_annulus.nii.gz'))

			r_list = []
			xyz_list = []
			r_sorted_list = []
			r_sorted_xyz_list = []
			for x in range(np.shape(r_vol_avg)[0]):
				for y in range(np.shape(r_vol_avg)[1]):
					for z in range(np.shape(r_vol_avg)[2]):
						r_list.append(r_vol_avg[x,y,z])
						xyz_list.append([x,y,z])
			sorted_r_list_indicies = np.argsort(np.array(r_list))
			for i in sorted_r_list_indicies:
				r_sorted_xyz_list.append(xyz_list[i])
			np.save(opj(ssp,'r_sorted_xyz_list.Wedge_annulus.npy'),r_sorted_xyz_list)
# 
#######################################################################################################