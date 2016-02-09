from kzpy3.vis import *

fig = plt.figure(figsize=(5,5))
#ax = fig.add_axes([0, 0, 1, 1], frameon=False)

_,l=dir_as_dic_and_list('/Users/karlzipser/Desktop/RPi_data/09Feb16_08h17m57s')

def button_press_event(event):
	f = l[np.int(np.floor(event.xdata))]
	print f
 	img = imread(opj('/Users/karlzipser/Desktop/RPi_data/09Feb16_08h17m57s',f))
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
    left_range.append(p)
    p = n[6].split('=')[1]
    right_range.append(p)
    p = n[7].split('=')[1]
    rand_control.append(p)

plt.ion()
plt.plot(steer,'g')
plt.show()


