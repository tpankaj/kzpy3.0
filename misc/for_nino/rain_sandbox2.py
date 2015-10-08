"""
animate timelapse frames matrix
"""
from kzpy3.vis import *
from matplotlib.animation import FuncAnimation


frames = load_img_folder_to_list(opjh('scratch/2015/9/27/timelapse.1443329409'))
n_frames = len(frames)



def even_frames(frame_number):
	print(frame_number)
	plt.clf()
	mi(frames[frame_number*2])
	if frame_number == n_frames-1:
		plt.close()

def even_frames_motion(frame_number):
	print(frame_number)
	plt.clf()
	f = 10*np.abs((1.0*frames[frame_number*2]-1.0*frames[frame_number*2+1]).mean(axis=2))
	f = np.clip(f,0,255)
	mi(f)
	if frame_number == n_frames-1:
		plt.close()

fig = plt.figure(1,figsize=(9,9))

animation = FuncAnimation(fig, even_frames, frames=n_frames/2-1, interval=3, repeat=False)

plt.show()

print('done....')


