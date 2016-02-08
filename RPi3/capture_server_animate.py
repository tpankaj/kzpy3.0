import io
import socket
import struct
#from PIL import Image
import time
import numpy as np
from kzpy3.vis import *
from  matplotlib.animation import FuncAnimation

#from  matplotlib.animation import FuncAnimation

img = np.random.random((100,100))
fig = plt.figure(figsize=(7,7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
def update(frame_number):
    plt.clf()
    mi(img)



print 'Start a socket listening for connections'
# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
t = time.time()
t2 = t

ctr = -1
first_time = True
cum_dt = 0
try:
    while True:
        t = time.time()
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(4))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection

        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)

        image = PIL.Image.open(image_stream)
        img = np.asarray(image.convert('RGB'))
        ctr += 1
        #print('Image is %dx%d' % image.size)
        imsave(opjD('temp',d2n(ctr,'.jpg')),img)
        
        if True: #t - t2 > 1:
            t2 = t
            #image.show()
            #print("*************************")
            #img = np.random.rand(10,10)
            #plt.clf()
            #mi(img)
            if first_time:
                animation = FuncAnimation(fig, update, interval=10)
                plt.show()
                start_t = time.time()
                plt.ion()
                plt.show()
                first_time = False
            plt.pause(0.0001)

        if ctr > 0:
            cum_dt += time.time()-t
            if np.mod(ctr,10) == 0:
                print(time.time()-t, (1.0*ctr)/cum_dt,np.shape(img))
        #image.verify()
        #print('Image is verified')
        
finally:
    connection.close()
    server_socket.close()

