from kzpy3.vis import *
import kzpy3.teg5.data.access_bag_files as access_bag_files
import threading



loaded_bag_files_names = {}
played_bagfile_dic = {}
used_timestamps = {}

data_path = '/home/karlzipser/Desktop/bair_car_data'
NUM_STATE_ONE_STEPS = 30

ignore_most=['Orange','sidewalks','campus','caffe','play','follow','furtive','local','racing']

BagFolder_dic,BagFolders_weighted = access_bag_files.load_Bag_Folders(data_path,ignore=['caffe'])

thread_id = 'loader_thread'
command_dic = {}
command_dic[thread_id] = 'start' #  command_dic[thread_id] = 'pause' # command_dic[thread_id] = 'stop'
delay_before_delete = 5*60

threading.Thread(target=access_bag_files.bag_file_loader_thread,
	args=(thread_id,command_dic,data_path,BagFolder_dic,BagFolders_weighted,delay_before_delete,loaded_bag_files_names,played_bagfile_dic)).start()

data_list = []

thread_id = 'get data thread'
command_dic[thread_id] = 'start'
def get_data_thread(BagFolder_dic,played_bagfile_dic,used_timestamps,NUM_STATE_ONE_STEPS):
	global data_list
	timer = Timer(1./300.)
	while True:
		#time.sleep(1)
		state = command_dic[thread_id]
		command = command_dic[thread_id]
		if command == 'pause':
			if state == 'pause':
				pass
			else:
				state = 'pause'
				cprint(d2s('Pausing thread ',thread_id),'yellow','on_blue')
			#time.sleep(1)
			continue
		if command == 'start' and state == 'pause':
			state = 'running'
			cprint(d2s('Unpausing thread ',thread_id),'yellow','on_blue')			
		if command == 'stop':
			cprint(d2s('Stopping thread ',thread_id),'yellow','on_blue')
			return
		data = access_bag_files.get_data(BagFolder_dic,played_bagfile_dic,used_timestamps,NUM_STATE_ONE_STEPS)
		try:
			if data != None:
				#print type(data['right_flip'][-1])
				#time.sleep(1)
				data_list.append(data)
				#print((len(data_list),len(data_list[-1])))
				#print(d2s("motor",data_list[-1]['motor'][-1]))
		except:
			pass #print 'error'
		if len(data_list) > 5:
			data_list = data_list[-5:]
		while not timer.check():
			time.sleep(1./30000.)
		timer.reset()

time.sleep(3*60)
threading.Thread(target=get_data_thread,args=(BagFolder_dic,played_bagfile_dic,used_timestamps,NUM_STATE_ONE_STEPS)).start()
time.sleep(5)



import caffe
USE_GPU = True
if USE_GPU:
	caffe.set_device(0)
	caffe.set_mode_gpu()
from kzpy3.caf5.Caffe_Net import *
solver_file_path = opjh("kzpy3/caf5/z2_color/solver1.prototxt")
version = 'version 1'
weights_file_mode = 'most recent'
weights_file_path = opjD('z2_color')


caffe_net = Caffe_Net(solver_file_path,version,weights_file_mode,weights_file_path)
while True:
	try:
		data = data_list[-1]
	except Exception as e:
		cprint("********** Exception ***********************",'red')
		print(e.message, e.args)
	if data != None:
		#print data['path']
		#time.sleep(1)
		caffe_net.train_step(data)
