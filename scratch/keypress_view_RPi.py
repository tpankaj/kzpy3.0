"""
ipython --pylab osx kzpy3/scratch/keypress_view_RPi.py
ssh pi@192.168.43.20
"""

from kzpy3.vis import *
import numpy as np
import matplotlib.pyplot as plt
from  matplotlib.animation import FuncAnimation

# Create new Figure and an Axes which fills it. 
fig = plt.figure(figsize=(7,7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0,1), ax.set_xticks([])
ax.set_ylim(0,1), ax.set_yticks([])

# Create rain data
n_drops = 50
rain_drops = np.zeros(n_drops, dtype=[('position', float, 2),
                                      ('size',     float, 1),
                                      ('growth',   float, 1),
                                      ('color',    float, 4)])

# Initialize the raindrops in random positions and with
# random growth rates.
rain_drops['position'] = np.random.uniform(0, 1, (n_drops, 2))
rain_drops['growth'] = np.random.uniform(50, 200, n_drops)

# Construct the scatter which we will update during animation
# as the raindrops develop.
scat = ax.scatter(rain_drops['position'][:,0], rain_drops['position'][:,1],
                  s=rain_drops['size'], lw=0.5, edgecolors=rain_drops['color'],
                  facecolors='none')


def update(frame_number):
    start_time = time.time()
    try:
        #c_new = os.path.getctime(opjD('image1.jpg'))
        #if c_new == c:
        #   pass #print('waiting...')
        #else:
        #c = c_new
        #unix(d2n('cp ',opjD('image1.jpg '),' /Users/karlzipser/Desktop/RPi_images/',c_new,'.',ctr,'.jpg'),False)
        #ctr += 1
        #print ctr
        img = imread(opjD('image1.jpg'))
        #print(shape(img))
        if shape(img)[2] == 3:
            plt.clf()
            mi(img)
        else:
            print('Empyt frame.')
    except KeyboardInterrupt:
        print('Quitting now.')
        sys.exit(1)
    except:
        pass
    

# Construct the animation, using the update function as the animation
# director.


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

animation = FuncAnimation(fig, update, interval=10)
plt.show()





a=input('afd')
while True:
	pass
#fig.canvas.mpl_disconnect(cid)