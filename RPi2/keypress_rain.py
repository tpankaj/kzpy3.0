"""
ipython --pylab osx kzpy3/scratch/keypress.py
"""

from kzpy3.vis import *
from  matplotlib.animation import FuncAnimation




print "Client Side:"
import socket
host = '127.0.0.1' # 'localhost'
port = 5000
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((host, port))








# Create new Figure and an Axes which fills it. 
fig = plt.figure(figsize=(1,1))


def update(frame_number):
    pass

def onclick(event):
    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        event.button, event.x, event.y, event.xdata, event.ydata)


def on_key(event):
    print event.key
    clientsocket.send(event.key)
    if event.key == 'q':
        clientsocket.close()
    	plt.clf()
    	plt.close()
    	fig.canvas.mpl_disconnect(cid)
    	print('quit!!')
    	sys.exit(1)
    else:
    	print(event.key, event.xdata, event.ydata)



    



cid = fig.canvas.mpl_connect('key_press_event', on_key)
fig.canvas.mpl_connect('button_press_event', onclick)
#fig.canvas.mpl_connect('motion_notify_event', onclick)


animation = FuncAnimation(fig, update, interval=10)
plt.ion()
plt.show()





a=input('afd')
while True:
	pass
#fig.canvas.mpl_disconnect(cid)