"""
ipython --pylab osx kzpy3/RPi2/keypress_rain.py
"""

from kzpy3.vis import *
from  matplotlib.animation import FuncAnimation


SOC = True

if SOC:
    print "Client Side:"
    import socket
    host = '127.0.0.1' # 'localhost'
    port = 5000
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((host, port))







fig = plt.figure(figsize=(5,5))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0,1), ax.set_xticks([])
ax.set_ylim(0,1), ax.set_yticks([])

def update(frame_number):
    try:
        pass
    except KeyboardInterrupt:
        print('Quitting now.')
        print('\nCleaning up.')
        #sftp.close()
        #transport.close()
        print('Done.')
        sys.exit(1)



def button_press_event(event):
    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        event.button, event.x, event.y, event.xdata, event.ydata)

def motion_notify_event(event):
    print(d2s(event.xdata,event.ydata))
    clientsocket.send(d2s(np.int(100*event.xdata),np.int(100*event.ydata)))

def key_press_event(event):
    #print event.key
    if SOC:
        clientsocket.send(event.key)
    if event.key == 'q':
        if SOC:
            clientsocket.close()
        plt.clf()
        plt.close()
        fig.canvas.mpl_disconnect(cid)
        print('quit!!')
        sys.exit(1)
    else:
        print(event.key)

def figure_leave_event(event):
    print('figure_leave_event')
    clientsocket.send('figure_leave_event')

def figure_enter_event(event):
    print('figure_enter_event')
    clientsocket.send('figure_enter_event')



cid = fig.canvas.mpl_connect('key_press_event', key_press_event)
fig.canvas.mpl_connect('button_press_event', button_press_event)
fig.canvas.mpl_connect('motion_notify_event', motion_notify_event)
fig.canvas.mpl_connect('figure_leave_event', figure_leave_event)
fig.canvas.mpl_connect('figure_enter_event', figure_enter_event)

animation = FuncAnimation(fig, update, interval=10)

plt.plot(40,40,'o')
plt.plot(40,50,'x')

plt.ion()
plt.show()


a=input('afd')
while True:
	pass
