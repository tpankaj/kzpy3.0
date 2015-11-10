from kzpy3.utils import *
import nibabel as nib

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




##### local functions ######

def load_func_runs(func_runs_mc_path,dic,nii_files=['mean_func.nii.gz','mask.nii.gz']):
	'''
	I'm not sure if this is a top-level function or not.
	nii_files = ['filtered_func_data.nii.gz','mean_func.nii.gz','mask.nii.gz']
	'''
	feat_paths = []
	for rp in run_paths(func_runs_mc_path):
		fp = feat_path(rp)
		print(fp)
		load_feat_dir(fp,dic,nii_files)
		feat_paths.append(fp)
	return feat_paths

def create_and_save_session_consensus_mask(func_runs_mc_path, dic, dst_path, ref_nii_name='20150620_110252mbboldmb620mmAPPSNs003a001'):
	'''
	As it stands, this is only valid if the ref_nii_name is in the same session, although this is only for the header and affine, which are not
	necessarily important. We could also select the first mask of the session and use its header, for example.
	'''
	consensus_mask = get_consensus_mask(func_runs_mc_path,dic)
	ref_mask_header = dic[select_keys(dic,[':header','mask','/'+ref_nii_name])[0]]
	ref_mask_affine = dic[select_keys(dic,[':affine','mask','/'+ref_nii_name])[0]]
	consensus_mask_img = nib.Nifti1Image(consensus_mask, ref_mask_affine, ref_mask_header)
	os.system('mkdir -p ' + dst_path)
	nib.save(consensus_mask_img, opj(dst_path,'consensus_mask.nii.gz'))

def load_stats_dir(path,dic,include_averages=False):
	'''
	The stats dir should contain the consensus mask, so this function can be used to load the consensus mask into the dic.
	'''
	ignore,d_lst = dir_as_dic_and_list(path)
	print(d_lst)
	for nf in d_lst:
		if '.nii.gz' in nf:
			if np.logical_xor(np.logical_and('average' in nf,include_averages),'average' not in nf):
				print('load as .nii.gz: ' + nf)
				nfp = opj(path,nf)
				nii = nib.load(nfp)
				dic[nfp+':header'] = nii.get_header()
				dic[nfp+':data'] = nii.get_data()
				dic[nfp+':affine'] = nii.get_affine()
		elif '.npy' in nf:
			print('load as .npy: ' + nf)
			nfp = opj(path,nf)
			dic[nfp+':'+nf.strip('.npy')] = np.load(nfp)
		else:
			os.sys.exit('Error, unknown file type: ' + nf)

def get_run_averages_and_r_volume(consensus_mask,dic,experiment_specifier='Wedge_annulus/sequence1',session_specifier='',dst_path='.'):
	'''
	aa1,ea1,oa1,r_volume1 = get_run_averages_and_r_volume(consensus_mask,Research,'Wedge_annulus/sequence1','','/Users/karlzipser/Desktop')
	'''
	runs=[]
	for k in dic.keys():
	    if str_contains(k,[experiment_specifier,session_specifier,'filtered_func_data',':data']):
	        runs.append(k)
	runs.sort(key=natural_keys)

	even_runs = runs[0:][::2]
	odd_runs = runs[1:][::2]

	oa = get_runs_average(odd_runs,dic)
	ea = get_runs_average(even_runs,dic)
	aa = get_runs_average(runs,dic)
	plt.figure()
	plt.plot(oa[53,16,16,:]-np.mean(oa[53,16,16,:]))
	plt.plot(ea[53,16,16,:]-np.mean(ea[53,16,16,:]))
	plt.plot(aa[53,16,16,:]-np.mean(aa[53,16,16,:]))

	r_volume = correlate_runs([ea,oa],[consensus_mask,consensus_mask],graphics=False)

	kzpy.fMRI.vis.coronal(r_volume,6,7,7,fig=experiment_specifier)

	header = dic[runs[0].replace(':data',':header')]
	affine = dic[runs[0].replace(':data',':affine')]
	r_volume_img = nib.Nifti1Image(r_volume, affine, header)
	nib.save(r_volume_img, opj(dst_path,'r_volume.nii.gz'))

	if True:
		aa_img = nib.Nifti1Image(aa, affine, header)
		nib.save(aa_img, opj(dst_path,'all_average.nii.gz'))
		ea_img = nib.Nifti1Image(ea, affine, header)
		nib.save(ea_img, opj(dst_path,'even_avereage.nii.gz'))
		oa_img = nib.Nifti1Image(oa, affine, header)
		nib.save(oa_img, opj(dst_path,'odd_average.nii.gz'))

	return aa,ea,oa,r_volume



###################################################
##################### LOCAL FUNCTIONS #############


def run_paths(func_runs_mc_path):
	rp = glob.glob(opj(func_runs_mc_path,'*'))
	rp.sort(key=natural_keys)
	return rp

def feat_path(rp):
	fps = glob.glob(os.path.join(rp,'*.feat'))
	if len(fps) > 1:
		os.sys.exit('Error, len(fp) > 1')
	return fps[0]

def load_feat_dir(path,dic,nii_files):
	for nf in nii_files:
		nfp = opj(path,nf)
		nii = nib.load(nfp)
		dic[nfp+':header'] = nii.get_header()
		dic[nfp+':data'] = nii.get_data()
		dic[nfp+':affine'] = nii.get_affine()
		mc = opj(path,'mc/prefiltered_func_data_mcf_rel.rms')
		dic[mc] = np.loadtxt(mc)
		design_fn = opj(path,'design.fsf')
		with open(design_fn) as f:
			dic[nfp+':design'] = f.readlines()
			
def load_stat_dir(path,dic):
	ignore,d_lst = kzpy.fMRI.data.dir_as_dic_and_list(path)
	print(d_lst)
	for nf in d_lst:
		if '.nii.gz' in nf:
			print('load as .nii.gz: ' + nf)
			nfp = opj(path,nf)
			nii = nib.load(nfp)
			dic[nfp+':header'] = nii.get_header()
			dic[nfp+':data'] = nii.get_data()
			dic[nfp+':affine'] = nii.get_affine()
		elif '.npy' in nf:
			print('load as .npy: ' + nf)
			nfp = opj(path,nf)
			dic[nfp+':'+nf.strip('.npy')] = np.load(nfp)
		else:
			os.sys.exit('Error, unknown file type: ' + nf)

			



#################




def get_runs_average(list_of_run_paths,dic):
	avg = 0*dic[list_of_run_paths[0]]
	for rp in list_of_run_paths:
		avg += dic[rp]
	avg /= np.float(len(list_of_run_paths))
	return avg

def correlate_runs(vol_list,mask_list,graphics=True):
	mc1r1 = vol_list[0]
	mc1r2 = vol_list[1]
	rc1mask = mask_list[0]
	rc2mask = mask_list[1]
	maskc = rc1mask*rc2mask
	rc1 = np.zeros((106,106,60))
	ctr = 0
	for x in range(106):
		for y in range(106):
			for z in range(60):
				if maskc[x,y,z]>0:
					ctr += 1
					cc = np.corrcoef(mc1r1[x,y,z,:],mc1r2[x,y,z,:])[0,1]
					if not np.isfinite(cc):
						print((x,y,z,cc))
						with open(opj(os.path.expanduser("~"),'Desktop/correlation_errors.txt'), "a") as myfile:
							myfile.write('('+str(x)+','+str(y)+','+str(z)+')->'+str(cc)+'\t')
						#os.sys.exit('if not np.isfinite(cc):')
					else:
						rc1[x,y,z] = cc
	if graphics:
		kzpy.fMRI.vis.coronal(rc1,10,7,7,3)
		print(rc1.max())
		print(ctr)
	return rc1

def get_consensus_mask(func_runs_mc_path,dic):
	ctr = 0
	load_func_runs(func_runs_mc_path,dic,nii_files=['mask.nii.gz'])
	need_to_init = True
	for k in dic.keys():
	    if str_contains(k,[func_runs_mc_path,'mask.nii.gz',':data']):
	        if need_to_init:
	        	need_to_init = False
	        	consensus_mask = dic[k]
	        	ctr += 1
	        else:
	        	consensus_mask *= dic[k]
	        	ctr += 1
	if np.max(consensus_mask) > 1.0:
		os.sys.exit('if np.max(consensus_mask) > 1.0:')
	if np.min(consensus_mask) < 0:
		os.sys.exit('if np.max(consensus_mask) < 0:')
	print(ctr)
	return consensus_mask

#######################################################################
#######################################################################

####
"""
e.g.,
ipython
from kzpy3.fMRI.data.preprocess_part_III import *
work_path = opjD('')
to_do = ['S1_2015/2015/7/10/0/func_runs/pp_a0']
create_and_save_session_consensus_mask_wrapper(work_path,to_do)
"""


def create_and_save_session_consensus_mask_wrapper(work_path,to_do):
	"""
	e.g.,
	work_path = opjD('')
	to_do = ['S1_2015/2015/7/10/0/func_runs/pp_a0']
	"""
	Mask_Making_Dic = {}
	rootDir = opj(work_path,'Research/data/subjects')
	for dirName, subdirList, fileList in os.walk(rootDir):
		if str_contains_one(dirName, to_do):
			if not str_contains(dirName,['pp_a0/']): # i.e., we are not in a subdirectory of pp_a0
				if not str_contains(dirName,['pp_b0/']): # i.e., we are not in a subdirectory of pp_b0
					print dirName
					subject_func_runs_path = dirName
					subject_stats_path = str(dirName).replace('func_runs','stats')
					print(subject_func_runs_path,subject_stats_path)
					create_and_save_session_consensus_mask(subject_func_runs_path, Mask_Making_Dic, subject_stats_path, ref_nii_name='')

"""
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
"""



