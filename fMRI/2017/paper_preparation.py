
path = '/Users/karlzipser/Desktop/19July2015_1Jan2016_p-imaging_results/p_images_alone/S1_2015'

folders_dic = {}


folders_dic['attend_face'] = ([9.,7.,7.],[
	opj(path,'attend_face/subjects/S1_2015/2015/2/3/0/stats/p_images/png_std/a_9'),
	opj(path,'attend_face/subjects/S1_2015/2015/2/3/0/stats/p_images/png_std/b_7'),
	opj(path,'attend_vase/subjects/S1_2015/2015/2/3/0/stats/p_images/png_std/c_7')])

folders_dic['attend_vase'] = ([4.,7.],[
	opj(path,'attend_vase/subjects/S1_2015/2015/2/3/0/stats/p_images/png_std/a_4'),
	opj(path,'attend_vase/subjects/S1_2015/2015/2/3/0/stats/p_images/png_std/b_7')])


folders_dic['read_letters'] = ([4.,9.,6.],[
	opj(path,'read_letters/subjects/S1_2015/2015/2/3/0/stats/p_images/png_std/a1_4'),
	opj(path,'read_letters/subjects/S1_2015/2015/2/3/0/stats/p_images/png_std/a1_9'),
	opj(path,'read_letters/subjects/S1_2015/2015/2/3/0/stats/p_images/png_std/d_6')])


mask_dic = {}
mask_dic['attend_vase'] = {}
mask_dic['attend_face'] = {}

mask_dic['attend_vase']['2.png'] = 'Vermeer_2_mask_vase.png'
mask_dic['attend_vase']['3.png'] = 'Vermeer_3_mask_vase.png'
mask_dic['attend_vase']['4.png'] = 'Vermeer_4_mask_vase.png'
mask_dic['attend_vase']['5.png'] = 'Vermeer_5_mask_vase.png'
mask_dic['attend_vase']['8.png'] = 'Vermeer_2_mask_vase.png'
mask_dic['attend_vase']['9.png'] = 'Vermeer_3_mask_vase.png'
mask_dic['attend_vase']['10.png'] = 'Vermeer_4_mask_vase.png'
mask_dic['attend_vase']['11.png'] = 'Vermeer_5_mask_vase.png'

mask_dic['attend_face']['2.png'] = 'Vermeer_2_mask_face.png'
mask_dic['attend_face']['3.png'] = 'Vermeer_3_mask_face.png'
mask_dic['attend_face']['4.png'] = 'Vermeer_4_mask_face.png'
mask_dic['attend_face']['5.png'] = 'Vermeer_5_mask_face.png'
mask_dic['attend_face']['8.png'] = 'Vermeer_2_mask_face.png'
mask_dic['attend_face']['9.png'] = 'Vermeer_3_mask_face.png'
mask_dic['attend_face']['10.png'] = 'Vermeer_4_mask_face.png'
mask_dic['attend_face']['11.png'] = 'Vermeer_5_mask_face.png'

blank = zeros((128,128))
mask_path = opjD('19July2015_1Jan2016_p-imaging_results/Vermeer_masks')
for t in mask_dic:
	for n in mask_dic[t]:
		blank = 0*blank
		blank[16:96+16] = imread(opj(mask_path,mask_dic[t][n]))[:,:,0]
		mask_dic[t][n] = blank

def process_p_images(folders_dic,task,mask_dic):

	weights = folders_dic[task][0]
	folders = folders_dic[task][1]

	img_dic = {}
	img_mean_dic = {}

	mask = zeros((128,128))

	mask2 = mask.copy()
	mask2[19:109,2:126] = 1.

	mask[30:128-30,20:108]=1. ;mask[128/2-12:128/2+12,128/2-12:128/2+12]=0.

	thresh = 10.

	for f,w in zip(folders,weights):
		print (f,w)
		imgs = sorted(gg(opj(f,'*.png')))
		for i in imgs:
			img = 1.0*imread(i)
			fn = fname(i)
			
			#mi(z2o(img)*(mask+0.2),1)
			values = []
			for x in range(128):
				for y in range(128):
					if mask[x,y] > 0.5:
						values.append(img[x,y])
			values = array(values)
			vmean = values.mean()
			vstd = values.std()
			img -= vmean
			img /= vstd
			img[img > thresh] = thresh
			img[img < -thresh] = -thresh
			img *= mask2
			if fn not in img_dic:
				img_dic[fn] = []
			img_dic[fn].append(w*img)
			#img[0,0] = thresh
			#img[0,1] = -thresh
			#mi(img,2,img_title=fn)
			#pause(0.1)

	weights_sum = array(weights).sum()

	ctr = 0
	for k in sorted(img_dic.keys(),key=natural_keys):
		ctr += 1
		img_mean_dic[k] = array(img_dic[k]).mean(axis=0) / weights_sum
		do_clf = False
		if ctr == 1:
			do_clf = True
		values = []
		if k in mask_dic[task]:
			for x in range(128):
				for y in range(128):
					if mask_dic[task][k][x,y] > 0.5:
						values.append(img[x,y])
			vmean = array(values).mean()
		else:
			vmean = 'not measured'
		mi(img_mean_dic[k],task,[2,3,ctr],do_clf=do_clf,img_title=d2s(k,vmean))



