import os
import glob
import scipy.io

subject = 'S4_2015'

movie_run_lst = glob.glob("movie_run_*.mat")

for m in movie_run_lst:
	mat = scipy.io.loadmat(m)
	moviename = str(mat['moviename']).split('/')[-1].replace('.avi','').replace("""']""",'')
	date = m[10:18]
	time = m[19:23]
	new_m =  date+time+'_subj'+ subject + '_run00_' + moviename + '.mat'
	os.system('cp ' + m + ' ' + new_m)