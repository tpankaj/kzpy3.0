path = '/media/karlzipser/rosbags1/new'

runs = sgg(opj(path,'*'))

for r in runs:
	n = r.replace('auto_start','snow')
	print n
	s = d2s('mv',r,n)
	print s
	unix(s,False)