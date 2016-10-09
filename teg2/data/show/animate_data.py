#!/usr/bin/env python
"""
An animated image
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from kzpy3.vis import *
fig = plt.figure(1)

L = load_obj('/home/karlzipser/Desktop/temp_bag_1/play_Nino_to_campus_08Oct16_09h00m00s_Mr_Blue_2/.preprocessed/left_image_bound_to_data2.pkl')
P = load_obj('/home/karlzipser/Desktop/temp_bag_1/play_Nino_to_campus_08Oct16_09h00m00s_Mr_Blue_2/.preprocessed/bair_car_2016-10-08-09-54-56_98.bag.pkl')

ctr = 0
skip = 0
shown = 0.0

ts = sorted(P['left'].keys())
imgs = []
for t in ts:
	imgs.append(P['left'][t]/255.)
t0 = time.time()
steers = list(49+zeros(20))
def updatefig(*args):
	global ctr, shown, skip
	while ts[ctr]-ts[0]<time.time()-t0:
		ctr += 1
		skip += 1
		steers.append(L[ts[ctr]]['steer'])
		
	shown=shown+1
	print d2s('skip/shown =', ctr/shown)
	mi(imgs[ctr],1) #P['left'][ts[ctr]]/.255.,1)
	#plt.figure(1)
	#plt.clf()
	#plt.imshow(imgs[ctr],cmap='gray') #P['left'][ts[ctr]]/.255.,1)
	plt.figure(2)
	plt.clf()
	
	steers.append(L[ts[ctr]]['steer'])
	plt.plot(99-np.array(steers[-20:]),range(20))
	plt.ylim((0,20))
	plt.xlim((-5,105))

ani = animation.FuncAnimation(fig, updatefig, interval=1)#, blit=True)

plt.show()