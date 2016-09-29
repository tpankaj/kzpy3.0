from kzpy3.utils import *

"""
from kzpy3.teg1.rosbag_work.preprocess_bag_data import *
bag_folders = gg('/media/karlzipser/bair_car_data_6/bair_car_data/*')
for b in bag_folders[:]:
	try:
		preprocess_bag_data(b)
		save_grayscale_quarter_bagfolder(b)
	except:
		print b + ' failed.'
"""

bair_car_data_path = '/Volumes/data recovery/bair_car_data_6_min'

bair_car_data_folders = gg(opj(bair_car_data_path,'*'))

total_pklbags = 0

for bf in bair_car_data_folders:
	bags = gg(opj(bair_car_data_path,bf,'*.bag'))
	pklbags = gg(opj(bair_car_data_path,bf,'.preprocessed','*.bag.pkl'))

	pklbags_sizes = []
	for p in pklbags:
		sz = os.path.getsize(p)
		if sz > 20000000:
			total_pklbags += 1
		pklbags_sizes.append(sz)
	pklbags_sizes = np.array(pklbags_sizes)

	leftpkl = gg(opj(bair_car_data_path,bf,'.preprocessed','left_image_*'))
	
	if len(pklbags_sizes) > 0:
		stats = (pklbags_sizes.min(),np.int(pklbags_sizes.mean()),pklbags_sizes.max())
	else:
		stats = ('nothing')
	print (stats, bf.split('/')[-1],len(bags),len(pklbags),len(leftpkl))

print d2s("total_pklbags =", total_pklbags)
print d2s("total time =", total_pklbags/2. /60.,"hours")