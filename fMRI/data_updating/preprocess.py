import os, sys
if not 'kzpy_initalized' in locals():
    kzpy_initalized = True
    sys.path.append(os.path.join(os.path.expanduser("~")))

import kzpy
from kzpy import *
import kzpy.utils
import kzpy.fMRI.data
import feat_design

# Step one: get the dicom data from a session into a chunking Research- folder
def dcm_to_Research_folders(start_path, end_path, subject, year, month, day, session):
	'''
	Example:
	preprocess.dcm_to_Research_folders('/Users/karlzipser/Desktop/25June2015_backups_of_KK_scanning_from_BIC\ copy/S1_2014_20June2015/Zipser_Pilots\ -\ 1','/Users/karlzipser/Desktop','S1_2014',2015,6,20,0)
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



# Step two: convert dicoms of sessions to Nifti's and place in appropriate Research- folders
def MULTI_dcm2nii(start_path, end_path,to_do,use_PSN=True):
	'''
	start_path = opj(home_path,'Desktop')
	end_path = opj(home_path,'Desktop')
	to_do = [['S4_2015',2015,6,17,0],['S5_2015',2015,6,3,0]]
	kzpy.fMRI.data.preprocess.MULTI_dcm2nii(start_path, end_path,to_do,True)
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
		

# Step three: apply feat to Nifti files, put in appropriate Reserach- folders
def MULTI_feat(start_path, end_path,to_do,TR_s, n_TRs, n_delete_TRs,run_one_in_bkg=True):
	'''

	'''
	#	to_do = [['S4_2015',2015,6,17,0,'align_to_middle_run_of_session','pp_a0']]
	
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
			design = feat_design.get_design(TR_s, n_TRs, n_delete_TRs,
				4,opj(home_path,"Google_Drive/Research/data/protocols/mb6_MosaicRefAcqTimes.txt"),
					0,"",
					opj(nii_path,mb6_nii_align_run_name),opj(fsl_path,mb6_nii_align_run_name))
			design_str = 'design_' + mb6_nii_align_run_name + '.fsf'
			with open(opj(home_path,"Desktop",design_str), "w") as text_file:
				text_file.write(design)
			align_mean_func_path = opj(fsl_path,mb6_nii_align_run_name+'.feat/mean_func')
			os.system('feat '+opj(home_path,"Desktop",design_str))

		ctr = 0
		for i in range(len(mb6_nii_to_align)):
			design = feat_design.get_design(TR_s, n_TRs, n_delete_TRs,
				4,opj(home_path,"Google_Drive/Research/data/protocols/mb6_MosaicRefAcqTimes.txt"),
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

# Step four: add session folders to main Research folder 	


def add_sessions(to_do,Research_path,print_only=True):
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

# Step five: get session information into main Research folder 	

def add_sessions_info(to_do,Research_path):
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



def add_session_info(subject,year,month,day,session,Research_path):
	'''
	'''
	ses_str = Research_path + '/Research/data/subjects/'+subject+'/'+str(year)+'/'+str(month)+'/'+str(day)+'/'+str(session)
	
	mb6 = sort_nii_files(ses_str + '/nii')

	ignore,mat = kzpy.utils.dir_as_dic_and_list(ses_str + '/mat')
	print((len(mb6),len(mat)))
	if len(mb6) != len(mat):
		print('ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
		system.exit('if len(mb6) != len(mat):')

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


# Step six: after manually editing the session_info.txt file for a given session,
# use this to create the runs folders for the session, which bind the mat files
# and the feat folders (and other stuff, if we have it),
# as well as linking the experiments runs to these.

def link_func_runs(subject,year,month,day,session,mc_version,Research_path):
	session_info_dic = get_session_info(subject,year,month,day,session,Research_path)

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
	


##################### local functions ########################

def add_session_paths(subject,year,month,day,session,pp,Research_path,print_only=True):
	'''
	'''
	ses_str0 = 'data/subjects/'+subject+'/'+str(year)+'/'+str(month)+'/'+str(day)+'/'+str(session)
	chunk_str0 = 'data-subjects-'+subject+'-'+str(year)+'-'+str(month)+'-'+str(day)+'-'+str(session)
	ses_prefix = Research_path + '/Research/'
	chunk_prefix = Research_path + '/Research-'
	ses_str = ses_prefix+ses_str0
	chunk_str = chunk_prefix+chunk_str0

	mb6_even,mb6_odd,mb6,t1,fm = kzpy.fMRI.data.preprocess.list_dcm_folders(chunk_str+'-dcm/'+ses_str0+'/dcm') 
	print('\t\t\tC dmc mb6_even:'+str(len(mb6_even)))
	print('\t\t\tC dmc mb6_odd:'+str(len(mb6_odd)))
	print('\t\t\tC dmc mb6:'+str(len(mb6)))
	print('\t\t\tC dmc t1:'+str(len(t1)))
	print('\t\t\tC dmc fm:'+str(len(fm)))

	mb6_lst = kzpy.fMRI.data.preprocess.sort_nii_files(chunk_str+'-nii/'+ses_str0+'/nii')
	print('\t\t\tC nii:'+str(len(mb6_lst)))

	ignore,feat_lst = kzpy.utils.dir_as_dic_and_list(chunk_str+'-fsl-' + pp +'/'+ses_str0+'/fsl/'+pp)
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

	os.chdir(wd)
	
	mb6_even,mb6_odd,mb6,t1,fm = kzpy.fMRI.data.preprocess.list_dcm_folders(ses_str+'/dcm') 
	print('\t\t\tdmc mb6_even:'+str(len(mb6_even)))
	print('\t\t\tdmc mb6_odd:'+str(len(mb6_odd)))
	print('\t\t\tdmc mb6:'+str(len(mb6)))
	print('\t\t\tdmc t1:'+str(len(t1)))
	print('\t\t\tdmc fm:'+str(len(fm)))
	
	mb6_lst = kzpy.fMRI.data.preprocess.sort_nii_files(ses_str+'/nii')
	print('\t\t\tnii:'+str(len(mb6_lst)))
	
	ignore,feat_lst = kzpy.utils.dir_as_dic_and_list(ses_str+'/fsl/'+pp)
	print('\t\t\tfeat:'+str(len(feat_lst)))




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


mb_bold_prefix = 'mb_bold_mb6_20mm_AP_PSN_'
t1_prefix = 't1_mprage_'
fm_prefix = 'gre_field_mapping_16Mar2015_'
mb_nii_suffix = 'a001.nii.gz'




def sort_dcm_folders(path,use_even=True):
	'''
	Example:
	dcm_path = '/Users/karlzipser/Desktop/Research-data-subjects-S1_2014-2015-6-20-0-dcm/data/subjects/S1_2014/2015/6/20/0/dcm'
	mb6,t1,fm = preprocess.sort_dcm_folders(dcm_path)
	len(mb6)
	mb6
	'''
	mb6 = []
	t1 = []
	fm = []
	dr,ls = kzpy.fMRI.data.dir_as_dic_and_list(path)
	for e in ls:
		if e[0:len(mb_bold_prefix)] == mb_bold_prefix:
			n = int(e[len(mb_bold_prefix):])
			use_it = False; # Here I relied on numbering of dcm folder names, but this is not valid. Need to select based on even-odd of sorted files. Make sure total is even.
			if use_even:
				if n%2 == 0:
					use_it = True
			else:
				if n%2 != 0:
					use_it = True
			if use_it:
				p = os.path.join(path,e)
				dr_sub,ls_sub = kzpy.fMRI.data.dir_as_dic_and_list(p)            
				mb6.append([e,n,len(ls_sub)])
        if e[0:len(t1_prefix)] == t1_prefix:
            t1.append(e)
        if e[0:len(fm_prefix)] == fm_prefix:
            fm.append(e)
	mb6.sort(key=lambda x: x[1])
	n_mb6_vols = mb6[0][2]
	for m in mb6:
		if m[2] != n_mb6_vols:
			print(path)
			sys.exit("if m[2] != n_mb6_vols:")
	return mb6,t1,fm


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


def list_dcm_folders(path):
	mb6 = []
	t1 = []
	fm = []
	dr,ls = kzpy.utils.dir_as_dic_and_list(path)
	for e in ls:
		#print(e[0:len(fm_prefix)])
		if e[0:len(fm_prefix)] == fm_prefix:
			fm.append(e)
		if e[0:len(mb_bold_prefix)] == mb_bold_prefix:
			n = int(e[len(mb_bold_prefix):])
			p = os.path.join(path,e)
			dr_sub,ls_sub = kzpy.utils.dir_as_dic_and_list(p)
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


def sort_nii_files(path):
	'''

	'''
	mb6_nii = []
	dr,ls = kzpy.utils.dir_as_dic_and_list(path)
	for e in ls:
		if e[-len(mb_nii_suffix):] == mb_nii_suffix:
			n = int(e[(-len(mb_nii_suffix)-3):(-len(mb_nii_suffix))])             
			mb6_nii.append([e,n])
	mb6_nii.sort(key=lambda x: x[1])
	return mb6_nii




