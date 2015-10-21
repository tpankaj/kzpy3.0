from kzpy3.utils import *
import kzpy3.fMRI.data.feat_design

"""
from kzpy3.fMRI.data.preprocess import *
import kzpy3.fMRI.data.preprocess;reload(kzpy3.fMRI.data.preprocess);from kzpy3.fMRI.data.preprocess import *
"""

def dcm_to_Research_folders(start_path, end_path, subject, year, month, day, session):
	'''	
	### Preprocessing step one: get the dicom data from a session into a chunking Research- folder

	E.g.,   [20 Oct. 2015]

	dcm_to_Research_folders( opjh('Desktop/dcm_folder'), opjh('Desktop'), 'S1_2015', 2015, 7, 10, 0 )

	This creates the dir ~/Desktop/Research-data-subjects-S1_2015-2015-7-10-0-dcm, with the dicoms in 
	the appropriate subdirectory.

	'''
	dst = end_path + '/Research-data-subjects-'
	dst += subject + '-' 
	dst += str(year) + '-' 
	dst += str(month) + '-' 
	dst += str(day) + '-' 
	dst += str(session) + '-'
	dst += 'dcm'
	dst += '/data/subjects/'
	dst += subject + '/'
	dst += str(year) + '/'
	dst += str(month) + '/'
	dst += str(day) + '/'
	dst += str(session) + '/'
	dst += 'dcm'
	mkdir_str = 'mkdir -p ' + dst
	print "-bash: "+mkdir_str
	os.system(mkdir_str)
	chmod_str0 =  'chmod a+w ' + start_path 
	os.system(chmod_str0)
	print "-bash: "+chmod_str0
	for filename in os.listdir(start_path.replace('\ ',' ')):
		chmod_str1 =  'chmod a+w ' + start_path + '/' + filename
		print "-bash: "+chmod_str1
		os.system(chmod_str1)
	mv_str = 'mv ' + start_path + '/* ' + dst
	print "-bash: "+mv_str
	os.system(mv_str)




def MULTI_dcm2nii(start_path, end_path,to_do,use_PSN=True):
	'''
	### Preprocessing step two: convert dicoms of sessions to Nifti's and place in appropriate Research- folders
	E.g.,

	start_path = opjh('Desktop')
	end_path = opjh('Desktop')
	to_do = [['S1_2015',2015,7,10,0]]     #[['S4_2015',2015,6,17,0],['S5_2015',2015,6,3,0]]
	MULTI_dcm2nii(start_path, end_path,to_do, True)

	This creates the folder:
	Research-data-subjects-S1_2015-2015-7-10-0-nii with appropriate subfolders.
	'''
	
	for symds in to_do:
		subject = symds[0]
		year = str(symds[1])
		month = str(symds[2])
		day = str(symds[3])
		session = str(symds[4])
		dcm_path = 'Research-data-subjects-' + subject + '-' + year + '-' + month + '-' + day + '-' + session + '-dcm/'
		dcm_path += 'data/subjects/' + subject + '/' + year + '/' + month + '/' + day + '/' + session + '/dcm/'
		
		nii_path = dcm_path.replace('dcm/','nii/')

		dcm_path = opj(start_path,dcm_path)
		nii_path = opj(end_path,nii_path)

		mb6_even,mb6_odd,mb6_all,t1,fm = list_dcm_folders(dcm_path)

		print dcm_path
		print nii_path
		
		if use_PSN:
			mb6 = mb6_even
		else:
			mb6 = mb6_odd
		multi_dcm2nii(dcm_path,mb6+t1+fm,nii_path)

#############
# Local constants and functions:

mb_bold_prefix = 'mb_bold_mb6_20mm_AP_PSN_'
t1_prefix = 't1_mprage_'
fm_prefix = 'gre_field_mapping_16Mar2015_'
mb_nii_suffix = 'a001.nii.gz'


def list_dcm_folders(path):
	mb6 = []
	t1 = []
	fm = []
	dr,ls = dir_as_dic_and_list(path)
	for e in ls:
		if e[0:len(fm_prefix)] == fm_prefix:
			fm.append(e)
		if e[0:len(mb_bold_prefix)] == mb_bold_prefix:
			n = int(e[len(mb_bold_prefix):])
			p = os.path.join(path,e)
			dr_sub,ls_sub = dir_as_dic_and_list(p)
			mb6.append([e,n,len(ls_sub)])
		if e[0:len(t1_prefix)] == t1_prefix:
			t1.append(e)		
	mb6.sort(key=lambda x: x[1])
	n_mb6_vols = mb6[0][2]
	for m in mb6:
		if m[2] != n_mb6_vols:
			print(path)
			print(m)
			print("Warning: number of volumes("+str(m[2])+") != n_mb6_vols("+str(n_mb6_vols)+"):")
	mb6_odd = mb6[0:][::2]
	mb6_even = mb6[1:][::2]
	return mb6_even,mb6_odd,mb6,t1,fm

def multi_dcm2nii(dcm_path,dcm_dirs,nii_path):
	'''
	Example:
	dcm_path = '/Users/karlzipser/Google_Drive/Research-data-subjects-S1_2014-2015-6-20-0-dcm/data/subjects/S1_2014/2015/6/20/0/dcm'
	nii_path = '/Users/karlzipser/Desktop/Research-data-subjects-S1_2014-2015-6-20-0-nii/data/subjects/S1_2014/2015/6/20/0/nii'
	mb6_even,mb6_odd,mb6,t1,fm = preprocess.list_dcm_folders(p)
	multi_dcm2nii(dcm_path,mb6_odd,nii_path):
	'''
	mkdir_str = 'mkdir -p ' + nii_path+'/txt'
	print(mkdir_str)
	os.system(mkdir_str)

	bkg = 0
	for d in dcm_dirs:
		if type(d)==str:
			n = d
		else:
			n = d[0]
		#dcm2nii_str = '/Users/davidzipser/Google_Drive/Research/data/protocols/mricron/dcm2nii64 -a y -o ' + nii_path + ' ' + dcm_path + '/' + n + ' > ' + nii_path + '/txt/' + n + '.txt'
		dcm2nii_str = 'dcm2nii64 -a y -o ' + nii_path + ' ' + dcm_path + '/' + n + ' > ' + nii_path + '/txt/' + n + '.txt'
		print(dcm2nii_str)
		if bkg < 2:
			dcm2nii_str += " &"
			bkg += 1
		else:
			bkg = 0
		#print(dcm2nii_str)
		os.system(dcm2nii_str)



