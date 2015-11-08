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
