from kzpy3.vis import *
import kzpy3.teg3.data.access.Bag_Folder as Bag_Folder
import kzpy3.teg3.data.access.Bag_File as Bag_File
from kzpy3.teg3.data.preprocess.preprocess_Bag_Folders import get_preprocess_dir_name_info as get_preprocess_dir_name_info
import cv2
import threading




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

class Timer:
    def __init__(self, time_s):
    	self.time_s = time_s
    	self.start_time = time.time()
    def check(self):
    	if time.time() - self.start_time > self.time_s:
    		return True
    	else:
    		return False
    def reset(self, time_s):
    	self.time_s = time_s
    	self.start_time = time.time()

thread_please_load_data = True
thread_please_show_image_data = True

loaded_bag_files_names = {}


bag_file_loader_thread_please_exit = False

def bag_file_loader_thread(delay_before_delete=60):
	global loaded_bag_files_names
	while True: # 50 brings us to 80.9 GiB, 75 brings us to 106.2. This is 56 loaded bag files, about 28 minutes of data, about 1% of 40 hours.
		if bag_file_loader_thread_please_exit:
			cprint('THREAD:: exiting bag_file_loader_thread()')
			return
		elif not thread_please_load_data:
			time.sleep(1)
		else:
			if len(loaded_bag_files_names) > 50:
				cprint('THREAD:: pause before deleting '+bf,'blue','on_red')
				time.sleep(delay_before_delete)
				bf = a_key(loaded_bag_files_names)
				cprint('THREAD:: deleting '+bf,'blue','on_red')
				r = loaded_bag_files_names[bf]
				loaded_bag_files_names.pop(bf)
				BF = BF_dic[r]
				BF['bag_file_image_data'].pop(bf)
			try:
				r = random.choice(BF_dic.keys())
				BF = BF_dic[r]
				if 'bag_file_image_data' not in BF:
					BF['bag_file_image_data'] = {}
				bf = random.choice(BF['bag_file_num_dic'])
				if bf in BF['bag_file_image_data']:
					continue
				BF['bag_file_image_data'][bf] = Bag_File.load_images(bf)
				loaded_bag_files_names[bf] = r
			except Exception as e:
				cprint("THREAD:: ********** Exception ***********************",'red')
				print(e.message, e.args)



show_image_data_please_exit = False

#def show_image_data():

			#plt.pause(1.0/60.0)

#cv2.destroyAllWindows()



BF_dic = load_Bag_Folders(opjD('runs'))

threading.Thread(target=bag_file_loader_thread).start()

played_bagfile_dic = {}

steer_rect_color = [0,0,255]


#time.sleep(30) # to let some data get loaded

#threading.Thread(target=show_image_data).start()


while True:
	if show_image_data_please_exit:
		cv2.destroyAllWindows()
		cprint('exiting show_image_data()')
		break #return
	elif not thread_please_show_image_data:
		time.sleep(1)
	else:
		r = random.choice(BF_dic.keys())
		BF = BF_dic[r]
		if 'bag_file_image_data' not in BF:
			continue
		if len(BF['bag_file_image_data']) < 1:
			time.sleep(1)
			continue
		bf = a_key(BF['bag_file_image_data'])
		bid = BF['bag_file_image_data'][bf]
		if bf.split('/')[-1] not in played_bagfile_dic:
			played_bagfile_dic[bf.split('/')[-1]] = 0
		played_bagfile_dic[bf.split('/')[-1]] += 1
		bag_left_timestamps = sorted(bid['left'].keys())

		good_bag_timestamps = list(set(BF['data']['good_start_timestamps']) & set(bag_left_timestamps))
		
		cprint(d2s('MAIN:: ',bf.split('/')[-1],'len(good_bag_timestamps) =',len(good_bag_timestamps)),'blue')

		steer_list = []
		for t in good_bag_timestamps:
			steer_list.append(np.abs(BF['left_image_bound_to_data'][t]['steer']-49))
		figure('steer')
		clf()
		plt.hist(steer_list,bins=10)
		xlim(0,99)
		plt.pause(0.01)


		if len(good_bag_timestamps) < 100:
			print(d2s('MAIN:: skipping',bf.split('/')[-1],"len(good_bag_timestamps) < 100"))
			continue
		ts = sorted(bid['left'].keys()) #sorted(good_bag_timestamps) #
		for i in range(len(ts)):
			t = ts[i]
			#mi(bid['left'][t],'left')
			steer = BF['left_image_bound_to_data'][t]['steer']
			motor = BF['left_image_bound_to_data'][t]['motor']
			state = BF['left_image_bound_to_data'][t]['state']
			img = bid['left'][t].copy()
			apply_rect_to_img(img,steer,0,99,steer_rect_color,steer_rect_color,0.9,0.1,center=True,reverse=True,horizontal=True)
			apply_rect_to_img(img,motor,0,99,steer_rect_color,steer_rect_color,0.9,0.1,center=True,reverse=True,horizontal=False)
			apply_rect_to_img(img,state,-4,4,steer_rect_color,steer_rect_color,0.1,0.1,center=True,reverse=True,horizontal=False)
			cv2.imshow('left',cv2.cvtColor(img,cv2.COLOR_RGB2BGR))#.astype('uint8'))

			if cv2.waitKey(33) & 0xFF == ord('q'):
			    break