path = '/media/karlzipser/rosbags1/new'

runs = sgg(opj(path,'*'))

for r in runs:
	n = r.replace('tape','tape_single_transmitter')
	print n
	s = d2s('mv',r,n)
	print s
	unix(s,False)