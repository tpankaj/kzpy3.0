from kzpy3.vis import *





mask = zeros((128,128))
mask[25:128-25,10:118]=1.
q = 6
mask[128/2-q:128/2+q,128/2-q:128/2+q]=0.
mask = mask[16:112,:]

mi(mask,'mask')

thresh = 10.







mask_dic_2 = {}
mask_dic_2['vase'] = {}
mask_dic_2['face'] = {}

mask_dic_2['vase']['1.png'] = '1_vase.png'
mask_dic_2['vase']['2.png'] = '2_vase.png'
mask_dic_2['vase']['3.png'] = '3_vase.png'
mask_dic_2['vase']['4.png'] = '4_vase.png'

mask_dic_2['face']['1.png'] = '1_face.png'
mask_dic_2['face']['2.png'] = '2_face.png'
mask_dic_2['face']['3.png'] = '3_face.png'
mask_dic_2['face']['4.png'] = '4_face.png'

mask_dic_2['space']['1.png'] = '1_space.png'
mask_dic_2['space']['2.png'] = '2_space.png'
mask_dic_2['space']['3.png'] = '3_space.png'
mask_dic_2['space']['4.png'] = '4_space.png'


blank = zeros((128,128))
mask_path = opjD('/Users/karlzipser/Desktop/19July2015_1Jan2016_p-imaging_results/S1_2014_S6_2015_images_and_masks/Vermeer_masks')
for t in mask_dic_2:
	for n in mask_dic_2[t]:
		blank = 0*blank
		blank[16:96+16] = z2o(imread(opj(mask_path,mask_dic_2[t][n]))[:,:,0])
		mask_dic_2[t][n] = mask2 * blank





mask2 = mask.copy()
mask2[19:109,2:126] = 1.

mask_dic_1 = {}
mask_dic_1['vase'] = {}
mask_dic_1['face'] = {}
mask_dic_1['space_near_vase'] = {}
mask_dic_1['space_near_face'] = {}

mask_dic_1['vase']['2.png'] = 'Vermeer_2_mask_vase.png'
mask_dic_1['vase']['3.png'] = 'Vermeer_3_mask_vase.png'
mask_dic_1['vase']['4.png'] = 'Vermeer_4_mask_vase.png'
mask_dic_1['vase']['5.png'] = 'Vermeer_5_mask_vase.png'
mask_dic_1['vase']['8.png'] = 'Vermeer_2_mask_vase.png'
mask_dic_1['vase']['9.png'] = 'Vermeer_3_mask_vase.png'
mask_dic_1['vase']['10.png'] = 'Vermeer_4_mask_vase.png'
mask_dic_1['vase']['11.png'] = 'Vermeer_5_mask_vase.png'

mask_dic_1['face']['2.png'] = 'Vermeer_2_mask_face.png'
mask_dic_1['face']['3.png'] = 'Vermeer_3_mask_face.png'
mask_dic_1['face']['4.png'] = 'Vermeer_4_mask_face.png'
mask_dic_1['face']['5.png'] = 'Vermeer_5_mask_face.png'
mask_dic_1['face']['8.png'] = 'Vermeer_2_mask_face.png'
mask_dic_1['face']['9.png'] = 'Vermeer_3_mask_face.png'
mask_dic_1['face']['10.png'] = 'Vermeer_4_mask_face.png'
mask_dic_1['face']['11.png'] = 'Vermeer_5_mask_face.png'

mask_dic_1['space_near_vase']['2.png'] = 'Vermeer_2_mask_vase.png'
mask_dic_1['space_near_vase']['3.png'] = 'Vermeer_3_mask_vase.png'
mask_dic_1['space_near_vase']['4.png'] = 'Vermeer_4_mask_vase.png'
mask_dic_1['space_near_vase']['5.png'] = 'Vermeer_5_mask_vase.png'
mask_dic_1['space_near_vase']['8.png'] = 'Vermeer_2_mask_vase.png'
mask_dic_1['space_near_vase']['9.png'] = 'Vermeer_3_mask_vase.png'
mask_dic_1['space_near_vase']['10.png'] = 'Vermeer_4_mask_vase.png'
mask_dic_1['space_near_vase']['11.png'] = 'Vermeer_5_mask_vase.png'

mask_dic_1['space_near_face']['2.png'] = 'Vermeer_2_mask_vase.png'
mask_dic_1['space_near_face']['3.png'] = 'Vermeer_3_mask_vase.png'
mask_dic_1['space_near_face']['4.png'] = 'Vermeer_4_mask_vase.png'
mask_dic_1['space_near_face']['5.png'] = 'Vermeer_5_mask_vase.png'
mask_dic_1['space_near_face']['8.png'] = 'Vermeer_2_mask_vase.png'
mask_dic_1['space_near_face']['9.png'] = 'Vermeer_3_mask_vase.png'
mask_dic_1['space_near_face']['10.png'] = 'Vermeer_4_mask_vase.png'
mask_dic_1['space_near_face']['11.png'] = 'Vermeer_5_mask_vase.png'


blank = zeros((128,128))
mask_path = opjD('19July2015_1Jan2016_p-imaging_results/S1_2015_HVO_images_and_masks/Vermeer_masks')
for t in mask_dic_1:
	for n in mask_dic_1[t]:
		blank = 0*blank
		blank[16:96+16] = z2o(imread(opj(mask_path,mask_dic_1[t][n]))[:,:,0])
		mask_dic_1[t][n] = mask2 * blank

















path = opjD('single_run_p_images')

subjects,_ = dir_as_dic_and_list(path)

for s in subjects:
	subjects[s] = {}
	subjects[s]['tasks_raw'],_ =  dir_as_dic_and_list(opj(path,s))
	for t in subjects[s]['tasks_raw']:
		task = t.split('.')[0]
		subjects[s][task] = {}
		subjects[s]['tasks_raw'][t] = {}
		_,subjects[s]['tasks_raw'][t] = sorted(dir_as_dic_and_list(opj(path,s,t)))
		for f in subjects[s]['tasks_raw'][t]:
			print (s,t,f)
			if len(f.split('_')) > 1:
				img_num = 100 + int(f.split('.')[0].split('_')[-1])
			else:
				img_num = int(f.split('.')[0])
				if img_num > 6:
					img_num -= 6
			if img_num not in subjects[s][task]:
				subjects[s][task][img_num] = []
			img = imread(opj(path,s,t,f))
			if shape(img)[0] == 128:
				img = img[16:112,:]

			img = 1.0 * img
			values = []
			for x in range(shape(img)[0]):
				for y in range(shape(img)[1]):
					if mask[x,y] > 0.5:
						values.append(img[x,y])
			values = array(values)
			vmean = values.mean()
			vstd = values.std()
			img -= vmean
			img /= vstd
			img[img > thresh] = thresh
			img[img < -thresh] = -thresh

			subjects[s][task][img_num].append(img)





