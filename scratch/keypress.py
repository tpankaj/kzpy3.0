
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(np.random.rand(10))

def onclick(event):
    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        event.button, event.x, event.y, event.xdata, event.ydata)


def on_key(event):
    print('you pressed', event.key, event.xdata, event.ydata)
    if event.key == 'left':
    	print('GO LEFT!!')
    if event.key == 'right':
    	print('GO RIGHT!!')

cid = fig.canvas.mpl_connect('key_press_event', on_key)

fig.canvas.mpl_disconnect(cid)