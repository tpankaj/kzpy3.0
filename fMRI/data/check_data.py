##################################
# - my standard initialization
# note, need to:
#   ln -s ~/Google_Drive/py/kzpy1 ~/kzpy to set up use of kzpy
import os, sys
if not 'kzpy_initalized' in locals():
    kzpy_initalized = True
    sys.path.append(os.path.join(os.path.expanduser("~")))
from kzpy import *
import kzpy.img
import kzpy.fMRI.vis
import kzpy.fMRI.data
import kzpy.fMRI.rf
#import kzpy.fMRI.reformat_stimuli_for_analysis
import kzpy.fMRI.utils
from kzpy.fMRI.utils import *
from kzpy.utils import *

#import kzpy.external.pyramids
#reload(kzpy)
#reload(kzpy.img)
#reload(kzpy.fMRI.vis)
#reload(kzpy.fMRI.data)
#reload(kzpy.fMRI.rf)
#reload(kzpy.fMRI.reformat_stimuli_for_analysis)
#reload(kzpy.fMRI.utils)
#reload(kzpy.external.pyramids)
#from kzpy import np, plt, pylab, scipy, glob, nib
from kzpy.img import mi
from kzpy.img import ProgressBar
from kzpy.utils import natural_keys
opj = os.path.join
PP,FF = pylab.rcParams,'figure.figsize'
PP[FF]=(6,6)
#%matplotlib inline
##################################

	
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



'''
#################

if True:
	p2Re = '/Users/karlzipser/Google_Drive/Research'
	wd = os.getcwd()
	os.chdir(p2Re)
	True



cd /Users/karlzipser/Google_Drive/2015/6/26June2015_data_processing/		
import check_data;reload(check_data);from check_data import *
'''

'''
p2Re = '/Users/karlzipser/Google_Drive/Research'
deKKv = 'data/experiments/Kendrick_Kay_visit_19to26June2015'

Research = {}

wd = os.getcwd()
os.chdir(p2Re)
func_runs_mc_path = deKKv+'/Wedge_annulus/sequence2/subjects/S1_2014/2015/6/20/0/func_runs/mc_20150620_110252mbboldmb620mmAPPSNs003a001/'
nii_files = ['filtered_func_data.nii.gz','mean_func.nii.gz','mask.nii.gz']
feat_paths = load_func_runs(func_runs_mc_path,Research,nii_files)
os.chdir(wd)


experiment_strs = ['Vermeer/attend_face','Vermeer/attend_object','Vermeer/attend_space']
for es in experiment_strs:
	func_runs_mc_path = deKKv+'/' + es + '/subjects/S1_2014/2015/6/20/0/func_runs/mc_20150620_110252mbboldmb620mmAPPSNs003a001/'
	load_func_runs(func_runs_mc_path,Research,['filtered_func_data.nii.gz','mean_func.nii.gz','mask.nii.gz'])




ffd2 = Research[opj(feat_paths[0],'filtered_func_data.nii.gz:data')]
ffd3 = Research[opj(feat_paths[1],'filtered_func_data.nii.gz:data')]
msk2 = Research[opj(feat_paths[0],'mask.nii.gz:data')]
msk3 = Research[opj(feat_paths[1],'mask.nii.gz:data')]

fig = 1
for fp in feat_paths:
	d = Research[opj(fp,'mean_func.nii.gz:data')]
	mi(d[:,:,np.round(np.shape(d)[2]/2)],fig,[2,2,1])
	mi(np.rot90(d[:,np.round(np.shape(d)[1]/2),:]),fig,[2,2,2],'run ' + os.path.split(rp)[1])
	mi(np.rot90(d[np.round(np.shape(d)[0]/2),:,:]),fig,[2,2,3])
	mcf = plt.figure(fig).add_subplot(2,2,4)
	plt.plot(Research[opj(fp,'mc/prefiltered_func_data_mcf_rel.rms')])
	mcf.set_ylim([0,0.2])
	fig += 1




runs=[]
for k in Research.keys():
    if str_contains(k,['Wedge_annulus','sequence1','filtered',':data']):
        runs.append(k)
runs.sort(key=natural_keys)

even_runs = runs[0:][::2]
odd_runs = runs[1:][::2]

oa = get_runs_average(odd_runs)
ea = get_runs_average(even_runs)
aa = get_runs_average(runs)
figure(20)
plt.plot(oa[53,16,16,:]-np.mean(oa[53,16,16,:]))
plt.plot(ea[53,16,16,:]-np.mean(ea[53,16,16,:]))
plt.plot(aa[53,16,16,:]-np.mean(aa[53,16,16,:]))


np.save('/Users/karlzipser/Desktop/aa.npy',aa)

from matplotlib.backends.backend_pdf import PdfPages
pp = PdfPages('multipage.pdf')
pp.savefig()
pp.close()


######################
# - make avg. r_volume for session
experiment_strs = ['Vermeer/attend_face','Vermeer/attend_object','Vermeer/attend_space','Wedge_annulus/sequence1','Wedge_annulus/sequence2']
r_vols={}
r_vol_avg = 0.0*r_volume1
r_vol_paths = []
for es in experiment_strs:
	print(es)
	r_vol_path = func_runs_mc_path = deKKv+'/' + es + '/subjects/S1_2014/2015/6/20/0/stats/mc_20150620_110252mbboldmb620mmAPPSNs003a001/r_volume.nii.gz'
	r_vol_paths.append(r_vol_path)
	nii = nib.load(r_vol_path)
	img = nii.get_data()
	r_vols[r_vol_path+':data']=img
	header = nii.get_header()
	r_vols[r_vol_path+':header']=img
	affine = nii.get_affine()
	r_vols[r_vol_path+':affine']=img
	r_vol_avg += img
	print('here')

r_vol_avg /= (1.0*len(r_vol_paths))
#
######################

######################
# 4 July 2015, map RF centers with two sequences
from check_data import *
from pRF import *
hrf = KK_getcanonicalhrf()
r_sorted_xyz_list = np.load('/Users/karlzipser/Google_Drive/Research/data/subjects/S1_2014/2015/6/20/0/stats/mc_20150620_110252mbboldmb620mmAPPSNs003a001/r_sorted_xyz_list.npy')

Research={}
os.chdir(p2Re)
mc1p='data/experiments/Kendrick_Kay_visit_19to26June2015/Wedge_annulus/sequence1/subjects/S1_2014/2015/6/20/0/stats/mc_20150620_110252mbboldmb620mmAPPSNs003a001'
mc2p='data/experiments/Kendrick_Kay_visit_19to26June2015/Wedge_annulus/sequence2/subjects/S1_2014/2015/6/20/0/stats/mc_20150620_110252mbboldmb620mmAPPSNs003a001'
load_stat_dir(mc1p,Research)
load_stat_dir(mc2p,Research)

aa1 = Research[select_keys(Research,['all_average','sequence1',':data'])[0]]
aa2 = Research[select_keys(Research,['all_average','sequence2',':data'])[0]]
TR_times = 0.9 * np.arange(0,np.shape(aa1)[3])

s1,frame_5Hz_times = sequence(1)
sc1 = convolve_s_with_hrf(s1,frame_5Hz_times,hrf,TR_times)
s2,frame_5Hz_times = sequence(2)
sc2 = convolve_s_with_hrf(s2,frame_5Hz_times,hrf,TR_times)

s1_peaks = {}
s2_peaks = {}
s1s2_r = {}
for i in range(30000):#len(r_sorted_xyz_list)):
	ni = -(i+1)
	xyz = tuple(r_sorted_xyz_list[ni])
	rf1,peak1 = rf_peak_xy(sc1,aa1[tuple(r_sorted_xyz_list[ni])],TR_times,'sc1',False)
	rf2,peak2 = rf_peak_xy(sc2,aa2[tuple(r_sorted_xyz_list[ni])],TR_times,'sc2',False)
	s1_peaks[xyz] = peak1
	s2_peaks[xyz] = peak2
	s1s2_r[xyz] = np.corrcoef(np.reshape(rf1,96*128),np.reshape(rf2,96*128))[0,1]
	print((ni,xyz,s1_peaks[xyz],s2_peaks[xyz],s1s2_r[xyz]))
	if i%1000 == 0:
		pickle.dump(s1_peaks,open("/Users/karlzipser/Desktop/s1_peaks."+str(i)+".p","wb"))
		pickle.dump(s2_peaks,open("/Users/karlzipser/Desktop/s2_peaks."+str(i)+".p","wb"))
		pickle.dump(s1s2_r,open("/Users/karlzipser/Desktop/s1s2_r."+str(i)+".p","wb"))
#
########################


'''



True
