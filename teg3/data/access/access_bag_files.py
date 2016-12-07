from kzpy3.vis import *
import kzpy3.teg3.data.access.Bag_Folder as Bag_Folder
import kzpy3.teg3.data.access.Bag_File as Bag_File
from kzpy3.teg3.data.preprocess.preprocess_Bag_Folders import get_preprocess_dir_name_info as get_preprocess_dir_name_info
import cv2

def load_Bag_Folders(bag_folders_path = opjD('runs')):

	BF_dic = {}

	bag_folders_paths_list = sorted(gg(opj(bag_folders_path,'*')),key=natural_keys)

	for bfp in bag_folders_paths_list:

		run_name = bfp.split('/')[-1]

		preprocessed_dir,left_image_bound_to_data_name = get_preprocess_dir_name_info(bfp)

		if len(gg(opj(bfp,preprocessed_dir,'Bag_Folder.pkl'))) == 1:
			print('')
			cprint(opj(run_name,preprocessed_dir,'Bag_Folder.pkl')+' exists, loading it.','yellow','on_red')
			BF = load_obj(opj(bfp,preprocessed_dir,'Bag_Folder.pkl'))
		else:
			if False:
				BF = Bag_Folder.init(bfp,
					preprocessed_dir=preprocessed_dir,
					left_image_bound_to_data_name=left_image_bound_to_data_name,
					NUM_STATE_ONE_STEPS=10)
				save_obj(BF,opj(bfp,preprocessed_dir,'Bag_Folder.pkl'))
			cprint('ERROR!!! '+opj(run_name,preprocessed_dir,'Bag_Folder.pkl')+' does not exist!','yellow','on_red')
			assert(False)

		if run_name in BF_dic:
			cprint('ERROR!!! '+run_name+' already in BF_dic!','yellow','on_red')
			assert(False)
		BF_dic[run_name] = BF

	return BF_dic

BF_dic = load_Bag_Folders(opjD('runs'))

run_names = BF_dic.keys()

loaded_bag_files_names = {}

def bag_file_loader_thread():
	global loaded_bag_files_names
	for j in range(1000): # 50 brings us to 80.9 GiB, 75 brings us to 106.2. This is 56 loaded bag files, about 28 minutes of data, about 1% of 40 hours.
		cprint(d2s(j),'red','on_blue')
		if len(loaded_bag_files_names) > 75:
			bf = a_key(loaded_bag_files_names)
			cprint('deleting '+bf)
			r = loaded_bag_files_names[bf]
			loaded_bag_files_names.pop(bf)
			BF = BF_dic[r]
			BF['bag_file_image_data'].pop(bf)
		try:
			r = random.choice(run_names)
			BF = BF_dic[r]
			if 'bag_file_image_data' not in BF:
				BF['bag_file_image_data'] = {}
			bf = random.choice(BF['bag_file_num_dic'])
			if bf in BF['bag_file_image_data']:
				continue
			BF['bag_file_image_data'][bf] = Bag_File.load_images(bf)
			loaded_bag_files_names[bf] = r
		except Exception as e:
			cprint("********** Exception ***********************",'red')
			print(e.message, e.args)

	print("DONE!!!!!!!!!!!!!!!")


import threading
threading.Thread(target=bag_file_loader_thread).start()


time.sleep(30)

for j in range(100):
	r = random.choice(run_names)
	BF = BF_dic[r]
	if 'bag_file_image_data' not in BF:
		continue
	if len(BF['bag_file_image_data']) < 1:
		continue
	bid = an_element(BF['bag_file_image_data'])
	bag_left_timestamps = sorted(bid['left'].keys())

	good_bag_timestamps = list(set(BF['data']['good_start_timestamps']) & set(bag_left_timestamps))
	
	cprint(d2s('len(good_bag_timestamps) =',len(good_bag_timestamps)),'blue')
	if len(good_bag_timestamps) < 100:
		print('skipping')
		continue
	ts = sorted(bid['left'].keys())
	for i in range(len(ts)):
		t = ts[i]
		#mi(bid['left'][t],'left')

		cv2.imshow('left',cv2.cvtColor(bid['left'][t],cv2.COLOR_RGB2BGR))#.astype('uint8'))

		if cv2.waitKey(3) & 0xFF == ord('q'):
		    j=1000;break
	#plt.pause(1.0/60.0)

cv2.destroyAllWindows()


