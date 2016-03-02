wmpts, polys = surfs.get_surf('S1', 'wm', merge=True)
wmlst = []
for p in range(shape(wmpts)[0]):
	if wmpts[p,2] > 20 and wmpts[p,2] < 21:
		wmlst.append(wmpts[p,:])
wmlst = np.array(wmlst)
wmx = wmlst[:,0]
wmy = wmlst[:,1]
plt.clf()
plt.plot(wmx,wmy,'o')

piapts, polys = surfs.get_surf('S1', 'pia', merge=True)
pialst = []
for p in range(shape(piapts)[0]):
	if piapts[p,2] > 20 and piapts[p,2] < 21:
		pialst.append(piapts[p,:])
pialst = np.array(pialst)
piax = pialst[:,0]
piay = pialst[:,1]
#plt.clf()
plt.plot(piax,piay,'o')

flatapts, polys = surfs.get_surf('S1', 'flat', merge=True)
flatlst = []
for p in range(shape(piapts)[0]):
	if piapts[p,2] > 20 and piapts[p,2] < 21:
		flatlst.append(flatpts[p,:])
flatlst = np.array(flatlst)
flatx = flatlst[:,0]
flaty = flatlst[:,1]
plt.figure(2)
plt.plot(flatx,flaty,'o')



"""
tksurfer S12015 lh smoothwm
tksurfer S12015 rh smoothwm
mris_flatten -O fiducial /Users/karlzipser/freesurfer/subjects/S12015/surf/lh.flatten.patch.3d /Users/karlzipser/freesurfer/subjects/S12015/surf/lh.flat.patch
mris_flatten -O fiducial /Users/karlzipser/freesurfer/subjects/S12015/surf/rh.flatten.patch.3d /Users/karlzipser/freesurfer/subjects/S12015/surf/rh.flat.patch



# 29 Feb. 2016
# This shows the process needed for marking visual areas
import cortex
view = cortex.Volume.random("S12015","mc_to_006a_of_9Feb2015",cmap="hot")

#cortex.add_roi(view,'A2')

rois = cortex.get_roi_verts('S12015', roi='V1')
v1=rois['V1']

mapper = cortex.get_mapper('S12015','mc_to_006a_of_9Feb2015')
l,r = mapper.backwards(v1)
mask = l+r

#view.data = mask
#img = cortex.quickflat.make(view)
#mi(img[0],4)

#mi(mask.mean(axis=0),22)

import h5py
f = h5py.File('/Users/karlzipser/2015/10/2015-10/HVO_RF_mapping.736252.5459.mat','r')
h = f['HVO_RF_mapping']
selected_voxel_xyzs = h[u'selected_voxel_xyzs'][:,:]
selected_voxel_xyzs -= 1 # matlab to python indexing

rmask = zeros((60,106,106))+0.5

for i in range(shape(selected_voxel_xyzs)[1]):
	x,y,z = selected_voxel_xyzs[:,i]
	rmask[z,y,x] = 1
# rmask[y,z,x]
# 	rmask[z,x,y]
view.data = rmask
fig = cortex.quickflat.make_figure(view,depth=0.5,thick=32,sampler='trilinear')

img = cortex.quickflat.make(view)
plt.clf()
mi(img[0],4)
cortex.webshow((rmask,"S12015","mc_to_006a_of_9Feb2015")) #[note,, __S12015 doesn't work]
"""


# mris_convert -p lh.flat.patch flat_lh.gii

"""
import cortex
from kzpy3.vis import *
plt.ion()
plt.show()
view = cortex.Volume.random("S12015","one",cmap="hot")
cortex.add_roi(view,'A1')
rois = cortex.get_roi_verts('S12015', roi='NEW12');rois
lh,rh = cortex.db.get_surf('S12015','flat')

img = np.zeros((500,500))
for i in range(len(rh[0])):
    x=rh[0][i,0]+250
    y=rh[0][i,1]+250
    if img[x,y] < 5:
    	img[x,y]+=1
plt.clf()
mi(img)

img = np.zeros((500,500))
for i in range(len(lh[0])):
    x=lh[0][i,0]+250
    y=lh[0][i,1]+250
    if img[x,y] < 5:
    	img[x,y]+=1
plt.clf()
mi(img,2)



import cortex
view = cortex.Volume.random("S1","fullhead",cmap="hot")

X,Y,Z = shape(view.data)
for x in range(X):
	for y in range(Y):
		for z in range(Z):
			view.data[x,y,z] = y
			if np.random.random(1) > 0.9:
				view.data[x,y,z] = 25
view.data[:,:,Y/2-4]=101
fig=cortex.quickflat.make_figure(view)
im[np.isnan(im)]=0
plt.figure(2);plt.clf()
mi(im,2)
#cortex.quickflat.make_png(opjD('temp2.png'),view)



from kzpy3.vis import *
plt.ion()
plt.show()
view = cortex.Volume.random("S1","fullhead",cmap="hot")
rois = cortex.get_roi_verts('S12015', roi='NEW12');rois
v1=rois['NEW12']

lh,rh = cortex.db.get_surf('S1','flat')

img = np.zeros((500,500))

for i in range(len(lh[0])):
    x=lh[0][i,0]+250
    y=lh[0][i,1]+250
    if img[x,y] < 5:
    	img[x,y]+=1

for i in range(len(v1)):
	j = v1[i]
	try:
	    x=lh[0][j,0]+250
	    y=lh[0][j,1]+250
	    img[x,y]=5
	except:
		pass

mapper = cortex.get_mapper('__S12015','one')
l,r = mapper.backwards(v1)
mask = l+r
plt.figure(20)
plt.clf()
mi(mask.mean(axis=0),20)

plt.figure(10)
plt.clf()
mi(img,10)



"""