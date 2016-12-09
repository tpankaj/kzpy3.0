from kzpy3.vis import *
import kzpy3.teg3.data.access.Bag_Folder as Bag_Folder
import kzpy3.teg3.data.access.Bag_File as Bag_File
from kzpy3.teg3.data.preprocess.preprocess_Bag_Folders import get_preprocess_dir_name_info as get_preprocess_dir_name_info
import cv2
import threading


NUM_STATE_ONE_STEPS = 30

played_bagfile_dic = {}

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



thread_please_load_data = True
thread_please_show_image_data = True

loaded_bag_files_names = {}


bag_file_loader_thread_please_exit = False

def bag_file_loader_thread(delay_before_delete=5*60):
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

				played_bagfile_dic_keys = []
				played_bagfile_dic_values = []
				for b in played_bagfile_dic.keys():
					played_bagfile_dic_keys.append(b)
					played_bagfile_dic_values.append(played_bagfile_dic[b])
				indicies = [i[0] for i in sorted(enumerate(played_bagfile_dic_values),key=lambda x:x[1])]
				indicies.reverse()
				ctr = 0
				for i in indicies:
					if ctr >= 25:
						break
					bf = played_bagfile_dic_keys[i]
					if bf in loaded_bag_files_names:
						#bf = a_key(loaded_bag_files_names)
						cprint('THREAD:: deleting '+bf,'blue','on_red')
						r = loaded_bag_files_names[bf]
						loaded_bag_files_names.pop(bf)
						BF = BF_dic[r]
						BF['bag_file_image_data'].pop(bf)
						ctr += 1
			try:
				r = random.choice(BF_dic.keys())
				BF = BF_dic[r]
				dic_keys = ['bag_file_image_data','good_bag_timestamps','binned_timestamps','binned_steers','bid_timestamps']
				for dk in dic_keys:
					if dk not in BF:
						BF[dk] = {}
				bf = random.choice(BF['bag_file_num_dic'])
				if bf in BF['bag_file_image_data']:
					continue
				BF['bag_file_image_data'][bf] = Bag_File.load_images(bf)
				loaded_bag_files_names[bf] = r

				bid = BF['bag_file_image_data'][bf]

				bag_left_timestamps = sorted(bid['left'].keys())

				good_bag_timestamps = list(set(BF['data']['good_start_timestamps']) & set(bag_left_timestamps))
				
				cprint(d2s('THREAD:: ',bf.split('/')[-1],'len(good_bag_timestamps) =',len(good_bag_timestamps)),'blue')

				binned_timestamps = [[],[]]
				binned_steers = [[],[]]

				for t in good_bag_timestamps:
					steer = BF['left_image_bound_to_data'][t]['steer']
					if steer < 43 or steer > 55:
						binned_timestamps[0].append(t)
						binned_steers[0].append(steer)
					else:
						binned_timestamps[1].append(t)
						binned_steers[1].append(steer)

				BF['good_bag_timestamps'][bf] = good_bag_timestamps
				BF['binned_timestamps'][bf] = binned_timestamps
				BF['binned_steers'][bf] = binned_steers
				BF['bid_timestamps'][bf] = sorted(bid['left'].keys())

			except Exception as e:
				cprint("THREAD:: ********** Exception ***********************",'red')
				print(e.message, e.args)



show_image_data_please_exit = False

#def show_image_data():

			#plt.pause(1.0/60.0)

#cv2.destroyAllWindows()



BF_dic = load_Bag_Folders(opjD('runs'))

threading.Thread(target=bag_file_loader_thread).start()



steer_rect_color = [0,0,255]


#time.sleep(30) # to let some data get loaded

#threading.Thread(target=show_image_data).start()


while True:
	if show_image_data_please_exit:
		cv2.destroyAllWindows()
		cprint('MAIN:: exiting show_image_data()')
		break #return
	elif not thread_please_show_image_data:
		time.sleep(1)
	else:
		r = random.choice(BF_dic.keys())
		BF = BF_dic[r]
		if 'bag_file_image_data' not in BF:
			time.sleep(1)
			continue
		if len(BF['bag_file_image_data']) < 1:
			time.sleep(1)
			continue
		bf = a_key(BF['bag_file_image_data'])
		if len(BF['good_bag_timestamps'][bf]) < 100:
			print(d2s('MAIN:: skipping',bf.split('/')[-1],"len(good_bag_timestamps) < 100"))
			continue
		bid = BF['bag_file_image_data'][bf]
		if bf not in played_bagfile_dic:
			played_bagfile_dic[bf] = 0
		played_bagfile_dic[bf] += 1

		if False:
			figure('steer')
			clf()
			bins = range(0,105,3)
			plt.hist(BF['binned_steers'][bf][0],bins=bins)
			plt.hist(BF['binned_steers'][bf][1],bins=bins)
			xlim(0,99)
			pause(0.01)
		"""
        if len(self.binned_timestamp_nums[0]) > 0 and len(self.binned_timestamp_nums[1]) > 0:
            timestamp_num = random.choice(self.binned_timestamp_nums[np.random.randint(len(self.binned_timestamp_nums))])
        elif len(self.binned_timestamp_nums[0]) > 0:
            timestamp_num = random.choice(self.binned_timestamp_nums[0])
        elif len(self.binned_timestamp_nums[1]) > 0:
            timestamp_num = random.choice(self.binned_timestamp_nums[1])
        else:
            return None
        """

		"""
						steer_list = []
						for t in good_bag_timestamps:
							steer_list.append(np.abs(BF['left_image_bound_to_data'][t]['steer']-49))
						steer_list = sorted(steer_list)
						figure('steer')
						clf()
						plt.hist(steer_list,bins=10)
						xlim(0,99)
						plt.pause(0.01)
		"""

		if False:
			ts = BF['bid_timestamps'][bf]
			for i in range(len(ts)):
				t = ts[i]
				#mi(bid['left'][t],'left')
				steer = BF['left_image_bound_to_data'][t]['steer']
				motor = BF['left_image_bound_to_data'][t]['motor']
				state = BF['left_image_bound_to_data'][t]['state']
				img = bid['left'][t].copy()
				apply_rect_to_img(img,steer,0,99,steer_rect_color,steer_rect_color,0.9,0.1,center=True,reverse=True,horizontal=True)
				apply_rect_to_img(img,motor,0,99,steer_rect_color,steer_rect_color,0.9,0.1,center=True,reverse=True,horizontal=False)
				apply_rect_to_img(img,state,-150,150,steer_rect_color,steer_rect_color,0.1,0.1,center=True,reverse=True,horizontal=False)
				cv2.imshow('left',cv2.cvtColor(img,cv2.COLOR_RGB2BGR))#.astype('uint8'))

				if cv2.waitKey(3) & 0xFF == ord('q'):
				    break

		if True:
			if len(BF['binned_timestamps'][bf][0]) > 0 and len(BF['binned_timestamps'][bf][1]) > 0:
				rt = random.choice(BF['binned_timestamps'][bf][np.random.randint(2)])
			elif len(BF['binned_timestamps'][bf][0]) > 0:
				rt = random.choice(BF['binned_timestamps'][bf][0])
			elif len(BF['binned_timestamps'][bf][1]) > 0:
				rt = random.choice(BF['binned_timestamps'][bf][1])
			else:
				continue		

			data = {}
			topics = ['steer','motor','state','gyro_x','gyro_y','gyro_z']
			for tp in topics:
				data[tp] = []

			ts = BF['bid_timestamps'][bf]
			for i in range(len(ts)):
				if ts[i] == rt:
					if len(ts) > i+NUM_STATE_ONE_STEPS:
						for j in range(i,i+NUM_STATE_ONE_STEPS):
							t = ts[j]

							steer = BF['left_image_bound_to_data'][t]['steer']
							motor = BF['left_image_bound_to_data'][t]['motor']
							#state = BF['left_image_bound_to_data'][t]['state']
							gyro_x = BF['left_image_bound_to_data'][t]['gyro'][0]
							gyro_y = BF['left_image_bound_to_data'][t]['gyro'][1]
							gyro_z = BF['left_image_bound_to_data'][t]['gyro'][2]
							img_left = bid['left'][t]
							img_right = bid['right'][t]
							img = img_left.copy()
							apply_rect_to_img(img,steer,0,99,steer_rect_color,steer_rect_color,0.9,0.1,center=True,reverse=True,horizontal=True)
							apply_rect_to_img(img,motor,0,99,steer_rect_color,steer_rect_color,0.9,0.1,center=True,reverse=True,horizontal=False)
							apply_rect_to_img(img,gyro_x,-150,150,steer_rect_color,steer_rect_color,0.1,0.03,center=True,reverse=True,horizontal=False)
							apply_rect_to_img(img,gyro_y,-150,150,steer_rect_color,steer_rect_color,0.13,0.03,center=True,reverse=True,horizontal=False)
							apply_rect_to_img(img,gyro_z,-150,150,steer_rect_color,steer_rect_color,0.16,0.03,center=True,reverse=True,horizontal=False)
							cv2.imshow('left',cv2.cvtColor(img,cv2.COLOR_RGB2BGR))#.astype('uint8'))

							data['steer'].append(steer)
							data['motor'].append(motor)
							data['gyro_x'].append(gyro_x)
							data['gyro_y'].append(gyro_y)
							data['gyro_z'].append(gyro_z)
							data['gyro_xy_mag'].append(np.sqrt(gyro_x**2+gyro_y**2))
							data['left'].append(img_left)
							data['right'].append(img_right)

							caffe_net.train_step(data)

							if cv2.waitKey(33) & 0xFF == ord('q'):
							    break
						break
					else:
						cprint("MAIN:: ERROR!!!!!!!!! if len(ts) > i+10: failed")

















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