import sys
sys.path.insert(0, "/home/pi")
from kzpy3.utils import *
import picamera
import paramiko

#paramiko.util.log_to_file(opjD('paramiko.log'))
hup = txt_file_to_list_of_strings('/home/pi/pw_MacbookPro.txt')
host = hup[0]
port = 22
transport = paramiko.Transport((host, port))

password = hup[2]
username = hup[1]
transport.connect(username = username, password = password)
sftp = paramiko.SFTPClient.from_transport(transport)


camera = picamera.PiCamera()
camera.hflip = True
camera.vflip = True
ydim = 224
camera.resolution = (np.int(1.3333*ydim), ydim)

image_path = '/home/pi/image1.jpg'
dst_image_path = '/Users/karlzipser/Desktop/RPi'

camera_on_time = 600
start_time = time.time()
last_time = start_time

ctr = 0
time_sum = 0
while time.time() < start_time + camera_on_time:
	try:
		t = time.time()
		ctr += 1
		time_sum += t-last_time
		if np.mod(ctr,100) == 0:
			print(d2s('Average interval =',time_sum / (1.0*ctr)))
		last_time = t
		camera.capture(image_path,format='jpeg', use_video_port=True,quality=10)
		sftp.put(image_path, '/Users/karlzipser/Desktop/image1.jpg')
		#sftp.put(image_path, opj(dst_image_path,d2n(ctr,'.jpg')))
	except:
		break
    
print('\nCleaning up.')
sftp.close()
transport.close()
print('Done.')

"""
from kzpy3.utils import *
import picamera
import paramiko

paramiko.util.log_to_file(opjD('paramiko.log'))
host = "example.com"
port = 22
transport = paramiko.Transport((host, port))
password = "foo"
username = "bar"
transport.connect(username = username, password = password)
sftp = paramiko.SFTPClient.from_transport(transport)

camera = picamera.PiCamera()
camera.hflip = True
camera.vflip = True

image_path = opjD('image1.jpg')
dst_image_path = '/Users/karlzipser/Desktop/image1.jpg'

camera_on_time = 300
start_time = time.time()

while time.time() < start_time + camera_on_time:
	print(time.time())
	camera.capture(image_path,quality=25)
	sftp.put(image_path, dst_image_path)
	#time.sleep(0.2)

sftp.close()
transport.close()






from kzpy3.utils import *
import picamera
import paramiko

#paramiko.util.log_to_file(opjD('paramiko.log'))
host = ""
port = 22
transport = paramiko.Transport((host, port))
password = ""
username = ""
transport.connect(username = username, password = password)
sftp = paramiko.SFTPClient.from_transport(transport)

camera = picamera.PiCamera()
camera.hflip = True
camera.vflip = True
camera.resolution = (640, 480)

image_path = '/home/pi/image1.jpg'
dst_image_path = '/Users/karlzipser/Desktop/image1.jpg'

camera_on_time = 300
start_time = time.time()
last_time = start_time


while time.time() < start_time + camera_on_time:
    print(time.time()-last_time)
    last_time=time.time()
    camera.capture(image_path,format='jpeg', use_video_port=True,quality=15)
    sftp.put(image_path, dst_image_path)

sftp.close()
transport.close()
"""
