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
# 29 Feb. 2016
# This shows the process needed for marking visual areas
view = cortex.Volume.random("__S12015","one",cmap="hot")

cortex.add_roi(view,'A2')

rois = cortex.get_roi_verts('__S12015', roi='A3')
v3=rois['A3']

mapper = cortex.get_mapper('__S12015','one')
l,r = mapper.backwards(v3)
mask = l+r

view.data = mask
img = cortex.quickflat.make(view)
mi(img[0],4)

mi(mask.mean(axis=0),22)

"""


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