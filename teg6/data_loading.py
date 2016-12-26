from kzpy3.utils import *
import kzpy3.teg4.data.access.Bag_File as Bag_File

meta_dir = opjD('bair_car_data','meta')
rgb_1to4_dir = opjD('bair_car_data','rgb_1to4')





def get_bag_names_dic(meta_dir,rgb_1to4_dir):

	_,all_run_names = dir_as_dic_and_list(meta_dir)

	to_ignore = ['caffe','home']

	run_names_dic = {}
	
	bag_names_dic = {}


	for r in all_run_names:
		if str_contains_one(r,to_ignore):
			cprint("Ignoring "+r,'yellow','on_blue')
		else:
			run_names_dic[r] = None

	for r in run_names_dic:
		p = opj(rgb_1to4_dir,r)
		if len(gg(p)) > 0:
			_,b = dir_as_dic_and_list(p)
			run_names_dic[r] = b
			for f in run_names_dic[r]:
				bag_names_dic[opj(r,f)] = False
		else:
			cprint("Warning: "+p+" does not exist",'red','on_cyan')

	N = 0
	for r in sorted(run_names_dic):
		n = len(run_names_dic[r])
		cprint(d2n('\t',r,': ',n))
		N += n
	cprint(d2s('All runs:',len(all_run_names),'Using runs:',len(run_names_dic)))
	cprint(d2n('Number of bags:',N,', estimated hours = ',dp(N/120.,1)))

	return bag_names_dic





def load_bag_file(bag_names_dic,BagFolder_dic,bag_img_dic,meta_dir,rgb_1to4_dir):
	timer = Timer(10)
	while True:
		bn = a_key(bag_names_dic)
		bf = fname(bn)
		if bag_names_dic[bn] == False:
			run_name = bn.split('/')[0]
			if run_name not in BagFolder_dic:
				cprint(opj(run_name,'Bag_Folder.pkl')+' exists, loading it.','yellow','on_red')
				BagFolder_dic[run_name] = load_obj(opj(meta_dir,run_name,'Bag_Folder.pkl'))
			bag_img_dic[bn] = Bag_File.load_images(opj(rgb_1to4_dir,bn),color_mode="rgb8",include_flip=True)
			bag_names_dic[bn] == True
			good_bag_timestamps = list(set(BagFolder_dic[run_name]['data']['good_start_timestamps']) & set(bag_img_dic[bn]['left'].keys()))
			
			binned_timestamps = [[],[]]
			binned_steers = [[],[]]

			for t in good_bag_timestamps:
				steer = BagFolder_dic[run_name]['left_image_bound_to_data'][t]['steer']
				if steer < 43 or steer > 55:
					binned_timestamps[0].append(t)
					binned_steers[0].append(steer)
				else:
					binned_timestamps[1].append(t)
					binned_steers[1].append(steer)
			dic_keys = ['bag_file_image_data','good_bag_timestamps','binned_timestamps','binned_steers','bid_timestamps']
			for dk in dic_keys:
				if dk not in BagFolder_dic[run_name]:
					BagFolder_dic[run_name][dk] = {}
			BagFolder_dic[run_name]['good_bag_timestamps'][bf] = good_bag_timestamps
			BagFolder_dic[run_name]['binned_timestamps'][bf] = binned_timestamps
			BagFolder_dic[run_name]['binned_steers'][bf] = binned_steers
			BagFolder_dic[run_name]['bid_timestamps'][bf] = sorted(bag_img_dic[bn]['left'].keys())			
			
			print bn
			
			return

		if timer:
			assert(False)





def deload_bag_file(bag_name,bag_names_dic,bag_img_dic):
	assert(bag_name in bag_img_dic)
	del bag_img_dic[bag_name]
	bag_names_dic[bag_name] = False





def get_data(BagFolder_dic,bag_img_dic,NUM_STATE_ONE_STEPS):
	if True:
		data = {}

		bn = a_key(bag_img_dic)
		bf = fname(bn)
		BF = BagFolder_dic[bn.split('/')[0]]
		print(1)
		if type(BF) != dict:
			return None
		print(2)

		print(3)
		if fname(bn) not in BF['good_bag_timestamps']:
			cprint(bf + """ not in BF['good_bag_timestamps']""")
			return None
		if len(BF['good_bag_timestamps'][fname(bn)]) < 100:
			if verbose:
				print(d2s('MAIN:: skipping',bf.split('/')[-1],"len(good_bag_timestamps) < 100"))
			return None
		print(4)
		bid = bag_img_dic[bn]

		print(4)
		if len(BF['binned_timestamps'][bf][0]) > 0 and len(BF['binned_timestamps'][bf][1]) > 0:
			rt = random.choice(BF['binned_timestamps'][bf][np.random.randint(2)])
		elif len(BF['binned_timestamps'][bf][0]) > 0:
			rt = random.choice(BF['binned_timestamps'][bf][0])
		elif len(BF['binned_timestamps'][bf][1]) > 0:
			rt = random.choice(BF['binned_timestamps'][bf][1])
		else:
			return None		
		print(4)
		topics = ['left','right','left_flip','right_flip','steer','motor','state','gyro_x','gyro_y','gyro_z','gyro_yz_mag']
		for tp in topics:
			data[tp] = []
		print(4)
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
						gyro_yz_mag = np.sqrt(gyro_y**2+gyro_z**2)
						img_left = bid['left'][t]
						right_timestamp = BF['left_image_bound_to_data'][t]['right_image']
						img_right = bid['right'][right_timestamp]

						img_left_flip = bid['left_flip'][t]
						img_right_flip = bid['right_flip'][right_timestamp]


						data['path'] = bf
						data['steer'].append(steer)
						data['motor'].append(motor)
						data['gyro_x'].append(gyro_x)
						data['gyro_y'].append(gyro_y)
						data['gyro_z'].append(gyro_z)
						data['gyro_yz_mag'].append(gyro_yz_mag)
						data['left'].append(img_left)
						data['right'].append(img_right)
						data['left_flip'].append(img_left_flip)
						data['right_flip'].append(img_right_flip)


					break
				else:
					if verbose:
						cprint("MAIN:: ERROR!!!!!!!!! if len(ts) > i+10: failed")
		print(4)
		try:
			if type(data['path']) != str:
				return None
			for topic in ['steer','motor','gyro_x','gyro_y','gyro_z','gyro_yz_mag','left','right','left_flip','right_flip']:
				if type(data[topic]) != list:
					return None
				if len(data[topic]) != NUM_STATE_ONE_STEPS:
					return None
			
			for topic in ['steer','motor','gyro_x','gyro_y','gyro_z','gyro_yz_mag']:
				for v in data[topic]:
					if not isinstance(v,(int,long,float)):
						return None

			for topic in ['left','right','left_flip','right_flip']:
				for v in data[topic]:
					if not isinstance(v,np.ndarray):
						return None
			
		except:
			return None
 	else:# Exception as e:
		cprint("********** Exception ***********************",'red')
		print(e.message, e.args)
		return None	
	return data



bag_names_dic = get_bag_names_dic(meta_dir,rgb_1to4_dir)

bag_img_dic = {}

BagFolder_dic = {}
t0=time.time()
for i in range(500):
	load_bag_file(bag_names_dic,BagFolder_dic,bag_img_dic,meta_dir,rgb_1to4_dir)
t1=time.time()
print t1-t0 #57 sec

NUM_STATE_ONE_STEPS = 30

verbose = True

