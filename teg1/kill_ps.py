from kzpy3.utils import *

def kill_ps(process_name_to_kill):

	ax_ps_lst = unix('ps ax')

	ps_lst = []

	for p in ax_ps_lst:
		if process_name_to_kill in p:
			ps_lst.append(p)

	pid_lst = []
	for i in range(len(ps_lst)):
		pid = int(ps_lst[i].split(' ')[1])
		pid_lst.append(pid)

	print pid_lst

	for p in pid_lst:
		unix(d2s('kill',p))