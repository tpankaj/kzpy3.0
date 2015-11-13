"""
animate timelapse frames matrix
"""
from kzpy3.vis import *
from matplotlib.animation import FuncAnimation



"""
def load_img_folder_to_dict(img_folder):
    '''Assume that *.* selects only images.'''
    img_fns = gg(opj(img_folder,'*.*'))
    imgs = {}
    for f in img_fns:
        imgs[f.split('/')[-1]] = imread(f)
    return imgs

def load_img_folder_to_list(img_folder):
    return dict_to_sorted_list(load_img_folder_to_dict(img_folder))
"""

def load_txt_folder_to_dict(img_folder):
    ''' '''
    img_fns = gg(opj(img_folder,'*.txt'))
    imgs = {}
    for f in img_fns:
        imgs[f.split('/')[-1]] = txt_file_to_list_of_strings(f)
    return imgs

frames_dic = load_img_folder_to_dict(opjh('Desktop/DATA/VIEWED'))# 'scratch/2015/11/RPi_images/viewed'))# 'scratch/2015/10/8/timelapse.1444316394'))
frames_dic_sortable = {}
for k in frames_dic.keys():
	ctr = k.split('.')[0]
	t = k.split('.')[1]
	t2 = k.split('.')[2]
	if t in frames_dic_sortable:
		print(d2s(t,t2,'in dic already'))
	frames_dic_sortable[t+'.'+t2] = frames_dic[k]
frames = dict_to_sorted_list(frames_dic_sortable)
n_frames = len(frames)

commands_dic = load_txt_folder_to_dict('/Users/karlzipser/Desktop/DATA/EXEC')

command_times = []
for k in sorted(commands_dic.keys()):
	t = k.split('.txt')[0]
	command_times.append(t)

frame_times = []
for k in sorted(frames_dic_sortable.keys()):
	frame_times.append(k)


def even_frames(frame_number):
	print(frame_number)
	plt.clf()
	mi(frames[frame_number])
	if frame_number == n_frames-1:
		plt.close()


fig = plt.figure(1,figsize=(9,9))

animation = FuncAnimation(fig, even_frames, frames=n_frames, interval=3, repeat=False)

plt.show()

print('done....')


