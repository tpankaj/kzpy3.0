from kzpy3.utils import *

ns = txt_file_to_list_of_strings(opjh('caffe/data/imagenet/person_clothing_min1000.txt'))

for i in range(len(ns)):
	n = ns[i].split()[0]
	jpgs = gg(opjh('scratch/15Sept2015_unpack_fall11_whole/fall11_whole',n,'*.JPEG'))
	str_lst = []
	for j in jpgs:
		str_lst.append(d2s(j,i))
	list_of_strings_to_txt_file(opjh('caffe/models/person_clothing_17Sept2015/jpgs_with_labels_all.txt'),str_lst,"a")

