from kzpy3.utils import *
import kzpy3.fMRI.data.feat_design

"""
21 October 2015

This module provides the code to preprocess fMRI data. There are several stages in this process.

Part I: Basic preprocessing

Basic preprocssing goals:

The BIC fMRI scanner produces data files in dicom format. These are exported using a program called
Osirix on the transfer Mac at the BIC. Each fMRI run is put into a separate folder of dicom files.
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
by FSL to generate more refined versions. Thus, preprocessing involves generating intermediate
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
		experiments
		protocols
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
	other
	stimuli

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

There are some things to note. First, the name of the Research- hierarchy containing the actual data files
indicates the contents. This makes it easy to select subsets of data as needed.
Second, the directory structure exactly mirrors the structure of the main Research
hierarchy. Third, as much as possible, names are used either to indicate classes of content, or
the content, without redundancies. Thus, under subjects/S1_2015, the subject number will not
be repeated (e.g., the dicom folder is "dcm", not "S1_2015_dcm").

In detail, here are preprocessing steps accomplished by this module:

1) The first preprocessing step is simply to move the folders from whatever transfer folder they were put in when
taken from the scanner, into a Research folder of the appropriate name. I will refer to this as "Research-".
This is done with the function

	dcm_to_Research_folders(start_path, end_path, subject, year, month, day, session)

2) The second preprocessing step reads the dicom files their Research- folder and transforms 
them into Nifti files and places these into another Research- folder. This requires an external application 
called "dcm2nii64" from the site http://www.mccauslandcenter.sc.edu/mricro/mricron/dcm2nii.html . 
I assume application file to be ~/Desktop/Research/data/protocols/mricron/dcm2nii64 . The function:
	
	MULTI_dcm2nii(start_path, end_path,to_do,use_PSN)

is used to accomplish this transformation.

		[22 Oct. 2015]

3) The third preprocessing step is to apply the FSL application FEAT to the .nii files. The function:
	
	MULTI_feat(start_path, end_path,to_do,TR_s, n_TRs, n_delete_TRs,run_one_in_bkg,mb6_MosaicRefAcqTimes_path)

with sample parameter settings:

		work_path = opjh('Desktop')
		TR_s, n_TRs, n_delete_TRs, = 0.9,300,6
		to_do = [['S1_2015',2015,7,10,0,'align_to_middle_run_of_session','pp_a0']]
		run_one_in_bkg = True

handles this. Unlike the previous two steps, this is a complex and parameter laden process. The to_do list
is a list of sessions, with each sublist specifying:
	subject
	session year
	month
	day
	session number
	alignment specifier
	alignment name

FEAT must be run for each .nii file in this process. A key question is to what should the .nii
file be motion-corrected to? This is important to enable the various .nii files from the same an other sessions
to be compared. One option for the alignment specifier is 'align_to_middle_run_of_session'. This causes the align_to_middle_run_of_session
run of the session to be sent to FEAT first, and subsequently processing the remaining runs aligned to it. I use the
alignment name 'pp_a0' for this. The reference volume information is saved in the FEAT log "report_log.html" under 'Initalisation',
with a call to /usr/local/fsl/bin/fslmaths. Another option is to align to a specified mean_func.nii.gz file in some pre-existing .feat folder.
For this condition I use the alignment name 'pp_b0'. Thus, one approach is to have one session aligned to its middle run (pp_a0) and another is
to have other sessions aligned to this same middle run (pp_b0). The alignment name in fact is a place holder which allows for different
parameter settings of FEAT processing to be stored in parallel. Thus, I may later have other preprocessing names with the 'pp_' prefix.

For slice time correction for the multi-band 6 scanning protocol, the file mb6_MosaicRefAcqTimes.txt is needed, which contains
information generated by dcm2nii64 in the previous step. These data should be the independent of subject or session, so I have a single
file to contain this information, which I keep in Research/data/protocols/. Note, if this file is not found, FEAT merely gives a warning,
but continues to run (presumably without slice time correction).


Part II: Data Organization

After finishing steps 1-3 above, the data will be in analysis-ready form. The goal of Part II is to do book keeping,
linking data files into the Research hierarchy so that they are easily accessible.

4) A simple step is to take sessions with data in Research- folders and link the relevant
data directories into the main Research hierarchy. This is accomplished with the 
	
	add_sessions(to_do,Research_path,print_only)

function. Note that the to_do argument requires a different structure from that above, something
which I should perhaps address to avoid confusion. Note that Research_path refers to the folder
containing the Research folders (e.g., opjh('Desktop')).

This generates the following folders in the session folder under the main Research folder:

	dcm [sym link]
	fsl
		pp_a0 [example, sym link]
	info
	log
	mat
	nii [sym link]

The .mat files generated by the fMRI stimulus computer for the session now need to be put into the mat
folder indicated in the list above. There should be exactly one .mat file for each functional run that 
is relevant for further analysis. These .mat files are discussed in more detail in the next section.

5) The next step is to prepare a text file for each session (info/session_info.txt), that allows for binding between runs and particular
experiments and tasks. This is done with the function

	add_sessions_info(to_do,Research_path)

These text files have the header line:

	nii_name	mat_name	sub_experiment	condition	experiment

with columns below containg the relevant information, as far as possible.

Where does the information about binding come from? Currently it is coded in the name of a .mat
file in the mat folder of the session, for example:

	mat/201507100902_subjS1_2015_run1_expZM01.mat

The reason for this is that these mat files are generated by the MATLAB script that generates stimuli for the 
projection screen in the scanner. 

Prior to June 2015 I did not use this system, so coded matfiles will need to be generated for earlier
data. The add_sessions_info can work on multiple sessions as specified in the to_do list.

Note, the information in info/session_info.txt generated here may not be complete, depending on 
the experiment. This is because not all information is coded in the matfile name. Specifically,
attention task is omited. Thus, for some experiments, these files will contain blanks in the form 
of underscore characters. These need to be manually edited before proceeding. Also, information may
be incorrect. For example, I need to change "Kendrick_Kay_visit_19to26June2015" into
"Phase_two_BIC_research" for the preprocessing I am testing now.

6) The next step is to use the [edited] info/session_info.txt files to generate symbolic links that bind 
data to experiments. This is done with the function

	link_func_runs(subject,year,month,day,session,mc_version,Research_path)

which creates an intermediate representation under the func_runs directory in the session directory.
This contains numbered runs with links to the .feat folder and the .mat file. Then, links are created 
under Research/data/experiments which mirror the func_runs directory under Research/data/subjects. For example,
the following directory structure is utilized/created:

Research
	data
		experiments
			Phase_two_BIC_research [Refers to July 2015 onward]
				Wedge_annulus
					sequence1
						subjects
							S1_2015
								7
									10
										0
											func_runs
												pp_a0
													1 [run number, sym link]
													3 [sym link]
					sequence2
						subjects
							S1_2015
								7
									10
										0
											func_runs
												pp_a0
													2 [sym link]
													4 [sym link]


In other words, step 6 allows us to access the data from the primary point of view of experiments and tasks,
rather than from the primary point of view of subjects and dates. The intention is that once preprocessing is complete, further analysis 
will access the data through the Research/data/expriments path rather than the Research/data/subjects path.

Only the relevant Research-...-fsl... folders need to be kept on working diskspace as long as the 
preprocessing is acceptable. Research-...-dcm and Research-...-nii folders can be kept on archive disks,
for example. At later stages, even the Research-...-fsl... folders may not be necessary for ongoing analysis, but that is outside
the scope of this preprocessing module.

In summary, we have the following input sources for preprocessing:

	.dcm files sorted by run, as transferred from the BIC following an experiment
	mb6_MosaicRefAcqTimes.txt for slice timing corrections of the multi-band 6 protocol
	.mat files generated by the stimulus Mac, or modified to be of the form 201507100902_subjS1_2015_run1_expZM01.mat
	a session_info.txt file for each session, generated here but edited manually

_____

##############################################################################################################
######## Here is an example log used to preprocess data collected from S1_2015 on 7/10/2015: #################
##
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
####### MULTI_feat ########
# 10/21/2015
from kzpy3.fMRI.data.preprocess import *
#import kzpy3.fMRI.data.preprocess;reload(kzpy3.fMRI.data.preprocess);from kzpy3.fMRI.data.preprocess import *
work_path = opjh('Desktop')
TR_s, n_TRs, n_delete_TRs, = 0.9,300,6
to_do = [['S1_2015',2015,7,10,0,'align_to_middle_run_of_session','pp_a0']]
run_one_in_bkg = True
MULTI_feat(work_path, work_path, to_do, TR_s, n_TRs, n_delete_TRs, run_one_in_bkg)
#
###############
# 10/22/2015
from kzpy3.fMRI.data.preprocess import *
#import kzpy3.fMRI.data.preprocess;reload(kzpy3.fMRI.data.preprocess);from kzpy3.fMRI.data.preprocess import *
to_do = [	['S1_2015',[[2015,7,10,0,'pp_a0']]]] # Note, different format from above.
add_sessions(to_do,opjh('Desktop'),print_only=False)
###############
# 10/22/2015
# <Now put the .mat files into the 'mat' directory, then:
add_sessions_info(to_do,opjh('Desktop'))
# Manually edit 'session_info.txt' as described in the comments above.
###############
# 10/22/2015
#
import kzpy3.fMRI.data.preprocess;reload(kzpy3.fMRI.data.preprocess);from kzpy3.fMRI.data.preprocess import *
link_func_runs('S1_2015',2015,7,10,0,'pp_a0',opjh('Desktop'))
##
############################### end of example log ###########################################################
##############################################################################################################
"""

############################## Part I: Basic preprocessing ##############################
#

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

def MULTI_feat(start_path, end_path,to_do,TR_s, n_TRs, n_delete_TRs,run_one_in_bkg=True,mb6_MosaicRefAcqTimes_path=opjh("Desktop/Research/data/protocols/mb6_MosaicRefAcqTimes.txt")):
	'''
	### Preprocessing step three: apply feat to Nifti files, put in appropriate Reserach- folders
	E.g.,
from kzpy3.fMRI.data.preprocess import *
import kzpy3.fMRI.data.preprocess;reload(kzpy3.fMRI.data.preprocess);from kzpy3.fMRI.data.preprocess import *
work_path = opjh('Desktop')
TR_s, n_TRs, n_delete_TRs, = 0.9,300,6
to_do = [['S1_2015',2015,7,10,0,'align_to_middle_run_of_session','pp_a0']]
run_one_in_bkg = True
# Step three: apply feat to Nifti files, put in appropriate Reserach- folders
#print('sleep... (to make sure dicom2nii finishes)')
#time.sleep(5*60);
#print('awake.')
MULTI_feat(work_path, work_path, to_do, TR_s, n_TRs, n_delete_TRs, run_one_in_bkg)

The to_do list is a list of sessions, with each sublist specifying:
	subject
	session year
	month
	day
	session number
	alignment/preprocessing specifier
	alignment/preprocessing name

'''
	ctr = 0

	for symds in to_do:
		subject = symds[0]
		year = str(symds[1])
		month = str(symds[2])
		day = str(symds[3])
		session = str(symds[4])
		align_mean_func_path = symds[5]
		pp_name = symds[6]

		nii_path = 'Research-data-subjects-' + subject + '-' + year + '-' + month + '-' + day + '-' + session + '-nii/'
		nii_path += 'data/subjects/' + subject + '/' + year + '/' + month + '/' + day + '/' + session + '/nii/'
		
		fsl_path = nii_path.replace('-nii/','-fsl-'+pp_name+'/')
		fsl_path = fsl_path.replace('/nii/','/fsl/'+pp_name+'/')

		nii_path = opj(end_path,nii_path)
		fsl_path = opj(start_path,fsl_path)

		mb6_nii = sort_nii_files(nii_path)
		mb6_nii_to_align = list(mb6_nii)

		if align_mean_func_path == 'align_to_middle_run_of_session':
			align_run_index = np.int(np.floor(len(mb6_nii)/2.0))
			mb6_nii_align_run = mb6_nii[align_run_index]
			mb6_nii_to_align = mb6_nii_to_align[:align_run_index]+mb6_nii_to_align[(1+align_run_index):]
			mb6_nii_align_run_name = mb6_nii_align_run[0][:-7]
			design = kzpy3.fMRI.data.feat_design.get_design(TR_s, n_TRs, n_delete_TRs,
				4,mb6_MosaicRefAcqTimes_path,
					0,"",
					opj(nii_path,mb6_nii_align_run_name),opj(fsl_path,mb6_nii_align_run_name))
			design_str = 'design_' + mb6_nii_align_run_name + '.fsf'
			with open(opj(home_path,"Desktop",design_str), "w") as text_file:
				text_file.write(design)
			align_mean_func_path = opj(fsl_path,mb6_nii_align_run_name+'.feat/mean_func')
			os.system('feat '+opj(home_path,"Desktop",design_str))

		ctr = 0
		for i in range(len(mb6_nii_to_align)):
			design = kzpy3.fMRI.data.feat_design.get_design(TR_s, n_TRs, n_delete_TRs,
				4,mb6_MosaicRefAcqTimes_path,
				1,align_mean_func_path,
				opj(nii_path,mb6_nii_to_align[i][0][:-7]),opj(fsl_path,mb6_nii_to_align[i][0][:-7]))
			design_str = 'design_' + mb6_nii_to_align[i][0][:-7] + '.fsf'
			with open(opj(home_path,"Desktop",design_str), "w") as text_file:
				text_file.write(design)
			print(mb6_nii_to_align[i][0][:-7]) # put in more detail, and add a version of this to align run above.
			feat_str = 'feat '+opj(home_path,"Desktop",design_str)
			if run_one_in_bkg:
				if ctr%2 == 0:
					feat_str += ' &'
			os.system(feat_str)
			ctr += 1


############################## Part II: Data Organization ##############################
#


	


def add_sessions(to_do,Research_path,print_only=True):
	"""
	### Preprocessing step four: add session folders to main Research folder 
	"""
	print('add_sessions:')
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
			add_session_paths(subject,year,month,day,session,pp,Research_path,print_only)


def add_sessions_info(to_do,Research_path):
	"""
	### Preprocessing step five: get session information into main Research folder
	"""

	print('add_sessions:')
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
			add_session_info(subject,year,month,day,session,Research_path)





def link_func_runs(subject,year,month,day,session,mc_version,Research_path):
	session_info_dic = get_session_info(subject,year,month,day,session,Research_path)

	"""
	### Preprocessing step six: after manually editing the session_info.txt file for a given session,
	use this to create the runs folders for the session, which bind the mat files
	and the feat folders (and other stuff, if we have it),
	as well as linking the experiments runs to these.
	"""
	nii_name = session_info_dic['nii_name']
	mat_name = session_info_dic['mat_name']
	experiment = session_info_dic['experiment']
	sub_experiment = session_info_dic['sub_experiment']
	condition = session_info_dic['condition']

	func_runs_str = Research_path + '/Research/data/subjects/'+subject+'/'+str(year)+'/'+str(month)+'/'+str(day)+'/'+str(session) + '/func_runs/' + mc_version
	fsl_str = Research_path + '/Research/data/subjects/'+subject+'/'+str(year)+'/'+str(month)+'/'+str(day)+'/'+str(session) + '/fsl/' + mc_version

	wd = os.getcwd()
	os.system('mkdir -p ' + func_runs_str)
	os.chdir(func_runs_str)
	for i in range(len(nii_name)):
		mkdir_str = 'mkdir ' + str(i+1)

		ln_str1 = 'ln -s ../../../fsl/' + mc_version + '/' + nii_name[i].strip('.nii.gz') + '.feat' + ' ' + nii_name[i].strip('.nii.gz') + '.feat'
		ln_str2 = 'ln -s ../../../mat/' + mat_name[i] + ' ' + mat_name[i]
		cd_str3 = 'cd ..'

		os.system(mkdir_str)
		os.chdir(str(i+1))
		os.system(ln_str1)
		os.system(ln_str2)
		os.chdir('..')
	if True:
		for i in range(len(nii_name)):
			ex = experiment[i]
			se = sub_experiment[i]
			co = condition[i]
			func_runs_str = Research_path + '/Research/data/subjects/'+subject+'/'+str(year)+'/'+str(month)+'/'+str(day)+'/'+str(session) + '/func_runs/' + mc_version
			experiment_func_runs_str = Research_path + '/Research/data/experiments/'+ex+'/'+se+'/'+co+'/subjects/'+subject+'/'+str(year)+'/'+str(month)+'/'+str(day)+'/'+str(session)+'/func_runs/'+mc_version
			

			mkdir_str = 'mkdir -p ' + experiment_func_runs_str
			os.system(mkdir_str)
			os.chdir(experiment_func_runs_str)

			ln_str = 'ln -s ../../../../../../../../../../../../subjects/'+subject+'/'+str(year)+'/'+str(month)+'/'+str(day)+'/'+str(session) + '/func_runs/' + mc_version + '/'+str(i+1) + ' '+ str(i+1)
			os.system(ln_str)
	#		ln_str2 = 'ln -s ../../../mat/' + mat_name[i] + ' ' + mat_name[i]
	#		cd_str3 = 'cd ..'
		#print(mkdir_str)
		#os.system(mkdir_str)
		
	#		os.chdir(str(i+1))
	#		os.system(ln_str1)
	#		os.system(ln_str2)
	#		os.chdir('..')

	os.chdir(wd)
	










############### Local constants and functions ##############
#
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
	mb6_even,mb6_odd,mb6,t1,fm = list_dcm_folders(p)
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


### required for MULTI_feat

def sort_nii_files(path):
	'''

	'''
	mb6_nii = []
	dr,ls = dir_as_dic_and_list(path)
	for e in ls:
		if e[-len(mb_nii_suffix):] == mb_nii_suffix:
			n = int(e[(-len(mb_nii_suffix)-3):(-len(mb_nii_suffix))])             
			mb6_nii.append([e,n])
	mb6_nii.sort(key=lambda x: x[1])
	return mb6_nii

def add_session_paths(subject,year,month,day,session,pp,Research_path,print_only=True):
	'''
	'''
	ses_str0 = 'data/subjects/'+subject+'/'+str(year)+'/'+str(month)+'/'+str(day)+'/'+str(session)
	chunk_str0 = 'data-subjects-'+subject+'-'+str(year)+'-'+str(month)+'-'+str(day)+'-'+str(session)
	ses_prefix = Research_path + '/Research/'
	chunk_prefix = Research_path + '/Research-'
	ses_str = ses_prefix+ses_str0
	chunk_str = chunk_prefix+chunk_str0
	
	mb6_even,mb6_odd,mb6,t1,fm = list_dcm_folders(chunk_str+'-dcm/'+ses_str0+'/dcm') 
	print('\t\t\tC dmc mb6_even:'+str(len(mb6_even)))
	print('\t\t\tC dmc mb6_odd:'+str(len(mb6_odd)))
	print('\t\t\tC dmc mb6:'+str(len(mb6)))
	print('\t\t\tC dmc t1:'+str(len(t1)))
	print('\t\t\tC dmc fm:'+str(len(fm)))

	mb6_lst = sort_nii_files(chunk_str+'-nii/'+ses_str0+'/nii')
	print('\t\t\tC nii:'+str(len(mb6_lst)))

	ignore,feat_lst = dir_as_dic_and_list(chunk_str+'-fsl-' + pp +'/'+ses_str0+'/fsl/'+pp)
	print('\t\t\tC feat:'+str(len(feat_lst)))

	wd = os.getcwd()
	
	if print_only == False:
		mkdir_str = 'mkdir -p '
		mkdir_str1 = mkdir_str + ses_str + '/log'
		mkdir_str2 = mkdir_str + ses_str + '/info'
		mkdir_str3 = mkdir_str + ses_str + '/mat'
		mkdir_str4 = mkdir_str + ses_str + '/fsl'
		os.system(mkdir_str1)
		os.system(mkdir_str2)
		os.system(mkdir_str3)
		os.system(mkdir_str4)
		
		os.chdir(ses_str)
		relative_path1 = os.path.relpath(chunk_str+'-dcm/'+ses_str0+ '/dcm',ses_str)
		ln_str1 = 'ln -s ' + relative_path1 + ' .'
		os.system(ln_str1)
		relative_path2 = os.path.relpath(chunk_str+'-nii/'+ses_str0+ '/nii',ses_str)
		ln_str2 = 'ln -s ' + relative_path2 + ' .'
		os.system(ln_str2)
		relative_path3 = os.path.relpath(chunk_str+'-fsl-'+pp+'/'+ses_str0+ '/fsl/'+pp,ses_str)
		ln_str3 = 'ln -s ../' + relative_path3 + ' ./fsl/'
		os.system(ln_str3)

		mb6_even,mb6_odd,mb6,t1,fm = list_dcm_folders(ses_str+'/dcm') 
		print('\t\t\tdmc mb6_even:'+str(len(mb6_even)))
		print('\t\t\tdmc mb6_odd:'+str(len(mb6_odd)))
		print('\t\t\tdmc mb6:'+str(len(mb6)))
		print('\t\t\tdmc t1:'+str(len(t1)))
		print('\t\t\tdmc fm:'+str(len(fm)))
		
		mb6_lst = sort_nii_files(ses_str+'/nii')
		print('\t\t\tnii:'+str(len(mb6_lst)))
		
		ignore,feat_lst = dir_as_dic_and_list(ses_str+'/fsl/'+pp)
		print('\t\t\tfeat:'+str(len(feat_lst)))

	os.chdir(wd)
	




def add_session_info(subject,year,month,day,session,Research_path):
	'''
	'''
	ses_str = Research_path + '/Research/data/subjects/'+subject+'/'+str(year)+'/'+str(month)+'/'+str(day)+'/'+str(session)
	
	mb6 = sort_nii_files(ses_str + '/nii')

	ignore,mat = dir_as_dic_and_list(ses_str + '/mat')
	print((len(mb6),len(mat)))
	if len(mb6) != len(mat):
		print('ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
		os.system.exit('if len(mb6) != len(mat):')

	info_str_lst = ['nii_name\tmat_name\tsub_experiment\tcondition\texperiment\n']
	for i in range(len(mb6)):
		if 'expZM01' in mat[i]:
			exp_str = ' Wedge_annulus sequence1 Kendrick_Kay_visit_19to26June2015'
		elif 'expZM02' in mat[i]:
			exp_str = ' Wedge_annulus sequence2 Kendrick_Kay_visit_19to26June2015'
		elif 'expZM03' in mat[i]:
			exp_str = ' Vermeer ____ Kendrick_Kay_visit_19to26June2015'
		elif 'expZM04' in mat[i]:
			exp_str = ' Kay_images ____ Kendrick_Kay_visit_19to26June2015'
		elif 'expZM06' in mat[i]:
			exp_str = ' Stereo_Kanizsa fixate Kendrick_Kay_visit_19to26June2015'
		elif 'expZM07' in mat[i]:
			exp_str = ' Three_circles attend_as_directed Kendrick_Kay_visit_19to26June2015'
		elif 'expZM08' in mat[i]:
			exp_str = ' Overlapping_face_place ____ Kendrick_Kay_visit_19to26June2015'
		elif 'expZM09' in mat[i]:
			exp_str = ' Gorilla ____ Kendrick_Kay_visit_19to26June2015'
		elif 'exp10.' in mat[i]:
			exp_str = ' Wedge_annulus sequence1a Phase_two_BIC_research'
		elif 'exp11.' in mat[i]:
			exp_str = ' Wedge_annulus sequence1b Phase_two_BIC_research'
		elif 'exp12.' in mat[i]:
			exp_str = ' Wedge_annulus sequence2a Phase_two_BIC_research'
		elif 'exp13.' in mat[i]:
			exp_str = ' Wedge_annulus sequence2b Phase_two_BIC_research'
		elif 'wedge-annulus.expand.2min28sec' in mat[i]:
			exp_str = ' Wedge_annulus sequence0 Phase_two_BIC_research'
		elif 'Mixed_TMS_3June2015_2min24s' in mat[i]:
			exp_str = ' Mixed_artists_attend_face_vase ____ TMS_BIC_research'
		else:
			exp_str = ' ____ ____ ____'

		s = mb6[i][0] + ' ' + mat[i] + exp_str
		if i+1<len(mb6):
			s = s+'\n\n'
		info_str_lst += [s]

	with open(ses_str + "/info/session_info.txt", "w") as text_file:
		for s in info_str_lst:
  			text_file.write("%s" % s)



def get_session_info(subject,year,month,day,session,Research_path):
	'''
	'''
	ses_str = Research_path + '/Research/data/subjects/'+subject+'/'+str(year)+'/'+str(month)+'/'+str(day)+'/'+str(session) + '/info'
	with open(ses_str+'/session_info.txt') as f:
		a = f.read()
	b = a.split('\n')

	column_data = []
	ctr = 0
	for c in b:
		if ctr == 0:
			headings = c.split()
		else:
			cd = c.split()
			if len(cd) >0:
				if False:#len(cd) != len(headings):
					print(headings)
					print(cd)
					sys.exit('Error, if len(cd) != len(headings):')
				column_data.append(cd)
		ctr+=1
	dic = {}
	for i in range(len(headings)):
		l = []
		for d in column_data:
			l.append(d[i])
		dic[headings[i]] = l

	return dic #,headings,column_data
