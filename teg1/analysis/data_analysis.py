
data_dic = {}

data_dic['GPS'] = {}
data_dic['acc'] = {}

data_filepathname = '/Volumes/ZBDD_4TB/teg_data/_18Apr16_16h49m55s.GPS_acc.txt'
frame_folder = '/Volumes/ZBDD_4TB/teg_data/_18Apr16_17h16m35s_caffe'

def data_to_dic(data_filepathname,data_dic):
	r = txt_file_to_list_of_strings(data_filepathname)
	for b in r:
		if 'GPS' in b:
			try:
				exec('c='+b)

				data_dic['GPS'][c[-1]] = c[1:-1]
			except Exception,e:
				print e
		elif 'acc' in b:
			exec('c='+b)
			g.append(c)
			data_dic['acc'][c[-1]] = c[1:-1]


data_to_dic(data_filepathname,data_dic)

acc_t = sorted(data_dic['acc'])
xa = []
ya = []
za = []

for t in acc_t:
	xyz = data_dic['acc'][t]
	xa.append(xyz[0])
	ya.append(xyz[1])
	za.append(xyz[2])

plt.plot(acc_t,za,'b')
plt.plot(smooth(np.array(za),window_len=50),'r')
"""
lat = []
lon = []
for d in g:
	lat.append(d[1])
	lon.append(d[2])
"""



frame_to_ctime_dic = {}
ctime_to_frame_dic = {}

path_to_frame_folder = '/Volumes/ZBDD_4TB/teg_data'
frame_folder = '_18Apr16_17h29m15s_caffe'
_,frame_names = dir_as_dic_and_list(opj(path_to_frame_folder,frame_folder))
for f in frame_names:
	ctime = os.path.getctime(opj(path_to_frame_folder,frame_folder,f))
	#ctime += 3600 #!!!!!!! Note, the ctimes on the frames are not on daylight savings time !!!!!!
	frame_to_ctime_dic[opj(frame_folder,f)] = ctime
	ctime_to_frame_dic[ctime] = opj(frame_folder,f)




# http://www.scipy.org/Cookbook/SignalSmooth
def smooth(x,window_len=11,window='hanning'):
        if x.ndim != 1:
                raise ValueError, "smooth only accepts 1 dimension arrays."
        if x.size < window_len:
                raise ValueError, "Input vector needs to be bigger than window size."
        if window_len<3:
                return x
        if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
                raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"
        s=numpy.r_[2*x[0]-x[window_len-1::-1],x,2*x[-1]-x[-1:-window_len:-1]]
        if window == 'flat': #moving average
                w=numpy.ones(window_len,'d')
        else:  
                w=eval('numpy.'+window+'(window_len)')
        y=numpy.convolve(w/w.sum(),s,mode='same')
        return y[window_len:-window_len+1]
