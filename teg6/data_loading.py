from kzpy3.utils import *
import kzpy3.teg4.data.access.Bag_File as Bag_File
import cv2

meta_dir = opjD('bair_car_data','meta')
rgb_1to4_dir = opjD('bair_car_data','rgb_1to4')





def get_bag_names_dic(meta_dir,rgb_1to4_dir,to_ignore = ['caffe','home','racing']):

	_,all_run_names = dir_as_dic_and_list(meta_dir)


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





def load_bag_file(bag_names_dic,BagFolder_dic,bag_img_dic,skip_bag_dic,meta_dir,rgb_1to4_dir):
	timer = Timer(10)
	while True:
		bn = a_key(bag_names_dic)
		if bn in skip_bag_dic:
			continue
		bf = fname(bn)
		if bag_names_dic[bn] == False:
			run_name = bn.split('/')[0]
			if run_name not in BagFolder_dic:
				cprint('Loading '+opj(run_name,'Bag_Folder.pkl'),'yellow','on_red')
				BagFolder_dic[run_name] = load_obj(opj(meta_dir,run_name,'Bag_Folder.pkl'))
			bag_img_dic[bn] = Bag_File.load_images(opj(rgb_1to4_dir,bn),color_mode="rgb8",include_flip=True)
			bag_names_dic[bn] == True

			good_bag_timestamps = list(set(BagFolder_dic[run_name]['data']['good_start_timestamps']) & set(bag_img_dic[bn]['left'].keys()))
			if len(good_bag_timestamps) < 100:
				skip_bag_dic[bn] = True
				del bag_img_dic[bn]
				del bag_names_dic[bn]
				continue
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





def _get_data(BagFolder_dic,bag_img_dic,NUM_STATE_ONE_STEPS):
	try:
		data = {}
		bn = a_key(bag_img_dic)
		bf = fname(bn)
		run_name = bn.split('/')[0]
		BF = BagFolder_dic[run_name]

		if type(BF) != dict:
			skip_bag_dic[bn] = True; return None

		if fname(bn) not in BF['good_bag_timestamps']:
			cprint(bf + """ not in BF['good_bag_timestamps']""")
			skip_bag_dic[bn] = True; return None
		if len(BF['good_bag_timestamps'][fname(bn)]) < 100:
			if verbose:
				print(d2s('MAIN:: skipping',bf.split('/')[-1],"len(good_bag_timestamps) < 100"))
			skip_bag_dic[bn] = True; return None

		bid = bag_img_dic[bn]

		if len(BF['binned_timestamps'][bf][0]) > 0 and len(BF['binned_timestamps'][bf][1]) > 0:
			rt = random.choice(BF['binned_timestamps'][bf][np.random.randint(2)])
		elif len(BF['binned_timestamps'][bf][0]) > 0:
			rt = random.choice(BF['binned_timestamps'][bf][0])
		elif len(BF['binned_timestamps'][bf][1]) > 0:
			rt = random.choice(BF['binned_timestamps'][bf][1])
		else:
			skip_bag_dic[bn] = True; return None

		topics = ['left','right','left_flip','right_flip','steer','motor','state','gyro_x','gyro_y','gyro_z','gyro_yz_mag']
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

		try:
			if type(data['path']) != str:
				skip_bag_dic[bn] = True; return None
			for topic in ['steer','motor','gyro_x','gyro_y','gyro_z','gyro_yz_mag','left','right','left_flip','right_flip']:
				if type(data[topic]) != list:
					skip_bag_dic[bn] = True; return None
				if len(data[topic]) != NUM_STATE_ONE_STEPS:
					skip_bag_dic[bn] = True; return None
			
			for topic in ['steer','motor','gyro_x','gyro_y','gyro_z','gyro_yz_mag']:
				for v in data[topic]:
					if not isinstance(v,(int,long,float)):
						skip_bag_dic[bn] = True; return None

			for topic in ['left','right','left_flip','right_flip']:
				for v in data[topic]:
					if not isinstance(v,np.ndarray):
						skip_bag_dic[bn] = True; return None
			
		except:
			skip_bag_dic[bn] = True; return None
 	except Exception as e:
		cprint("********** Exception ***********************",'red')
		print(e.message, e.args)
		skip_bag_dic[bn] = True; return None
		
	return data




def get_data(BagFolder_dic,bag_img_dic,group_binned_timestamps,NUM_STATE_ONE_STEPS):
	try:
		data = {}

		c = random.choice([0,1])
		rt = a_key(group_binned_timestamps[c])
		run_name,bf = group_binned_timestamps[c][rt]
		bn = opj(run_name,bf)

		BF = BagFolder_dic[run_name]

		if type(BF) != dict:
			skip_bag_dic[bn] = True; return None

		if fname(bn) not in BF['good_bag_timestamps']:
			cprint(bf + """ not in BF['good_bag_timestamps']""")
			skip_bag_dic[bn] = True; return None
		if len(BF['good_bag_timestamps'][fname(bn)]) < 100:
			if verbose:
				print(d2s('MAIN:: skipping',bf.split('/')[-1],"len(good_bag_timestamps) < 100"))
			skip_bag_dic[bn] = True; return None

		bid = bag_img_dic[bn]

		if len(BF['binned_timestamps'][bf][0]) > 0 and len(BF['binned_timestamps'][bf][1]) > 0:
			rt = random.choice(BF['binned_timestamps'][bf][np.random.randint(2)])
		elif len(BF['binned_timestamps'][bf][0]) > 0:
			rt = random.choice(BF['binned_timestamps'][bf][0])
		elif len(BF['binned_timestamps'][bf][1]) > 0:
			rt = random.choice(BF['binned_timestamps'][bf][1])
		else:
			skip_bag_dic[bn] = True; return None

		topics = ['left','right','left_flip','right_flip','steer','motor','state','gyro_x','gyro_y','gyro_z','gyro_yz_mag']
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

		try:
			if type(data['path']) != str:
				skip_bag_dic[bn] = True; return None
			for topic in ['steer','motor','gyro_x','gyro_y','gyro_z','gyro_yz_mag','left','right','left_flip','right_flip']:
				if type(data[topic]) != list:
					skip_bag_dic[bn] = True; return None
				if len(data[topic]) != NUM_STATE_ONE_STEPS:
					skip_bag_dic[bn] = True; return None
			
			for topic in ['steer','motor','gyro_x','gyro_y','gyro_z','gyro_yz_mag']:
				for v in data[topic]:
					if not isinstance(v,(int,long,float)):
						skip_bag_dic[bn] = True; return None

			for topic in ['left','right','left_flip','right_flip']:
				for v in data[topic]:
					if not isinstance(v,np.ndarray):
						skip_bag_dic[bn] = True; return None
			
		except:
			skip_bag_dic[bn] = True; return None
 	except Exception as e:
		cprint("********** Exception ***********************",'red')
		print(e.message, e.args)
		skip_bag_dic[bn] = True; return None
		
	return data


def visualize_data(data,dt=33):
	figure('steer motor gyro_yz_mag')
	clf()
	#plt.subplot(1,3,3)
	plot((array(d['steer'])-49)/100.,'r')
	plot((array(d['motor'])-49)/100,'g')
	plot((array(d['gyro_yz_mag'])/200.),'b')
	ylim(-0.5,0.5)
	pause(0.00001)
	for i in range(len(d['right'])):
		#mi(d['right'][i],'right')
		#pause(0.00000001)
		cv2.imshow('right',cv2.cvtColor(d['left'][i],cv2.COLOR_RGB2BGR))
		if cv2.waitKey(dt) & 0xFF == ord('q'):
			pass

if True:
	bag_names_dic = get_bag_names_dic(meta_dir,rgb_1to4_dir)

	bag_img_dic = {}

	BagFolder_dic = {}

	skip_bag_dic = {}

	bag_viewed_counter_dic = {}



	N = 100
	t0=time.time()
	for i in range(N):
		load_bag_file(bag_names_dic,BagFolder_dic,bag_img_dic,skip_bag_dic,meta_dir,rgb_1to4_dir)
	t1=time.time()
	print t1-t0,(t1-t0)/(1.0*N) #177 sec

	NUM_STATE_ONE_STEPS = 30

	verbose = True

	if True:
		memory_usage_dic = {}
		memory_usage_dic[100] = (17.4,177)

	"""
	In an hour, about 6340 bag files can be loaded.

	"""

	group_binned_timestamps = {}
	group_binned_timestamps[0] = {}
	group_binned_timestamps[1] = {}
	for r in BagFolder_dic.keys():
		if 'binned_timestamps' in BagFolder_dic[r]:
			for bf in BagFolder_dic[r]['binned_timestamps'].keys():
				binned_timestamps = BagFolder_dic[r]['binned_timestamps'][bf]
				for i in range(2):
					for j in range(len(binned_timestamps[i])):
						group_binned_timestamps[i][binned_timestamps[i][j]] = (r,bf)


bag_viewed_counter_dic = {}
N = 10000
ctr = 0
t0=time.time()
counts_timer = Timer(10)
counts = []
count_median = 0
while count_median < 30:
	if counts_timer.check():
		counts_timer.reset()
		for c in bag_viewed_counter_dic.keys():
			counts.append(bag_viewed_counter_dic[c])
		counts = sorted(counts)
		figure('counts')
		hist(counts)
		count_median = np.median(array(counts))
		plt.title(count_median)
	cprint(d2s(i),'red','on_yellow')
	d=get_data(BagFolder_dic,bag_img_dic,group_binned_timestamps,NUM_STATE_ONE_STEPS)
	if d == None:
		ctr += 1
	else:
		visualize_data(d,1)
		bf = d['path']
		if bf not in bag_viewed_counter_dic:
			bag_viewed_counter_dic[bf] = 0
		bag_viewed_counter_dic[bf] += 1
		print(d2s(bf,bag_viewed_counter_dic[bf]))
t1=time.time()
print t1-t0,(t1-t0)/(1.0*N) #57 sec
print(d2s(ctr,100*ctr/(N*1.0),'%'))


