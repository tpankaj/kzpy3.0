import cortex
import nibabel as nib
from kzpy3.vis import *
import math

def angle_wrt_x(A,B):
    """Return the angle between B-A and the positive x-axis.
    Values go from 0 to pi in the upper half-plane, and from 
    0 to -pi in the lower half-plane.
    http://stackoverflow.com/questions/13543977/python-does-a-module-exist-which-already-find-an-angle-and-the-distance-between
    """
    ax, ay = A
    bx, by = B
    return math.atan2(by-ay, bx-ax)

def dist(A,B):
    ax, ay = A
    bx, by = B
    return math.hypot(bx-ax, by-ay)

def hor_ver(ori):
	if ori >= 0 and ori <= 90:
		return ori
	elif ori > 90 and ori <= 180:
		return 180-ori
	elif ori < 0 and ori >= -90:
		return -ori
	else:
		return 180+ori

test_img = zeros((31,31))
A = (15,15)
for x in range(31):
	for y in range(31):
		B = (x,y)
		test_img[x,y] = hor_ver(np.degrees(angle_wrt_x(A, B)))
mi(test_img,'test_img')






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
rfx = h['voxel_rf_peaks'][1]
rfy = h['voxel_rf_peaks'][0]
rf_ori = 0*rfx
rf_ecc = 0*rfx
A = (64,64)
for i in range(len(rfx)):
	B = (rfx[i],rfy[i])
	theta = angle_wrt_x(A, B)
	d = dist(A, B)
	rf_ori[i] = math.degrees(theta)
	rf_ecc[i] = d

ori_data = zeros((106,106,60)) * np.nan
ecc_data = zeros((106,106,60)) * np.nan
for i in range(shape(selected_voxel_xyzs)[1]):
	x,y,z = selected_voxel_xyzs[:,i]
	ori_data[x,y,z] = hor_ver(rf_ori[i])/90.0 #rf_ecc[i] #
	ecc_data[x,y,z] = rf_ecc[i]/64.0
#data = zeroToOneRange(data)
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
		surfaces[h]['mid0'] = (0.75*surfaces[h]['wm']+0.25*surfaces[h]['pia'])
		surfaces[h]['mid1'] = (0.5*surfaces[h]['wm']+0.5*surfaces[h]['pia'])
		surfaces[h]['mid2'] = (0.25*surfaces[h]['wm']+0.75*surfaces[h]['pia'])
	l,r = cortex.db.get_surf(subject, 'flat', merge=False)
	surfaces['lh']['flat'] = l[0]
	surfaces['rh']['flat'] = r[0]
	return surfaces

def get_pixel_voxel_mappings(surfaces):
	pix_dics = {}
	for h in ['lh','rh']:
		f = surfaces[h]['flat'].copy()
		f -= f.min()
		pix_dics[h] = {}
		bad_center = int(f.max()/2.0) # Don't know why, but the center is a problem.
		for i in range(len(f)):
			for l in ['wm','mid2','mid1','mid0','pia']:
				x,y = int(f[i,0]),int(f[i,1])
				if x == bad_center and y == bad_center:
					pass
				else:
					X,Y,Z = int(surfaces[h][l][i,0]),int(surfaces[h][l][i,1]),int(surfaces[h][l][i,2])
					if (x,y) not in pix_dics[h]:
						pix_dics[h][(x,y)] = []
					pix_dics[h][(x,y)].append((X,Y,Z))
	return pix_dics

def display_slice(reference,surfaces,Z,data,img_title=None):
	if not img_title:
		img_title = Z
	mi(data[:,:,Z]+reference[:,:,Z]/reference.max(),do_clf=True,toolBar=True,do_axis=True,figure_num = img_title)
	pts = np.concatenate((surfaces['lh']['pia'],surfaces['rh']['pia'],surfaces['lh']['wm'],surfaces['rh']['wm']),axis=0)
	pts_lst = []
	for p in range(shape(pts)[0]):
	    if pts[p,2] > Z-0.5 and pts[p,2] < Z+0.5:
	        pts_lst.append(pts[p,:])
	pts_lst = np.array(pts_lst)
	piax = pts_lst[:,0]
	piay = pts_lst[:,1]
	plt.plot(piay,piax,'.',markersize=2)

def red_green(v):
	return [v,1.0-v,0]
def yellow_blue(v):
	return [v,v,1.0-v]


def get_flat_images(surfaces,pix_dics,data,colorizer=red_green):
	flat_imgs = {}
	for h in ['lh','rh']:
		f = surfaces[h]['flat'].copy()
		f -= f.min()
		flat_imgs[h] = np.zeros((f.max()+1,f.max()+1,3))
		for xy in pix_dics[h]:
			x,y = xy
			vox_lst = pix_dics[h][xy]
			ctr = 0.0
			accum = 0.0
			for XYZ in vox_lst:
				X,Y,Z = XYZ
				if not np.isnan(data[X,Y,Z]):
					accum += data[X,Y,Z]
					ctr +=1.0
			if ctr > 0:
				flat_imgs[h][xy[0],xy[1],:] = colorizer(accum/ctr)
			else:
				flat_imgs[h][xy[0],xy[1],:] = 0.5
	return flat_imgs

####################

surfaces = get_surfaces(subject,xfm)

#display_slice(reference,surfaces,25,data)

pix_dics = get_pixel_voxel_mappings(surfaces)

ori_flat_imgs = get_flat_images(surfaces,pix_dics,ori_data,red_green)
ecc_flat_imgs = get_flat_images(surfaces,pix_dics,ecc_data,yellow_blue)

for h in ['lh','rh']:
	mi(ori_flat_imgs[h],h+' ori_data',do_clf=True,toolBar=True,do_axis=True)

for h in ['lh','rh']:
	mi(ecc_flat_imgs[h],h+' ecc_data',do_clf=True,toolBar=True,do_axis=True)






"""
# bkp
flat_imgs = {}
pix_dics = {}
for h in ['lh','rh']:
	f = surfaces[h]['flat'].copy()
	f -= f.min()
	flat_imgs[h] = np.zeros((f.max()+1,f.max()+1))
	pix_dics[h] = {}
	bad_center = int(f.max()/2.0) # Don't know why, but the center is a problem.
	for i in range(len(f)):
		for l in ['wm','mid2','mid1','mid0','pia']:
			x,y = int(f[i,0]),int(f[i,1])
			if x == bad_center and y == bad_center:
				pass
			else:
				X,Y,Z = int(surfaces[h][l][i,0]),int(surfaces[h][l][i,1]),int(surfaces[h][l][i,2])
				if (x,y) not in pix_dics[h]:
					pix_dics[h][(x,y)] = []
				pix_dics[h][(x,y)].append((X,Y,Z))
				flat_imgs[h][x,y] = data[X,Y,Z]#max(data[X,Y,Z],flat_imgs[h][x,y])
	mi(flat_imgs[h],h+' data',do_clf=True,toolBar=True,do_axis=True)
"""



"""
roi_flatmasks = {}
roi_masks = {}
for h in ['lh','rh']:
	roi_flatmasks[h] = flat_imgs[h].copy()
	#roi_flatmask[h][:,int(f.max()*0.5):] = 0
	roi_flatmasks[h][roi_flatmasks[h]<1] = 0
	if h == 'rh':
		pass#roi_flatmasks[h] = v1mask
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





"""
K =  0.035
surfaces = get_surfaces(subject,xfm)
b = surfaces['lh']['pia'].copy()
for i in range(len(b[:,0])):
	if b[i,1] < 20:
		b[i,1] += K*(b[i,1]-65)
surfaces['lh']['pia'] = b
c = surfaces['lh']['wm'].copy()
for i in range(len(b[:,0])):
	if c[i,1] < 20:
		c[i,1] += K*(c[i,1]-65)
surfaces['lh']['wm'] = c
display_slice(reference,surfaces,20,data,'data')


"""




"""
Commands to prepare flat surfaces:

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