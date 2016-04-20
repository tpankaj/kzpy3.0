from kzpy3.utils import *

def make_frame_aliases(input_dir,img_range=()):
	_,fnames = dir_as_dic_and_list(input_dir)
	if len(img_range) == 0:
		img_range = (0,len(fnames))
	temp_dir = opjD('temp'+'_'+input_dir.split('/')[-1])
	unix(d2s('mkdir -p',temp_dir))
	ctr = 0
	for i in range(img_range[0],img_range[1]):
		unix(d2s('ln -s',opj(input_dir,fnames[i]),opj(temp_dir,d2n(ctr,'.jpg'))),False)
		ctr+=1

"""
ffmpeg  -r 15 -i %d.jpg output.gif

ffmpeg -r 15 -i %d.jpg -vcodec mpeg4 -b 990k video.avi
[see http://stackoverflow.com/questions/3158235/image-sequence-to-video-quality]


ffmpeg -i %d.png -pix_fmt yuv420p -r 30 -b:v 14000k temp.mpg

"""





