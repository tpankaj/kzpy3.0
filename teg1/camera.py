from kzpy3.utils import *

def camera_on(data_dir=opjD('teg_data/temp')):
	unix('mkdir -p ' + data_dir)
	os.chdir(data_dir)
	subprocess.Popen([opjh('kzpy3/teg1/cam15Hz320x240.sh')])

def camera_off():
	kill_ps('gst-launch-0.10')

def kill_ps(process_name_to_kill):
	ax_ps_lst = unix('ps ax',False)
	ps_lst = []
	for p in ax_ps_lst:
		if process_name_to_kill in p:
			ps_lst.append(p)
	pid_lst = []
	for i in range(len(ps_lst)):
		pid = int(ps_lst[i].split(' ')[1])
		pid_lst.append(pid)
	#print pid_lst
	for p in pid_lst:
		unix(d2s('kill',p))
