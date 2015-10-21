from kzpy3.utils import *
import kzpy3.fMRI.data.feat_design

"""
21 October 2015

Basic preprocssing goals:

This module provides the code to preprocess fMRI data. There are several stages in this process.

The BIC fMRI scanner produces data files in dicom format. These are exported using a program called
Osirix on the transfer Mac at the BIC. Each fMRI run is put into a separate folder of  dicom files.
For example, a typical run folder and contents are:

	mb_bold_mb6_20mm_AP_PSN_8
		IM-0008-0001.dcm
		IM-0008-0002.dcm
		IM-0008-0003.dcm
		. . .

Each dcm file contains a single volume at one TR.

There will be several of these folders for each scanning session.

These files will be processed in a sequence of steps, taking them into Nifti format (where an
entire run is in a single 4 dimensional space-time file). Subsequently these are further processed
by FSL to generate more refined versions. Thus, preprocessing involves generating a lot of intermediate
stages of data files. I organize these in 'Research' hierarchies.


Organization of the Research folders:

It would seem natural to keep all the data within a single hierarchy of directories. There is a major problem
with this, however, because the data directories can become huge and they quickly fill up hard drive capacity.
Not all the intermediate data stages are necessary for active analysis.

The solution is to put separate chunks on data into independent directories and symbolically link them into
the main hierarchy as needed.

The main directory structure is:

Research
	data
		experiments [ignore this for now]
		protocols [ignore this for now]
		subjects
			S1_2015 [for example]
				2015 [year]
				  7 [month]
				    10 [day of scan]
				       0 [session within day]
					dcm [dicoms, this will be a symbolic link]
					fsl
					func_runs
					info
					log
					mat
					nii
					stats
	other [ignore this for now]
	stimuli [ignore this for now]

The dcm subdirectory will not contain files, but will be a symbolic link to a dcm directory in the following:

Research-data-subjects-S1_2015-2015-7-10-0-dcm
	data
		subjects
			S1_2015
				2015
				  7
				    10
				       0
					dcm
						AAHScout_32ch_5
						AAHScout_32ch_MPR_6
						mb_bold_mb6_20mm_AP_PSN_7
							IM-0007-0001.dcm
							IM-0007-0002.dcm
							IM-0007-0003.dcm
							. . .

						. . .

There are some things to note. First, the name of the hierarchy containing the actual data files
indicates the contents. This makes it easy to select subsets of data as needed.
Second, the directory structure exactly mirrors the structure of the main Research
hierarchy. Third, as much as possible, names are used either to indicate classes of content, or
the content, without redundancies. Thus, under subjects/S1_2015, the subject number will not
be repeated (e.g., the dicom folder is "dcm", not "S1_2015_dcm").

1) The first preprocessing step is simply to move the folders from whatever transfer folder they were put in when
taken from the scanner into a Research folder of the appropriate name. I will refer to this as "Research-".This is done with:

	dcm_to_Research_folders(start_path, end_path, subject, year, month, day, session)

2) The second preprocessing step takes take the dicom files their Research- folder and transform 
them into Nifti files and place these into another Research- folder. This requires an application 
called "dcm2nii64" from the site http://www.mccauslandcenter.sc.edu/mricro/mricron/dcm2nii.html . 
I assume this to be ~/Desktop/Research/data/protocols/mricron/dcm2nii64 . The function:
	
	MULTI_dcm2nii(start_path, end_path,to_do,use_PSN)

is used to accomplish this transformation.


Here is an example log used to preprocess data collected from S1_2015 on 7/10/2015:

####### dcm_to_Research_folders ########
# 10/21/2015, 9:39 a.m.
ipython
from kzpy3.fMRI.data.preprocess import *
#import kzpy3.fMRI.data.preprocess;reload(kzpy3.fMRI.data.preprocess);from kzpy3.fMRI.data.preprocess import *
dcm_to_Research_folders( opjh('Desktop/a_dcm_folder'), opjh('Desktop'), 'S1_2015', 2015, 7, 10, 0 )
#
####### MULTI_dcm2nii ########
# 10/21/2015, 9:54 a.m.
ipython
from kzpy3.fMRI.data.preprocess import *
start_path = opjh('Desktop')
end_path = opjh('Desktop')
to_do = [['S1_2015',2015,7,10,0]]
MULTI_dcm2nii(start_path, end_path,to_do, True)
#
###############
"""

def dcm_to_Research_folders(start_path, end_path, subject, year, month, day, session):
	'''	
	### Preprocessing step one: get the dicom data from a session into a chunking Research- folder

	E.g.,   [20 Oct. 2015]

	dcm_to_Research_folders( opjh('Desktop/a_dcm_folder'), opjh('Desktop'), 'S1_2015', 2015, 7, 10, 0 )

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

def multi_dcm2nii(dcm_path,dcm_dirs,nii_path,dcm2nii64_path = False):
	'''
	This requires the application dcm2nii64. If the path to this is
	not specificied, it is set to an assumed location (see code below).
	The application if from the site: http://www.mccauslandcenter.sc.edu/mricro/mricron/dcm2nii.html

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
		if not dcm2nii64_path:
			dcm2nii64_path = opjh('Desktop/Research/data/protocols/mricron/dcm2nii64')
		dcm2nii_str = dcm2nii64_path + ' -a y -o ' + nii_path + ' ' + dcm_path + '/' + n + ' > ' + nii_path + '/txt/' + n + '.txt'
		print(dcm2nii_str)
		if bkg < 2:
			dcm2nii_str += " &"
			bkg += 1
		else:
			bkg = 0
		#print(dcm2nii_str)
		os.system(dcm2nii_str)



