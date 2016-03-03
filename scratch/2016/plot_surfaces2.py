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
	"""
	Use pycortex functionality to load white matter and pial surfaces.
	Generate mid-depth surface(s)
	"""
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


def display_slice(reference,surfaces,Z,data,img_title=Z):
	mi(data[:,:,Z]+reference[:,:,Z]/reference.max(),do_clf=True,toolBar=True,do_axis=True,figure_num = img_title)
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


display_slice(reference,surfaces,25,data)



pix_dics = {}
flat_imgs = {}

for h in ['lh','rh']:
	f =surfaces[h]['flat'].copy()
	f -= f.min()
	flat_imgs[h] = np.zeros((f.max()+1,f.max()+1))
	pix_dics[h] = {}
	bad_center = int(f.max()/2.0)
	for i in range(len(f)):
		for l in ['wm','mid','pia']:
			x,y = int(f[i,0]),int(f[i,1])
			if x == bad_center and y == bad_center:
				pass
			else:
				X,Y,Z = int(surfaces[h][l][i,0]),int(surfaces[h][l][i,1]),int(surfaces[h][l][i,2])
				if (x,y) not in pix_dics[h]:
					pix_dics[h][(x,y)] = []
				pix_dics[h][(x,y)].append((X,Y,Z))
				flat_imgs[h][x,y] = max(data[X,Y,Z],flat_imgs[h][x,y])
	mi(flat_imgs[h],h+' data',do_clf=True,toolBar=True,do_axis=True)


roi_flatmasks = {}
roi_masks = {}
for h in ['lh','rh']:
	roi_flatmasks[h] = flat_imgs[h].copy()
	#roi_flatmask[h][:,int(f.max()*0.5):] = 0
	roi_flatmasks[h][roi_flatmasks[h]<1] = 0
	if h == 'rh':
		roi_flatmasks[h] = v1mask
	mi(roi_flatmasks[h],'roi_flatmask '+h)
	roi_masks[h] = 0*reference
	r = np.where(roi_flatmasks[h] > 0)
	for i in range(len(r[0])):
		x = r[0][i]
		y = r[1][i]
		XYZs = pix_dics[h][(x,y)]
		for xyz in XYZs:
			roi_masks[h][xyz[0],xyz[1],xyz[2]] = 1
	display_slice(reference,surfaces,25,roi_masks[h],'roi '+h)

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