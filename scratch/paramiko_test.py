import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('127.0.0.1', username='karlzipser',password='')
stdin,stdout,stderr = ssh.exec_command('pwd;cd ~/Desktop;pwd')
print(stdout.read())