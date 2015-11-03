import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('127.0.0.1', username='',password='')
stdin,stdout,stderr = ssh.exec_command('pwd;cd ~/Desktop;ls -al;pwd')
print(stdout.read())

import picamera
camera = picamera.PiCamera()
camera.hflip = True
camera.vflip = True
camera.capture('image1.png')