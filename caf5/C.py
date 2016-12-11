from kzpy3.vis import *
import threading
import kzpy3.teg4.data.access.access_bag_files as access_bag_files
import kzpy3.caf5.Caffe_Net as Caffe_Net

		    
loaded_bag_files_names = {}
played_bagfile_dic = {}
used_timestamps = {}

BF_dic = access_bag_files.load_Bag_Folders(opjD('runs'))

threading.Thread(target=access_bag_files.bag_file_loader_thread,args=(BF_dic,5*60,loaded_bag_files_names,played_bagfile_dic)).start()


while len(loaded_bag_files_names) < 1:
	cprint(d2s("""len(loaded_bag_files_names) =""",len(loaded_bag_files_names)))
	time.sleep(5)

solver_file_path = opjh("kzpy3/caf4/z2_color/solver.prototxt")
weights_file_path = opjD('z2_color')

#caffe_net = Caffe_Net.Caffe_Net(solver_file_path,'version 1','this one',weights_file_path)
caffe_net = Caffe_Net.Caffe_Net(solver_file_path,'version 1','most recent',weights_file_path)
#caffe_net = Caffe_Net.Caffe_Net(solver_file_path,'version 1',None,None)

while True:
	data = access_bag_files.get_data(BF_dic,played_bagfile_dic,used_timestamps)
	if data != None:
		caffe_net.train_step(data)


