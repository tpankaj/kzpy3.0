############
print(1+np.sqrt(7))

############
############
############
############
############
"""
ipython --pylab osx kzpy3/scratch/keypress.py
"""

from kzpy3.vis import *

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(np.random.rand(10))

def onclick(event):
    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        event.button, event.x, event.y, event.xdata, event.ydata)


def on_key(event):
    
    if event.key == 'left':
    	print('GO LEFT!!')
    elif event.key == 'right':
    	print('GO RIGHT!!')
    elif event.key == 'q':
    	plt.clf()
    	plt.close()
    	fig.canvas.mpl_disconnect(cid)
    	print('quit!!')
    	sys.exit(1)
    else:
    	print('you pressed', event.key, event.xdata, event.ydata)


cid = fig.canvas.mpl_connect('key_press_event', on_key)
a=input('afd')
while True:
	pass
#fig.canvas.mpl_disconnect(cid)

############

def krn(c):
	f = opjh('kzpy3/scratch/2015/12/scratch_script.py')
	t = txt_file_to_list_of_strings(f)
	ctr = 0
	u = '\n'.join(t)
	v = u.split('############\n')
	print('###########\n')
	print(v[c])
	d = raw_input('########### Do this? ')
	if d == 'y':
		exec(v[c],globals())

############
############

a = 1+1
b = 3
c = a**b
print(c)

############

from kzpy3.vis import *
p = imread(opjh('Pictures/bay2.png'))
mi(p,3,img_title='shit')

############

a = 1+1
b = 3
c = a-b
print(c)

############

def krun(c):
	f = opjh('kzpy3/scratch/2015/12/scratch_script.py')
	t = txt_file_to_list_of_strings(f)
	ctr = 0
	u = '\n'.join(t)
	v = u.split('############\n')
	print('###########\n')
	print(v[c])
	d = raw_input('########### Do this? ')
	if d == 'y':
		exec(v[c],globals())

############


