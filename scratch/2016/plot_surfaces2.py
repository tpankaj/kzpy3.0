import cortex
import nibabel as nib
from kzpy3.vis import *

db_path = '/anaconda/share/pycortex/db'

########## specific data #########
#
subject = 'S12015'
transform_name = '9Feb2015'
reference = (nib.load(opj(db_path,subject,'transforms',transform_name,'reference.nii.gz'))).get_data()
xfm = np.load(opj(db_path,subject,'transforms',transform_name,'coord.npy'))

import h5py
f = h5py.File('/Users/karlzipser/2015/10/2015-10/HVO_RF_mapping.736252.5459.mat','r')
h = f['HVO_RF_mapping']
selected_voxel_xyzs = h['selected_voxel_xyzs'][:,:]
selected_voxel_xyzs -= 1 # matlab to python indexing
data = zeros((106,106,60))+0.5
for i in range(shape(selected_voxel_xyzs)[1]):
	x,y,z = selected_voxel_xyzs[:,i]
	data[x,y,z] = 1
#
#################################



def get_surfaces(subject,xfm):
	surfaces = {}
	surfaces['lh'] = {}
	surfaces['rh'] = {}
	for t in ['wm','pia']:
		l,r = cortex.db.get_surf(subject, t, merge=False)
		surfaces['lh'][t] = (xfm[:3,:3].dot(l[0].T)).T
		surfaces['rh'][t] = (xfm[:3,:3].dot(r[0].T)).T
		for i in range(3):
			surfaces['lh'][t][:,i] += xfm[i,3]
			surfaces['rh'][t][:,i] += xfm[i,3]
	for h in ['lh','rh']:
		surfaces[h]['mid'] = (0.5*surfaces[h]['wm']+0.5*surfaces[h]['pia'])
	l,r = cortex.db.get_surf(subject, 'flat', merge=False)
	surfaces['lh']['flat'] = l[0]
	surfaces['rh']['flat'] = r[0]
	return surfaces


def display_slice(reference,surfaces,Z,data):
	mi(data[:,:,Z]+reference[:,:,Z]/reference.max(),do_clf=True,toolBar=True,do_axis=True,figure_num = Z)
	#pts = np.concatenate((surfaces['lh']['pia'],surfaces['rh']['pia'],surfaces['lh']['mid'],surfaces['rh']['mid'],surfaces['lh']['wm'],surfaces['rh']['wm']),axis=0)
	pts = np.concatenate((surfaces['lh']['pia'],surfaces['rh']['pia'],surfaces['lh']['wm'],surfaces['rh']['wm']),axis=0)
	pts_lst = []
	for p in range(shape(pts)[0]):
	    if pts[p,2] > Z-0.5 and pts[p,2] < Z+0.5:
	        pts_lst.append(pts[p,:])
	pts_lst = np.array(pts_lst)
	piax = pts_lst[:,0]
	piay = pts_lst[:,1]
	plt.plot(piay,piax,'.',markersize=2)


####################

surfaces = get_surfaces(subject,xfm)


for z in range(1,60):
	display_slice(reference,surfaces,z,data)




for h in ['lh','rh']:
	f =surfaces[h]['flat']
	f -= f.min()
	img = np.zeros((f.max()+1,f.max()+1))
	for i in range(len(f)):
		for l in ['wm','mid','pia']:
			img[int(f[i,0]),int(f[i,1])] = max(rmask[surfaces[h][l][i,0],surfaces[h][l][i,1],surfaces[h][l][i,2]],img[int(f[i,0]),int(f[i,1])])
	mi(img,h)

roi_flatmask = img.copy()
roi_flatmask[:int(f.max()*0.7),:int(f.max()*0.7)] = 0
roi_flatmask[roi_flatmask<1] = 0
mi(roi_flatmask,'roi_flatmask')

"""
tksurfer S12015 lh smoothwm
save patch as: lh.S12015_flat.patch.3d
cd freesurfer/subjects/S12015/surf/
mris_flatten lh.S12015_flat.patch.3d lh.S12015_flat.flat.patch.3d
mris_convert -p lh.S12015_flat.flat.patch.3d flat_lh.gii

tksurfer S12015 rh smoothwm
[file:load curvature]
save patch as: rh.S12015_flat.patch.3d
cd freesurfer/subjects/S12015/surf/
mris_flatten rh.S12015_flat.patch.3d rh.S12015_flat.flat.patch.3d
mris_convert -p rh.S12015_flat.flat.patch.3d.out flat_rh.gii
"""