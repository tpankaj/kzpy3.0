##################################
# - my standard initialization
# note, need to:
#   ln -s ~/Google_Drive/py/kzpy2 ~/kzpy to set up use of kzpy
import os, sys
if not 'kzpy_initalized' in locals():
    kzpy_initalized = True
    sys.path.append(os.path.join(os.path.expanduser("~")))
save_images = False
if save_images:
	from kzpy3.vis import *
else:
	from kzpy.img import mi
from kzpy import *
import kzpy.img
import kzpy.fMRI.vis
import kzpy.fMRI.data
import kzpy.fMRI.data.preprocess
import kzpy.fMRI.data.check_data
import kzpy.fMRI.rf
#import kzpy.fMRI.reformat_stimuli_for_analysis
import kzpy.fMRI.utils
#import kzpy.external.pyramids
#reload(kzpy)
#reload(kzpy.img)
#reload(kzpy.fMRI.vis)
#reload(kzpy.fMRI.data)
#reload(kzpy.fMRI.data.preprocess)
#reload(kzpy.fMRI.data.check_data)
#reload(kzpy.fMRI.rf)
#reload(kzpy.fMRI.reformat_stimuli_for_analysis)
#reload(kzpy.fMRI.utils)
#reload(kzpy.external.pyramids)
#

from kzpy.img import ProgressBar
from kzpy.utils import str_contains as str_contains
from kzpy.utils import str_contains_one as str_contains_one
z2o = kzpy.utils.zeroToOneRange
from kzpy.fMRI.data.pRF import KK_getcanonicalhrf

import time
PP,FF = pylab.rcParams,'figure.figsize'
PP[FF]=(6,6)
#%matplotlib inline

print("imports complete")

##################################

########################################################
# rsync -P -rav /Volumes/30June2015_4TB_fMRI_data_drive/Desktop/ /Volumes/1July2015_fMRI_data_disk/Desktop
# rsync -P -rav --exclude '*-dcm' /Volumes/30June2015_4TB_fMRI_data_drive/Desktop/ /Volumes/25Oct2014_BKP2/Desktop
# rsync -P -rav ~/Google_Drive/py/ /Volumes/1July2015_fMRI_data_disk/py
########################################################
# ipython --pylab
# cd kzpy/fMRI/2015/7
# import do_preprocessing_8July2015
# reload(do_preprocessing_8July2015);from do_preprocessing_8July2015 import *
########################################################

#work_path = '/Volumes/30June2015_4TB_fMRI_data_drive/Desktop'
#work_path = '/Volumes/26Oct2014/Desktop'
work_path = '/Users/karlzipser/2015/12'
#######################################################################################################
################### PART I: dcm -> nii -> .feat ################
#
# - 13 July 2015, using 2014 iMac
'''
TR_s, n_TRs, n_delete_TRs, = 0.9,300,6
work_path = '/Volumes/30June2015_4TB_fMRI_data_drive/Desktop'
to_do = [['S7_2015',2015,7,13,0,'/Volumes/30June2015_4TB_fMRI_data_drive/Desktop/Research-data-subjects-S7_2015-2015-7-10-0-fsl-pp_a0/data/subjects/S7_2015/2015/7/10/0/fsl/pp_a0/20150710_180737mbboldmb620mmAPPSNs016a001.feat/mean_func.nii.gz','pp_b0','']]
run_one_in_bkg = True
'''

if False:
	# Step one: get the dicom data from a session into a chunking Research- folder
	
	for symds in to_do:
		dcm_path = symds[7]
		subject = symds[0]
		year = str(symds[1])
		month = str(symds[2])
		day = str(symds[3])
		session = str(symds[4])
		kzpy.fMRI.data.preprocess.dcm_to_Research_folders(dcm_path, work_path, subject, year, month, day, session)

if False:
	# Step two: convert dicoms of sessions to Nifti's and place in appropriate Research- folders
	kzpy.fMRI.data.preprocess.MULTI_dcm2nii(work_path, work_path, to_do, True)

if False:
	# Step three: apply feat to Nifti files, put in appropriate Reserach- folders
	#print('sleep... (to make sure dicom2nii finishes)')
	#time.sleep(5*60);
	#print('awake.')
	kzpy.fMRI.data.preprocess.MULTI_feat(work_path, work_path, to_do, TR_s, n_TRs, n_delete_TRs, run_one_in_bkg)
#
########################################################
########################################################



#######################################################################################################
################# PART II: link everthing up ###########
#	
if False:
	to_do = [	['S1_2014',[[2015,6,21,0,'pp_a0']]]]
	work_path = '/Volumes/30June2015_4TB_fMRI_data_drive/Desktop'

	kzpy.fMRI.data.preprocess.add_sessions(to_do,work_path,False)

if False:
	work_path = '/Volumes/30June2015_4TB_fMRI_data_drive/Desktop'
	#to_do = [['S7_2015',[[2015,7,13,0,'pp_b0']]]]
	# Step four: get session information into main Research folder
	# But first, make sure .mat files are placed into mat folder.
	work_path = '/Volumes/30June2015_4TB_fMRI_data_drive/Desktop'
	kzpy.fMRI.data.preprocess.add_sessions_info(to_do,work_path)

if False:
	# Step five: link functional runs
	work_path = '/Volumes/30June2015_4TB_fMRI_data_drive/Desktop'

	#to_do = [['S1_2014',[[2015,6,21,0,'pp_a0']]],
#		['S1_2014',[[2015,6,22,0,'pp_a0']]],
#		['S1_2014',[[2015,6,23,0,'pp_a0']]],
#		['S6_2015',[[2015,6,23,0,'pp_a0']]],
	
	for t in to_do:
		subject = t[0]
		print('\t'+subject)
		for ymds in t[1]:
			year = ymds[0]
			month = ymds[1]
			day = ymds[2]
			session = ymds[3]
			pp = ymds[4]
			print('\t\t'+str(year)+' '+str(month)+' '+str(day)+' '+str(session)+' '+pp)
			kzpy.fMRI.data.preprocess.link_func_runs(subject,year,month,day,session,pp,work_path)
#
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
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
###################### Part V: map receptive fields ###################################################
#
# mapping with sequences 1 & 2
if False:
	subject = 'S1_2014'
	nnn = 20000

	work_path = '/Volumes/30June2015_4TB_fMRI_data_drive/Desktop'
	import kzpy.fMRI.data.pRF
	reload(kzpy.fMRI.data.pRF)
	from kzpy.fMRI.data.pRF import *
	hrf = KK_getcanonicalhrf()
	n_TRs = 294
	TR_times = 0.9 * np.arange(0,n_TRs)
	s1,frame_5Hz_times = get_WA_mask_sequence(1,opj(work_path,'Research/'))
	sc1 = convolve_s_with_hrf(s1,frame_5Hz_times,hrf,TR_times)
	s2,frame_5Hz_times = get_WA_mask_sequence(2,opj(work_path,'Research'))
	sc2 = convolve_s_with_hrf(s2,frame_5Hz_times,hrf,TR_times)
	print('')

	r_sorted_xyz_list_paths = []
	rootDir = opj(work_path,'Research/data/subjects')
	for dirName, subdirList, fileList in os.walk(rootDir):
		if str_contains(dirName, [subject,'stats/pp_']):
			r_sorted_xyz_list_paths.append(dirName)
	for rxyz in r_sorted_xyz_list_paths:
		s = extract_session_from_stats_path(rxyz)
		sequence1_paths = []
		sequence2_paths = []
		for dirName, subdirList, fileList in os.walk(opj(work_path,'Research/data/experiments')):
			if str_contains(dirName, [s,'sequence1']):
				sequence1_paths.append(dirName+'/all_average.nii.gz')
			if str_contains(dirName, [s,'sequence2']):
				sequence2_paths.append(dirName+'/all_average.nii.gz')
		print(rxyz+'/r_sorted_xyz_list.Wedge_annulus.npy')
		print('\t'+sequence1_paths[0])
		print('\t'+sequence2_paths[0])

		r_sorted_xyz_list = np.load(rxyz+'/r_sorted_xyz_list.Wedge_annulus.npy')
		nii1=nib.load(sequence1_paths[0])
		aa1=nii1.get_data()
		nii2=nib.load(sequence2_paths[0])
		aa2=nii2.get_data()


		rf_x_vol = np.zeros((106,106,60))
		rf_y_vol = np.zeros((106,106,60))
		rf_r_vol = np.zeros((106,106,60))
		s1_peaks = {}
		s2_peaks = {}

		for i in range(6000,nnn):#len(r_sorted_xyz_list)):
			ni = -(i+1)
			xyz = tuple(r_sorted_xyz_list[ni])
			rf1,s1_peaks[xyz] = rf_peak_xy(sc1,aa1[tuple(r_sorted_xyz_list[ni])],TR_times,'aa1 ' + str(ni),False)
			rf2,s2_peaks[xyz] = rf_peak_xy(sc2,aa2[tuple(r_sorted_xyz_list[ni])],TR_times,'aa2 ' + str(ni),False)
			rf1flat=np.reshape(rf1,np.shape(rf1)[0]*np.shape(rf1)[1])
			rf2flat=np.reshape(rf2,np.shape(rf2)[0]*np.shape(rf2)[1])
			cc = np.corrcoef(rf1flat,rf2flat)[0,1]
			print((ni,xyz,s1_peaks[xyz],s2_peaks[xyz],cc))#,s2_peaks[xyz]))
			peak = (np.array(s1_peaks[xyz])+np.array(s2_peaks[xyz]))/2.0
			rf_x_vol[xyz[0],xyz[1],xyz[2]] = peak[0]
			rf_y_vol[xyz[0],xyz[1],xyz[2]] = peak[1]
			rf_r_vol[xyz[0],xyz[1],xyz[2]] = cc
			print((rf_x_vol[xyz],rf_y_vol[xyz],rf_r_vol[xyz]))

		header = nii1.get_header()
		affine = nii1.get_affine()
		rf_x_vol_img = nib.Nifti1Image(rf_x_vol, affine, header)
		nib.save(rf_x_vol_img, opj(rxyz,'rf_x_vol.Wedge_annulus.'+str(nnn)+'.nii.gz'))
		rf_y_vol_img = nib.Nifti1Image(rf_y_vol, affine, header)
		nib.save(rf_y_vol_img, opj(rxyz,'rf_y_vol.Wedge_annulus.'+str(nnn)+'.nii.gz'))
		rf_r_vol_img = nib.Nifti1Image(rf_r_vol, affine, header)
		nib.save(rf_r_vol_img, opj(rxyz,'rf_r_vol.Wedge_annulus.'+str(nnn)+'.nii.gz'))

# Mapping with sequences 1a,1b,2a & 2b
# This is a first pass, there are problems to resolve.
if False:
	subject = 'S7_2015'
	nnn = 20000

	work_path = '/Volumes/30June2015_4TB_fMRI_data_drive/Desktop'
	import kzpy.fMRI.data.pRF
	reload(kzpy.fMRI.data.pRF)
	from kzpy.fMRI.data.pRF import *
	hrf = KK_getcanonicalhrf()
	n_TRs = 294
	TR_times = 0.9 * np.arange(0,n_TRs)
	s1a,frame_5Hz_times = get_WA_mask_sequence_ab('1a',opj(work_path,'Research/'))
	sc1a = convolve_s_with_hrf(s1a,frame_5Hz_times,hrf,TR_times)
	s1b,frame_5Hz_times = get_WA_mask_sequence_ab('1b',opj(work_path,'Research/'))
	sc1b = convolve_s_with_hrf(s1b,frame_5Hz_times,hrf,TR_times)
	s2a,frame_5Hz_times = get_WA_mask_sequence_ab('2a',opj(work_path,'Research'))
	sc2a = convolve_s_with_hrf(s2a,frame_5Hz_times,hrf,TR_times)
	s2b,frame_5Hz_times = get_WA_mask_sequence_ab('2b',opj(work_path,'Research'))
	sc2b = convolve_s_with_hrf(s2a,frame_5Hz_times,hrf,TR_times)
	print('')

	r_sorted_xyz_list_paths = []
	rootDir = opj(work_path,'Research/data/subjects')
	for dirName, subdirList, fileList in os.walk(rootDir):
		if str_contains(dirName, [subject,'stats/pp_']):
			r_sorted_xyz_list_paths.append(dirName)
	for rxyz in r_sorted_xyz_list_paths:
		s = extract_session_from_stats_path(rxyz)
		sequence1a_paths = []
		sequence2a_paths = []
		sequence1b_paths = []
		sequence2b_paths = []
		for dirName, subdirList, fileList in os.walk(opj(work_path,'Research/data/experiments')):
			if str_contains(dirName, [s,'sequence1a']):
				sequence1a_paths.append(dirName+'/all_average.nii.gz')
			if str_contains(dirName, [s,'sequence2a']):
				sequence2a_paths.append(dirName+'/all_average.nii.gz')
			if str_contains(dirName, [s,'sequence1b']):
				sequence1b_paths.append(dirName+'/all_average.nii.gz')
			if str_contains(dirName, [s,'sequence2b']):
				sequence2b_paths.append(dirName+'/all_average.nii.gz')
		print(rxyz+'/r_sorted_xyz_list.Wedge_annulus.npy')
		print('\t'+sequence1a_paths[0])
		print('\t'+sequence2a_paths[0])
		print('\t'+sequence1b_paths[0])
		print('\t'+sequence2b_paths[0])

		r_sorted_xyz_list = np.load(rxyz+'/r_sorted_xyz_list.Wedge_annulus.npy')
		nii1a=nib.load(sequence1a_paths[0])
		aa1a=nii1a.get_data()
		nii2a=nib.load(sequence2a_paths[0])
		aa2a=nii2a.get_data()
		nii1b=nib.load(sequence1b_paths[0])
		aa1b=nii1b.get_data()
		nii2b=nib.load(sequence2b_paths[0])
		aa2b=nii2b.get_data()


		rf_x_vol = np.zeros((106,106,60))
		rf_y_vol = np.zeros((106,106,60))
		rf_r_vol = np.zeros((106,106,60))
		s1a_peaks = {}
		s2a_peaks = {}
		s1b_peaks = {}
		s2b_peaks = {}

		for i in range(0,nnn):#len(r_sorted_xyz_list)):
			ni = -(i+1)
			xyz = tuple(r_sorted_xyz_list[ni])
			rf1a,s1a_peaks[xyz] = rf_peak_xy(sc1a,aa1a[tuple(r_sorted_xyz_list[ni])],TR_times,'aa1a ' + str(ni),False)
			rf2a,s2a_peaks[xyz] = rf_peak_xy(sc2a,aa2a[tuple(r_sorted_xyz_list[ni])],TR_times,'aa2a ' + str(ni),False)
			rf1b,s1b_peaks[xyz] = rf_peak_xy(sc1b,aa1b[tuple(r_sorted_xyz_list[ni])],TR_times,'aa1b ' + str(ni),False)
			rf2b,s2b_peaks[xyz] = rf_peak_xy(sc2b,aa2b[tuple(r_sorted_xyz_list[ni])],TR_times,'aa2b ' + str(ni),False)
			rf1 = (rf1a+rf1b)/2.0
			rf2 = (rf2a+rf2b)/2.0
			rf = (rf1+rf2)/2.0
			rf1flat=np.reshape(rf1,np.shape(rf1)[0]*np.shape(rf1)[1])
			rf2flat=np.reshape(rf2,np.shape(rf2)[0]*np.shape(rf2)[1])
			cc = np.corrcoef(rf1flat,rf2flat)[0,1]
			print((ni,xyz,s1a_peaks[xyz],s2a_peaks[xyz],s1b_peaks[xyz],s2b_peaks[xyz],cc))#,s2_peaks[xyz]))
			peak = np.unravel_index(rf.argmax(), rf.shape)
			rf_x_vol[xyz[0],xyz[1],xyz[2]] = peak[0]
			rf_y_vol[xyz[0],xyz[1],xyz[2]] = peak[1]
			rf_r_vol[xyz[0],xyz[1],xyz[2]] = cc
			print((rf_x_vol[xyz],rf_y_vol[xyz],rf_r_vol[xyz]))

		header = nii1a.get_header()
		affine = nii1a.get_affine()
		rf_x_vol_img = nib.Nifti1Image(rf_x_vol, affine, header)
		nib.save(rf_x_vol_img, opj(rxyz,'rf_x_vol.Wedge_annulus.'+str(nnn)+'.nii.gz'))
		rf_y_vol_img = nib.Nifti1Image(rf_y_vol, affine, header)
		nib.save(rf_y_vol_img, opj(rxyz,'rf_y_vol.Wedge_annulus.'+str(nnn)+'.nii.gz'))
		rf_r_vol_img = nib.Nifti1Image(rf_r_vol, affine, header)
		nib.save(rf_r_vol_img, opj(rxyz,'rf_r_vol.Wedge_annulus.'+str(nnn)+'.nii.gz'))
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
###################### Part VI: p-imaging ###################################################
def get_activation_image(xy2p,vs,H=96,W=128):
	X,Y = H,W
	img3 = np.zeros((H,W))
	for x in range(X):
		for y in range(Y):
			v = 0.0
			j = np.int(xy2p[x,y][1][0])
			#print(j)
			v = vs[j]
			#print(v)
			img3[x,y] = v
	return img3

def get_activation_image_new(xy2p,vs,H=96,W=128,num_to_average = 'all'):
	X,Y = H,W
	img3 = np.zeros((H,W))
	if num_to_average == 'all':
		num_to_average = len(xy2p[0,0][1]) # need to insure this will be a good coordinate
	else:
		assert num_to_average > 0
		assert num_to_average <= len(xy2p[0,0][1])
	for x in range(X):
		for y in range(Y):
			v = 0.0
			for i in range(num_to_average):
				j = np.int(xy2p[x,y][1][i])
				v += vs[j]
				img3[x,y] = v/num_to_average
	return img3

def make_p_images(subject,year,month,day,session,pp,sub_experiments,conditions,experiment,num_to_average,mapping_year=False,mapping_month=False,mapping_day=False,mapping_session=False,mapping_pp=False,USE_Z_SCORING=False):
	'''
	'''
	if not mapping_year:
		mapping_year = year
	if not mapping_month:
		mapping_month = month
	if not mapping_day:
		mapping_day = day
	if not mapping_session:
		mapping_session = session
	if not mapping_pp:
		mapping_pp = pp

	USE_STD_SCORING = not USE_Z_SCORING

	print('USE_Z_SCORING = ' + str(USE_Z_SCORING))

	rf_path = opj(work_path,'Research/data/subjects',subject,str(mapping_year),str(mapping_month),str(mapping_day),str(mapping_session),'stats',mapping_pp)
	rf_x_vol_nii = nib.load(opj(rf_path,'rf_x_vol.Wedge_annulus.6000.nii.gz'))
	rf_y_vol_nii = nib.load(opj(rf_path,'rf_y_vol.Wedge_annulus.6000.nii.gz'))
	rf_r_vol_nii = nib.load(opj(rf_path,'rf_r_vol.Wedge_annulus.6000.nii.gz'))
	std1_vol_nii = nib.load(opj(work_path,'Research/data/experiments',experiment,'Wedge_annulus/sequence1/subjects',subject,str(mapping_year),str(mapping_month),str(mapping_day),str(mapping_session),'stats',mapping_pp,'all_average.nii.gz'))
	std2_vol_nii = nib.load(opj(work_path,'Research/data/experiments',experiment,'Wedge_annulus/sequence2/subjects',subject,str(mapping_year),str(mapping_month),str(mapping_day),str(mapping_session),'stats',mapping_pp,'all_average.nii.gz'))
	rf_x_vol=rf_x_vol_nii.get_data()
	rf_y_vol=rf_y_vol_nii.get_data()
	rf_r_vol=rf_r_vol_nii.get_data()
	std1_vol = std1_vol_nii.get_data()
	std2_vol = std2_vol_nii.get_data()

	for sub_ex in sub_experiments:
		for task in conditions:
			stats_path = opj(work_path,'Research/data/experiments',experiment,sub_ex,task,'subjects',subject,str(year),str(month),str(day),str(session),'stats',pp)
			nii1=nib.load(opj(stats_path,'betas.nipy_GLM.nii.gz'))
			aa1 = nii1.get_data()

			points = []
			selected_xyz = []

			for x in range(np.shape(rf_x_vol)[0]):
				for y in range(np.shape(rf_x_vol)[1]):
					for z in range(np.shape(rf_x_vol)[2]):
						if rf_r_vol[x,y,z] > 0.9:
							points.append([rf_x_vol[x,y,z],rf_y_vol[x,y,z]])
							selected_xyz.append([x,y,z])
			print(len(selected_xyz))

			xy2p,p2xys = kzpy.fMRI.rf.get_mappings(points,W=128,N=30)

			z_aa1 = 0.0*aa1



			if USE_Z_SCORING:
				for xyz in selected_xyz:
					x,y,z = xyz[0],xyz[1],xyz[2]
					sd = np.std(aa1[x,y,z,:])
					if np.isfinite(sd):
						if not sd == 0:
							z_aa1[x,y,z,:] = aa1[x,y,z,:] - np.mean(aa1[x,y,z,:])
							z_aa1[x,y,z,:] /= sd
			elif USE_STD_SCORING:
				for xyz in selected_xyz:
					x,y,z = xyz[0],xyz[1],xyz[2]
					sd = (np.std(std1_vol[x,y,z,:])+np.std(std2_vol[x,y,z,:]))/2.0#np.std(aa1[x,y,z,:])#
					if np.isfinite(sd):
						if not sd == 0:
							z_aa1[x,y,z,:] = aa1[x,y,z,:] - aa1[x,y,z,-1] # NOTE, EXPECT LAST STIMULUS TO BE THE BLANK!!!! #np.mean(aa1[x,y,z,:]) #np.mean(aa1[x,y,z,:])
							z_aa1[x,y,z,:] /= sd
			else:
				os.sys.exit('UNKNOWING SCORING')				


			p_image_png_dir = opj(stats_path,'p_images/png_std')
			p_image_npy_dir = opj(stats_path,'p_images/npy')
			os.system('mkdir -p ' + p_image_png_dir)
			os.system('mkdir -p ' + p_image_npy_dir)
			for TR in range(np.shape(aa1)[3]):
				vs = []
				for xyz in selected_xyz:
					vs.append(z_aa1[xyz[0],xyz[1],xyz[2],TR])
				img = get_activation_image_new(xy2p,vs,H=96,W=128,num_to_average=num_to_average)
				scipy.misc.imsave(opj(p_image_png_dir,str(TR)+'.png'),img)
				np.save(opj(p_image_npy_dir,str(TR)+'.npy'),img)


def img_varient(img, scale_factor, mirror_flip):
	H = np.shape(img)[0]
	W = np.shape(img)[1]
	if scale_factor == 1 and mirror_flip == False:
		#print('Do nothing.')
		return img
	scale_factor = np.float(scale_factor)
	iv = scipy.misc.imresize(img, scale_factor)
	xc,yc = np.shape(iv)[0],np.shape(iv)[1]
	xc,yc = xc/2,yc/2
	iv = iv[(xc-H/2):(xc+H/2),(yc-W/2):(yc+W/2)]
	if mirror_flip:
		iv = np.fliplr(iv)
	return iv

def z_aggressive_score_img(img,t=2.5,nt= -2.5):
	z = img - np.mean(img)
	z = z / np.std(z)
	z[z>t]=t
	z[z<= nt]= nt
	return z

z2o = kzpy.utils.zeroToOneRange

#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
###################### Part VII: GLM ###################################################

def vol_to_voxels(vol):
	print('vol_to_voxels(vol)')
	XYZT = np.shape(vol)
	mask = vol[:,:,:,0].copy()
	mask[mask>0]=1
	mask[mask<=0]=0
	n_voxels = np.sum(mask)
	n_TRs = XYZT[3]
	voxels = np.zeros((n_TRs, n_voxels))
	vox_xyzs = np.zeros((n_voxels,3))
	ctr = 0
	pb = ProgressBar(XYZT[0])
	for x in range(XYZT[0]):
		pb.animate(x+1)
		for y in range(XYZT[1]):
			for z in range(XYZT[2]):
				if mask[x,y,z]:
					voxels[:,ctr] = (vol[x,y,z,:]-np.mean(vol[x,y,z,:]))/np.std(vol[x,y,z,:])
					vox_xyzs[ctr,:] = [x,y,z]
					ctr += 1
	return voxels,vox_xyzs

def vox_list_to_vol(voxels,vox_xyzs,mask):
    XYZ = np.shape(mask)
    TRs = np.shape(voxels[:,0])[0]
    print((XYZ[0],XYZ[1],XYZ[2],TRs))
    vol = np.zeros((XYZ[0],XYZ[1],XYZ[2],TRs))
    for v in range(np.shape(vox_xyzs)[0]):
        xyz = vox_xyzs[v]
        vol[xyz[0],xyz[1],xyz[2],:] = voxels[:,v]
    return vol


def KK_visit_nipy_GLM(stats_path,stimulus_txt_path):

	stimulus_txt = np.loadtxt(stimulus_txt_path)
	n_Secs = len(stimulus_txt)
	n_TRs_all = 300
	n_images = np.int(np.max(stimulus_txt))

	stimulus_REGRESSORS = np.zeros((n_Secs, n_images))
	for s in range(n_Secs):
	    if stimulus_txt[s] > 0:
	        stimulus_REGRESSORS[s,stimulus_txt[s]-1] = 1

	hrf = KK_getcanonicalhrf()
	hrf_1Hz = hrf[::5]
	#PP[FF]=3,3
	#plt.figure('hrf_1Hz')
	#plt.plot(hrf_1Hz,'.-')
	#mi(stimulus_REGRESSORS,'stimulus_REGRESSORS')

	HRF_REG = np.zeros((n_TRs_all,n_images))
	stimulus_times = np.arange(0,n_Secs)
	TR_times = 0.9 * np.arange(0,n_TRs_all)

	for i in range(n_images):
	    r = stimulus_REGRESSORS[:,i]
	    hp = np.convolve(r, hrf_1Hz)[:(np.shape(r)[0])]
	    hp_interp = np.interp(TR_times,stimulus_times,hp)
	    HRF_REG[:,i]=hp_interp
	#PP[FF] = 5,8
	#mi(HRF_REG,'HRF_REG')

	nii = nib.load(opj(stats_path,'all_average.nii.gz'))
	data = nii.get_data()
	header = nii.get_header()
	affine = nii.get_affine()
	
	Voxels,Vox_xyzs = vol_to_voxels(data)

	# - http://nipy.org/nipy/api/generated/nipy.modalities.fmri.glm.html

	from nipy.modalities.fmri.glm import GeneralLinearModel

	n_TRs = 294
	n_voxels = np.shape(Voxels)[1]
	#n_images = 24

	DATA = Voxels

	REGRESSORS = HRF_REG.copy()[6:] # this deals with DELETE volumes

	model = GeneralLinearModel(REGRESSORS)
	model.fit(DATA)

	#mi(DATA,1,[1,1,1],'DATA ' + str(np.shape(DATA)))
	#mi(REGRESSORS,2,[1,1,1],'REGRESSORS ' + str(np.shape(REGRESSORS)))

	betas = model.get_beta()
	#mi(betas,3,[1,1,1],'betas ' + str(np.shape(betas)))

	mse = model.get_mse()
	#plt.figure('mse ' + str(np.shape(mse)))
	#plt.plot(mse)

	vol_betas = vox_list_to_vol(betas,Vox_xyzs,data[:,:,:,0].copy())

	betas_nii = nib.Nifti1Image(vol_betas, affine, header)
	nib.save(betas_nii, opj(stats_path,'betas.nipy_GLM.nii.gz'))
	

def KK_visit_Vermeer_GLM(stats_path):

	stimulus_txt = np.loadtxt('/Users/davidzipser/Google_Drive/Data/stimuli/2015/6/Vermeer_1024x768/natural_stimuli_10Hz_Fri_Jun_19_21-56-59_2015.medium_letters/stimulus.txt')
	n_Secs = len(stimulus_txt) # DANGER
	n_TRs_all = 300
	n_images = 24

	stimulus_REGRESSORS = np.zeros((n_Secs, n_images))
	for s in range(n_Secs):
	    if stimulus_txt[s] > 0:
	        stimulus_REGRESSORS[s,stimulus_txt[s]-1] = 1

	hrf = KK_getcanonicalhrf()
	hrf_1Hz = hrf[::5]
	#PP[FF]=3,3
	#plt.figure('hrf_1Hz')
	#plt.plot(hrf_1Hz,'.-')
	#mi(stimulus_REGRESSORS,'stimulus_REGRESSORS')

	HRF_REG = np.zeros((n_TRs_all,n_images))
	stimulus_times = np.arange(0,n_Secs)
	TR_times = 0.9 * np.arange(0,n_TRs_all)

	for i in range(n_images):
	    r = stimulus_REGRESSORS[:,i]
	    hp = np.convolve(r, hrf_1Hz)[:(np.shape(r)[0])]
	    hp_interp = np.interp(TR_times,stimulus_times,hp)
	    HRF_REG[:,i]=hp_interp
	#PP[FF] = 5,8
	#mi(HRF_REG,'HRF_REG')

	nii = nib.load(opj(stats_path,'all_average.nii.gz'))
	data = nii.get_data()
	header = nii.get_header()
	affine = nii.get_affine()
	
	Voxels,Vox_xyzs = vol_to_voxels(data)

	# - http://nipy.org/nipy/api/generated/nipy.modalities.fmri.glm.html

	from nipy.modalities.fmri.glm import GeneralLinearModel

	n_TRs = 294
	n_voxels = np.shape(Voxels)[1]
	n_images = 24

	DATA = Voxels

	REGRESSORS = HRF_REG.copy()[6:] # this deals with DELETE volumes

	model = GeneralLinearModel(REGRESSORS)
	model.fit(DATA)

	#mi(DATA,1,[1,1,1],'DATA ' + str(np.shape(DATA)))
	#mi(REGRESSORS,2,[1,1,1],'REGRESSORS ' + str(np.shape(REGRESSORS)))

	betas = model.get_beta()
	#mi(betas,3,[1,1,1],'betas ' + str(np.shape(betas)))

	mse = model.get_mse()
	#plt.figure('mse ' + str(np.shape(mse)))
	#plt.plot(mse)

	vol_betas = vox_list_to_vol(betas,Vox_xyzs,data[:,:,:,0].copy())

	betas_nii = nib.Nifti1Image(vol_betas, affine, header)
	nib.save(betas_nii, opj(stats_path,'betas.nipy_GLM.nii.gz'))


#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
###################### Part VIII: controlling making betas and p-images, combination of p-images ######
# Setup:
#######################################################################################################
Img_Dic = {}
Img_Dic['Vermeer'] = []
Img_Dic['Overlapping_face_place'] = []
for i in range(4):
	Img_Dic['Vermeer'].append(scipy.misc.imread(opj(work_path,'Research/stimuli/Kendrick_Kay_visit_19to26June2015/Vermeer/png',str(i)+'.png')))
Img_Dic['Kay_images'] = []
for i in range(4):
	Img_Dic['Kay_images'].append(scipy.misc.imread(opj(work_path,'Research/stimuli/Kendrick_Kay_visit_19to26June2015/Kay_images/png',str(i)+'.png')))
Img_Dic['Three_circles'] = []
for i in range(4):
	Img_Dic['Three_circles'].append(scipy.misc.imread(opj(work_path,'Research/stimuli/Kendrick_Kay_visit_19to26June2015/Three_circles/png',str(i)+'.png')))
for i in range(8):
	Img_Dic['Overlapping_face_place'].append(scipy.misc.imread(opj(work_path,'Research/stimuli/Kendrick_Kay_visit_19to26June2015/Overlapping_face_place/png',str(i)+'.png')))



Ses_Dic = {}
Ses_Dic['KZ_20'] = ('S1_2014',2015,6,20,0,'pp_a0')
Ses_Dic['KZ_21'] = ('S1_2014',2015,6,21,0,'pp_b0')
Ses_Dic['KZ_22'] = ('S1_2014',2015,6,22,0,'pp_b0')
Ses_Dic['KZ_23'] = ('S1_2014',2015,6,23,0,'pp_b0')
Ses_Dic['KZ_25'] = ('S1_2014',2015,6,25,0,'pp_a0')
Ses_Dic['KK_21'] = ('S6_2015',2015,6,21,0,'pp_a0')
Ses_Dic['KK_23'] = ('S6_2015',2015,6,23,0,'pp_b0')

Exp_Dic = {}
Exp_Dic['Vermeer0'] = (['Vermeer'],['read_letters','attend_face','attend_object','attend_space'],'Kendrick_Kay_visit_19to26June2015')
Exp_Dic['Kay_images'] = (['Kay_images'],['read_letters','attend_face','attend_object'],'Kendrick_Kay_visit_19to26June2015')
Exp_Dic['Vermeer1'] = (['Vermeer'],['read_letters','attend_figure','attend_ground','attend_skin','attend_position','attend_texture'],'Kendrick_Kay_visit_19to26June2015')
Exp_Dic['Three_circles'] = (['Three_circles'],['attend_as_directed'],'Kendrick_Kay_visit_19to26June2015')
Exp_Dic['Overlapping_face_place'] = (['Overlapping_face_place'],['attend_face','attend_place'],'Kendrick_Kay_visit_19to26June2015')

circle_ses = ['KZ_22','KZ_23','KK_23']
vermeer0_ses = ['KZ_20','KZ_21','KK_21']
vermeer1_ses = ['KZ_25']
overlap_ses = ['KZ_22','KZ_23']
kay_img_ses = ['KZ_20']

#######################################################################################################
# Control:
ex,sess = 'Vermeer0',vermeer0_ses
#ex,sess = 'Three_circles',circle_ses
#ex,sess = 'Overlapping_face_place',overlap_ses
#ex,sess = 'Kay_images',kay_img_ses
Get_Betas = False
Make_P_Images = False
Combine_P_Images = True
use_z_scoring = False
fix_mask_radius = 5
########################################################################################################

def mi_save(
    image_matrix,
    figure_num = 1,
    subplot_array = [1,1,1],
    img_title = '',
    img_xlabel = 'x',
    img_ylabel = 'y',
    cmap = 'gray',
    toolBar = True,
    do_clf = True,
    do_axis = False ):
	mi(image_matrix,
		figure_num,
		subplot_array,
		img_title,
		img_xlabel,
		img_ylabel,
		cmap,
		toolBar,
		do_clf,
		do_axis)
	if img_title == '':
		img_title = 'img'
	unix('mkdir -p '+opjD(figure_num))
	imsave(opjD(figure_num,d2f('-',img_title,subplot_array,'.png')),image_matrix)


if True: ########################################################################################################
	
	if not save_images:
		mi_save = mi

	SES = {}
	for ses in sess:
		SES[ses]={}
		subject,year,month,day,session,pp = Ses_Dic[ses]
		sub_experiments,conditions,experiment = Exp_Dic[ex]
		mapping_year,mapping_month,mapping_day,mapping_session,mapping_pp = False,False,False,False,False
		if ses == 'KK_23':
			mapping_year,mapping_month,mapping_day,mapping_session,mapping_pp = (2015,6,21,0,'pp_a0')
		#######################################################################################################
		if Get_Betas: # get betas

			for task in conditions: #['attend_figure','attend_ground','attend_position','attend_skin','attend_texture','read_letters']:#['attend_face','attend_object','attend_space','read_letters']:
				stats_path = opj(work_path,'Research/data/experiments',experiment,sub_experiments[0],task,'subjects',subject,str(year),str(month),str(day),str(session),'stats',pp)
				stimulus_txt_path = opj(work_path,'Research/stimuli',experiment,sub_experiments[0],'stimulus.txt')
				KK_visit_nipy_GLM(stats_path,stimulus_txt_path)
		#######################################################################################################
		if Make_P_Images:
			make_p_images(subject,year,month,day,session,pp,sub_experiments,conditions,experiment,30,mapping_year,mapping_month,mapping_day,mapping_session,mapping_pp,use_z_scoring)
		#######################################################################################################
		if Combine_P_Images:

			if sub_experiments[0] == 'Vermeer' or sub_experiments[0] == 'Kay_images':
				mirror_flip = [False,True]
				scale_factor = [1.4,1.2,1.0]
				n_images = 4
				for i in range(len(Img_Dic[sub_experiments[0]])):
					mi_save(img_varient(Img_Dic[sub_experiments[0]][i],scale_factor[0],False),opj(subject,sub_experiments[0],str(month),str(day)),[n_images+1,1+len(conditions),1+i*(1+len(conditions))],'')	
					mi_save(img_varient(Img_Dic[sub_experiments[0]][i],scale_factor[0],False),opj(subject,sub_experiments[0],str(month),str(day),'YB'),[n_images+1,1+len(conditions),1+i*(1+len(conditions))],'')	
				
				task_ctr = 0
				for task in conditions:
					task_ctr+=1
					ctr = 0
					for i in range(n_images):
						avg_img = np.zeros((96,128))
						for j in range(len(mirror_flip)):
							for k in range(len(scale_factor)):
								stats_path = opj(work_path,'Research/data/experiments',experiment,sub_experiments[0],task,'subjects',subject,str(year),str(month),str(day),str(session),'stats',pp)
								img1 = scipy.misc.imread(opj(stats_path,'p_images/png_std/'+str(ctr)+'.png'))#  '/Users/davidzipser/Desktop/Pictures_Desktop/new_'+task_str+'/'+str(ctr)+'.png')
								img1 = img_varient(img1,scale_factor[k],mirror_flip[j])

								avg_img += img1
								ctr += 1
								#mi(img1,tng+task_str,[4,6,ctr],str(ctr))
						mn = avg_img.mean()
						for x in range(np.shape(avg_img)[0]):
							for y in range(np.shape(avg_img)[1]):
								if np.sqrt((x-np.shape(avg_img)[0]/2)**2+(y-np.shape(avg_img)[1]/2)**2) < fix_mask_radius:
									avg_img[x,y] = mn
						#mi(z2o(z_aggressive_score_img(avg_img/6.0,3.0,-2))**2,tng+' avg HERE!'+task_str,[4,1,i+1])
						title_str = ''
						if (not save_images and i == 0) or save_images:
							title_str = task
						mi_save(z2o(avg_img)**1.0,opj(subject,sub_experiments[0],str(month),str(day)),[n_images+1,1+len(conditions),1+task_ctr+i*(1+len(conditions))],title_str)
						avg_img_big = scipy.misc.imresize(avg_img,[768,1024])
						ci = kzpy.img.yb_color_modulation_of_grayscale_image(img_varient(Img_Dic[sub_experiments[0]][i],scale_factor[0],False),z2o(avg_img_big)**3.0,(1.0-z2o(avg_img_big))**3.0)
						mi_save(ci,opj(subject,sub_experiments[0],str(month),str(day),'YB'),[n_images+1,1+len(conditions),1+task_ctr+i*(1+len(conditions))],title_str)
						
			elif sub_experiments[0] == 'Three_circles':
				n_images = 4
				scale_factor = [2.0,1.5,1.0]
				for i in range(len(Img_Dic[sub_experiments[0]])):
					mi_save(img_varient(Img_Dic[sub_experiments[0]][i],scale_factor[0],False),'differences: ' + opj(subject,sub_experiments[0],str(month),str(day)),[n_images+1,1+len(conditions),1+i*(1+len(conditions))],title_str)	
					mi_save(img_varient(Img_Dic[sub_experiments[0]][i],scale_factor[0],False),'differences: ' + opj(subject,sub_experiments[0],str(month),str(day),'YB'),[n_images+1,1+len(conditions),1+i*(1+len(conditions))],title_str)	

				
				#del img
				task_ctr = 0
				avgs = []
				for task in conditions:
					task_ctr+=1
					ctr = 0
					for i in range(n_images):
						avg_img = np.zeros((96,128))
						for k in range(len(scale_factor)):
							stats_path = opj(work_path,'Research/data/experiments',experiment,sub_experiments[0],task,'subjects',subject,str(year),str(month),str(day),str(session),'stats',pp)
							img1 = scipy.misc.imread(opj(stats_path,'p_images/png_std/'+str(ctr)+'.png'))#  '/Users/davidzipser/Desktop/Pictures_Desktop/new_'+task_str+'/'+str(ctr)+'.png')
							img1 = img_varient(img1,scale_factor[k],False)
							avg_img += img1
							ctr += 1
							mi_save(img1,opj(subject,sub_experiments[0],str(month),str(day),'separate'),[4,6,ctr],str(ctr))
							mn = avg_img.mean()
							for x in range(np.shape(avg_img)[0]):
								for y in range(np.shape(avg_img)[1]):
									if np.sqrt((x-np.shape(avg_img)[0]/2)**2+(y-np.shape(avg_img)[1]/2)**2) < fix_mask_radius:
										avg_img[x,y] = mn
						title_str = ''
						if (not save_images and i == 0) or save_images:
							title_str = task+' '
						mi_save(z2o(avg_img)**1.0,opj(subject,sub_experiments[0],str(month),str(day)),[n_images+1,1+len(conditions),1+i*(1+len(conditions))],title_str + str(i))
						avgs.append(avg_img)
				avg = np.array(avgs).mean(axis=0)
				for i in range(n_images):
					avg_img_big = scipy.misc.imresize(z2o(avgs[i]-avg),[768,1024])
					ci = kzpy.img.yb_color_modulation_of_grayscale_image(img_varient(Img_Dic[sub_experiments[0]][i],scale_factor[0],False),(z2o(avg_img_big)**1.0)**3.0,(1.0-z2o(avg_img_big))**3.0,False)
					mi_save(ci,'differences: ' + opj(subject,sub_experiments[0],str(month),str(day),'YB'),[n_images+1,1+len(conditions),1+task_ctr+i*(1+len(conditions))],title_str + str(i))
					mi_save(z2o(avgs[i]-avg)**1.0,'differences: ' + opj(subject,sub_experiments[0],str(month),str(day)),[n_images+1,1+len(conditions),1+task_ctr+i*(1+len(conditions))],title_str + str(i))

			elif sub_experiments[0] == 'Overlapping_face_place':
				mirror_flip = [False]
				scale_factor = [1.0]
				n_images = 8
				for i in range(len(Img_Dic[sub_experiments[0]])):
					mi_save(img_varient(Img_Dic[sub_experiments[0]][i],scale_factor[0],False)[130:637,308:715],opj(subject,sub_experiments[0],str(month),str(day)),[n_images+1,1+len(conditions),1+i*(1+len(conditions))],'')	
					mi_save(img_varient(Img_Dic[sub_experiments[0]][i],scale_factor[0],False)[130:637,308:715],opj(subject,sub_experiments[0],str(month),str(day),'YB'),[n_images+1,1+len(conditions),1+i*(1+len(conditions))],'')	
				
				task_ctr = 0
				SES[ses]['Tasks'] = {}
				SES[ses]['Tasks']['attend_face']=[]
				SES[ses]['Tasks']['attend_place']=[]
				for task in conditions:
					task_ctr+=1
					ctr = 0
					for i in range(n_images):
						avg_img = np.zeros((96,128))
						for j in range(len(mirror_flip)):
							for k in range(len(scale_factor)):
								stats_path = opj(work_path,'Research/data/experiments',experiment,sub_experiments[0],task,'subjects',subject,str(year),str(month),str(day),str(session),'stats',pp)
								img1 = scipy.misc.imread(opj(stats_path,'p_images/png_std/'+str(ctr)+'.png'))#  '/Users/davidzipser/Desktop/Pictures_Desktop/new_'+task_str+'/'+str(ctr)+'.png')
								img1 = img_varient(img1,scale_factor[k],mirror_flip[j])

								avg_img += img1
								ctr += 1
								#mi_save(img1,tng+task_str,[4,6,ctr],str(ctr))
						mn = avg_img.mean()
						for x in range(np.shape(avg_img)[0]):
							for y in range(np.shape(avg_img)[1]):
								if np.sqrt((x-np.shape(avg_img)[0]/2)**2+(y-np.shape(avg_img)[1]/2)**2) < 0: #fix_mask_radius:
									avg_img[x,y] = mn
						#mi_save(z2o(z_aggressive_score_img(avg_img/6.0,3.0,-2))**2,tng+' avg HERE!'+task_str,[4,1,i+1])
						title_str = ''
						if (not save_images and i == 0) or save_images:
							title_str = task
						avg_img_big = scipy.misc.imresize(avg_img,[768,1024])
						avg_img_big = avg_img_big[130:637,308:715]
						mi_save(z2o(avg_img_big)**1.0,opj(subject,sub_experiments[0],str(month),str(day)),[n_images+1,1+len(conditions),1+task_ctr+i*(1+len(conditions))],title_str)
						SES[ses]['Tasks'][task].append(z2o(avg_img_big))
						#ci = kzpy.img.yb_color_modulation_of_grayscale_image(img_varient(Img_Dic[sub_experiments[0]][i],scale_factor[0],False),z2o(avg_img_big)**3.0,(1.0-z2o(avg_img_big))**3.0)
						stim = (z2o(img_varient(Img_Dic[sub_experiments[0]][i],scale_factor[0],False)[:,:,0])-0.5)[130:637,308:715]
						ci = stim * z2o(avg_img_big)**2
						mi_save(ci,opj(subject,sub_experiments[0],str(month),str(day),'YB'),[n_images+1,1+len(conditions),1+task_ctr+i*(1+len(conditions))],title_str)
				for i in range(len(Img_Dic[sub_experiments[0]])):
					mi_save(SES[ses]['Tasks']['attend_face'][i]-SES[ses]['Tasks']['attend_place'][i],opj(subject,sub_experiments[0],str(month),str(day),'DIFF'),[n_images+1,1+len(conditions),1+1+i*(1+len(conditions))],title_str)
					mi_save(-SES[ses]['Tasks']['attend_face'][i]+SES[ses]['Tasks']['attend_place'][i],opj(subject,sub_experiments[0],str(month),str(day),'DIFF'),[n_images+1,1+len(conditions),1+2+i*(1+len(conditions))],title_str)
					stim = (z2o(img_varient(Img_Dic[sub_experiments[0]][i],scale_factor[0],False)[:,:,0])-0.5)[130:637,308:715]
					ci = stim * z2o(SES[ses]['Tasks']['attend_face'][i]-SES[ses]['Tasks']['attend_place'][i])**2
					mi_save(ci,opj(subject,sub_experiments[0],str(month),str(day),'DIFF MOD'),[n_images+1,1+len(conditions),1+1+i*(1+len(conditions))],title_str)
					ci = stim * z2o(-SES[ses]['Tasks']['attend_face'][i]+SES[ses]['Tasks']['attend_place'][i])**2
					mi_save(ci,opj(subject,sub_experiments[0],str(month),str(day),'DIFF MOD'),[n_images+1,1+len(conditions),1+2+i*(1+len(conditions))],title_str)

			else:
				os.sys.exit('ERROR, unknown sub_experiment: ' + sub_experiments[0])		
if False:
	for i in range(len(Img_Dic[sub_experiments[0]])):
		titles = ['','','']
		if i == 0:
			titles = ['stimulus','attend_face','attend_place']
		stim = (z2o(img_varient(Img_Dic[sub_experiments[0]][i],scale_factor[0],False)[:,:,0])-0.5)[130:637,308:715]
		ci = stim * 0.5*(z2o(SES['KZ_22']['Tasks']['attend_face'][i]-SES['KZ_22']['Tasks']['attend_place'][i])**2+z2o(SES['KZ_23']['Tasks']['attend_face'][i]-SES['KZ_23']['Tasks']['attend_place'][i])**2)
		mi(ci,opj(subject,sub_experiments[0],str(month),str(day),'DIFF MOD SES'),[n_images+1,1+len(conditions),1+1+i*(1+len(conditions))],titles[1])
		ci = stim * 0.5*(z2o(-SES['KZ_22']['Tasks']['attend_face'][i]+SES['KZ_22']['Tasks']['attend_place'][i])**2+z2o(-SES['KZ_23']['Tasks']['attend_face'][i]+SES['KZ_23']['Tasks']['attend_place'][i])**2)
		mi(ci,opj(subject,sub_experiments[0],str(month),str(day),'DIFF MOD SES'),[n_images+1,1+len(conditions),1+2+i*(1+len(conditions))],titles[2])
		mi(img_varient(Img_Dic[sub_experiments[0]][i],scale_factor[0],False)[130:637,308:715],opj(subject,sub_experiments[0],str(month),str(day),'DIFF MOD SES'),[n_images+1,1+len(conditions),1+i*(1+len(conditions))],titles[0])	


#######################################################################################################
if False:
	face_place_sequence = [1,2,3,3,4,5,6,7,
		7, 8, 1, 2, 6, 5, 4, 3,
		1, 2, 3, 5, 6, 7, 4, 8,
		2, 2, 3, 4, 6, 7, 8, 2,
		3, 6, 4, 4, 5, 5, 7, 8,
		1, 1, 3, 5, 6, 7, 8, 1]
	for i in range(15):
			print(str(0))
	for n in face_place_sequence:
		for i in range(3):
			print(str(face_place_sequence[n]))
		for i in range(2):
			print(str(0))
	for i in range(15):
			print(str(0))

#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################

#
print('Done')
#
########################################################
