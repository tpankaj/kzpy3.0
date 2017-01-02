
path = '/Users/karlzipser/Desktop/19July2015_1Jan2016_p-imaging_results/p_images_alone/S1_2015'

task = 'attend_face'

folders = [opj(path,'attend_face/subjects/S1_2015/2015/2/3/0/stats/p_images/png_std/a_9'),
	opj(path,'attend_face/subjects/S1_2015/2015/2/3/0/stats/p_images/png_std/b_7'),opj(path,'attend_vase/subjects/S1_2015/2015/2/3/0/stats/p_images/png_std/c_7')]

weights = [9.,7.,7.]

img_dic = {}
img_mean_dic = {}

mask = zeros((128,128))

mask2 = mask.copy()
mask2[19:109,2:126] = 1.





mask[30:128-30,20:108]=1. ;mask[128/2-12:128/2+12,128/2-12:128/2+12]=0.

thresh = 3.

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
	mi(img_mean_dic[k],task,[2,3,ctr],do_clf=do_clf,img_title=k)