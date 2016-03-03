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
#
#################################
"""
xfm = [
        [
            -0.49957099095280805, 
            -0.02070785171394666, 
            -0.00015375068717687874, 
            56.099478022100556
        ], 
        [
            -0.020706750693901786, 
            0.49946988934948844, 
            0.010054032143392434, 
            42.09083352832065
        ], 
        [
            0.00026283624546495014, 
            -0.010051764031716521, 
            0.49989882666773866, 
            7.980459285840416
        ], 
        [
            0.0, 
            0.0, 
            0.0, 
            1.0
        ]
    ]
xfm = np.array(xfm)
"""


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
	l,r = cortex.db.get_surf(subject, 'flat', merge=False)
	surfaces['lh']['flat'] = l[0]
	surfaces['rh']['flat'] = r[0]
	return surfaces




def display_slice(reference,surfaces,Z):
	mi(reference[:,:,Z],do_clf=True,toolBar=True,do_axis=True,figure_num = Z)
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

for z in [20,30,40]:
	display_slice(reference,surfaces,z)

f =surfaces['lh']['flat']
f -= f.min()
img = np.zeros((f.max()+1,f.max()+1))
for i in range(len(f)):
	img[f[i,0],f[i,1]] += 1
mi(img,100)



"""
tksurfer S12015 lh smoothwm
save patch as: lh.S12015_flat.patch.3d
cd freesurfer/subjects/S12015/surf/
mris_flatten lh.S12015_flat.patch.3d lh.S12015_flat.flat.patch.3d

tksurfer S12015 rh smoothwm
[file:load curvature]
save patch as: rh.S12015_flat.patch.3d
cd freesurfer/subjects/S12015/surf/
mris_flatten rh.S12015_flat.patch.3d rh.S12015_flat.flat.patch.3d
"""