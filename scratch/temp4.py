from kzpy3.utils import *

def temp4(c):
	f = '/Users/karlzipser/Desktop/temp.py'
	t = txt_file_to_list_of_strings(f)
	ctr = 0
	u = '\n'.join(t)
	v = u.split('############\n')
	print('###########\n')
	print(v[c])
	d = raw_input('########### Do this? ')
	if d == 'y':
		exec(v[c],globals())