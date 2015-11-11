from kzpy3.utils import *
from kzpy3.fMRI.data.preprocess_part_III import *
from kzpy3.fMRI.data.pRF import *

import nibabel as nib

"""
These processing functions begin to get more and more specific for specific experiments, guided toward
voxel RF mapping.

Part IV is just one function,

	average_r_volumes_for_Wedge_annulus_and_sorted_xyz_list(subject,experiment)

which takes stats from the experiments dir, averages them, and saves results to subjects dir. The idea is that
these stats, related to RF mapping, tell general information of use about the subject.

Part V maps the recetpive fields using:

	map_receptive_fields_with_Wedge_Annulus_sequences_1_and_2(work_path,subject)

This saves files of the form:

	rf_r_vol.Wedge_annulus.674160.nii
	rf_x_vol.Wedge_annulus.674160.nii
	rf_y_vol.Wedge_annulus.674160.nii

in the subject's stats dir for the session. Again, not in the experiments dir because these are intended as general results about the
subject which will be used elsewhere.
##############################################################################################################
######## Here is an example log used to process data collected from S1_2015 on 7/10/2015: #################
##
# 11/10/2015
ipython
work_path = opjD('')
subject = 'S1_2015'
experiment = 'Phase_two_BIC_research/Wedge_annulus'
average_r_volumes_for_Wedge_annulus_and_sorted_xyz_list(work_path,subject,experiment)

subject = 'S1_2015'
work_path = opjD('')
map_receptive_fields_with_Wedge_Annulus_sequences_1_and_2(work_path,subject)

##############################################################################################################

"""

#########################################################################################################
################### PART IV: average r_volumes for Wedge_annulus, and sorted xyz list ###################
#


def average_r_volumes_for_Wedge_annulus_and_sorted_xyz_list(work_path,subject,experiment):
	"""
	This is a specialized function to get stats across stimuli, used prior to RF mapping
	e.g.,
	work_path = opjD('')
	subject = 'S1_2015'
	experiment = 'Phase_two_BIC_research/Wedge_annulus'
	average_r_volumes_for_Wedge_annulus_and_sorted_xyz_list(work_path,subject,experiment)
	"""
	r_volume_paths = []
	rootDir = opj(work_path,'Research/data/experiments')
	for dirName, subdirList, fileList in os.walk(rootDir):
		if str_contains(dirName, [subject,experiment,'stats/pp_']):
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
###################### Part V: map receptive fields ###################################################
#


def map_receptive_fields_with_Wedge_Annulus_sequences_1_and_2(work_path,subject):
	"""
	subject = 'S1_2015'
	work_path = opjD('')
	"""

	

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

		nnn = len(r_sorted_xyz_list) #20000

		for i in range(0,nnn):#len(r_sorted_xyz_list)):
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

			if mod(i,100) == 0 or i == (nnn-1):
				print('*** Saving ***')
				header = nii1.get_header()
				affine = nii1.get_affine()
				rf_x_vol_img = nib.Nifti1Image(rf_x_vol, affine, header)
				nib.save(rf_x_vol_img, opj(rxyz,'rf_x_vol.Wedge_annulus.'+str(nnn)+'.nii.gz'))
				rf_y_vol_img = nib.Nifti1Image(rf_y_vol, affine, header)
				nib.save(rf_y_vol_img, opj(rxyz,'rf_y_vol.Wedge_annulus.'+str(nnn)+'.nii.gz'))
				rf_r_vol_img = nib.Nifti1Image(rf_r_vol, affine, header)
				nib.save(rf_r_vol_img, opj(rxyz,'rf_r_vol.Wedge_annulus.'+str(nnn)+'.nii.gz'))


