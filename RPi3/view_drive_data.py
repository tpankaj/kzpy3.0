from kzpy3.vis import *

fig = plt.figure(figsize=(20,3))
#ax = fig.add_axes([0, 0, 1, 1], frameon=False)

data_dir = '/Users/karlzipser/Desktop/RPi_data/09Feb16_12h10m58s'

_,l=dir_as_dic_and_list(data_dir)
"""
for f in l:
    img = imread(opj(data_dir,f))
    plt.clf()
    plt.ion()
    mi(img)
    plt.show()
    plt.pause(0.03)

"""
def button_press_event(event):
	f = l[np.int(np.floor(event.xdata))]
	print f
 	img = imread(opj(data_dir,f))
 	plt.figure(10)
 	plt.clf()
 	plt.ion()
 	mi(img,10)
 	plt.pause(0.001)
 	plt.figure(1)
 	

fig.canvas.mpl_connect('button_press_event', button_press_event)

timestamp = []
steer = []
speed = []
rps = []
left_range = []
right_range = []
rand_control = []
for m in l:
    n = m.split('_')
    p = n[2].split('=')[1]
    steer.append(p)
    p = n[3].split('=')[1]
    speed.append(p)
    p = n[4].split('=')[1]
    rps.append(p)
    p = n[5].split('=')[1]
    left_range.append(int(p))
    p = n[6].split('=')[1]
    right_range.append(p)
    p = n[7].split('=')[1]
    rand_control.append(p)

lrs = []
lrs.append(left_range[0])
for i in range(1,len(left_range)):
    lrs.append((left_range[i-1]+left_range[i])/2.0)

plt.ion()
plt.plot(steer,'b')
plt.show()
plt.plot(speed,'k')
plt.plot(left_range,'r')
plt.plot(right_range,'g')
plt.plot(rps,'y')


a=input('w')

