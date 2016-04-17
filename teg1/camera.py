from kzpy3.utils import *

def camera_on(data_dir=opjD('teg_data/temp')):
	unix('mkdir -p ' + data_dir)
	current_dir = os.getcwd()
	os.chdir(data_dir)
	subprocess.Popen([opjh('kzpy3/teg1/cam15Hz320x240.sh')])
	os.chdir(current_dir)

def camera_off():
	kill_ps('gst-launch-0.10')


"""
img_top_folder = opjD('teg_data/temp3')
_,img_dirs = dir_as_dic_and_list(img_top_folder)
ctimes = []
dt = []
for d in img_dirs:
    ctimes.append(os.path.getmtime(opj(img_top_folder,d)))
for i in range(len(ctimes)-1):
    dt.append(ctimes[i+1]-ctimes[i])
dt = np.array(dt)
print dt.mean()
"""
