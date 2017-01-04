"""
2 January 2016

This script looks at results from scanning HVO (S1_2015) during attend-vase or attend-face tasks
with Vermeer paintings. It loads the data, combines and z-scores it, loads region mask_means
and applies them to find mean p-image values for each region for each condition. Then it does
t-tests across paintings to test for signifcance in difference between activations for the
the two attention conditions for the face and vase regions.

"""

Subject = "S1_2015"

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

folders_dic['attend_scene'] = ([1.],[
	opj(path,'attend_scene/subjects/S1_2015/2015/2/3/0/stats/p_images/png_std/a')])

folders_dic['attend_space_near_face'] = ([1.],[
	opj(path,'attend_space_near_face/subjects/S1_2015/2015/2/3/0/stats/p_images/png_std/a')])

folders_dic['attend_space_near_vase'] = ([1.],[
	opj(path,'attend_space_near_vase/subjects/S1_2015/2015/2/3/0/stats/p_images/png_std/a')])

folders_dic['attend_object'] = ([1.],[
	opj(path,'attend_object')])

folders_dic['attend_body'] = ([1.],[
	opj(path,'attend_body')])


mask = zeros((128,128))
mask2 = mask.copy()
mask2[19:109,2:126] = 1.
mask[30:128-30,20:108]=1. ;mask[128/2-12:128/2+12,128/2-12:128/2+12]=0.

mask_dic = {}
mask_dic['vase'] = {}
mask_dic['face'] = {}
mask_dic['space_near_vase'] = {}
mask_dic['space_near_face'] = {}

mask_dic['vase']['2.png'] = 'Vermeer_2_mask_vase.png'
mask_dic['vase']['3.png'] = 'Vermeer_3_mask_vase.png'
mask_dic['vase']['4.png'] = 'Vermeer_4_mask_vase.png'
mask_dic['vase']['5.png'] = 'Vermeer_5_mask_vase.png'
mask_dic['vase']['8.png'] = 'Vermeer_2_mask_vase.png'
mask_dic['vase']['9.png'] = 'Vermeer_3_mask_vase.png'
mask_dic['vase']['10.png'] = 'Vermeer_4_mask_vase.png'
mask_dic['vase']['11.png'] = 'Vermeer_5_mask_vase.png'

mask_dic['face']['2.png'] = 'Vermeer_2_mask_face.png'
mask_dic['face']['3.png'] = 'Vermeer_3_mask_face.png'
mask_dic['face']['4.png'] = 'Vermeer_4_mask_face.png'
mask_dic['face']['5.png'] = 'Vermeer_5_mask_face.png'
mask_dic['face']['8.png'] = 'Vermeer_2_mask_face.png'
mask_dic['face']['9.png'] = 'Vermeer_3_mask_face.png'
mask_dic['face']['10.png'] = 'Vermeer_4_mask_face.png'
mask_dic['face']['11.png'] = 'Vermeer_5_mask_face.png'

mask_dic['space_near_vase']['2.png'] = 'Vermeer_2_mask_vase.png'
mask_dic['space_near_vase']['3.png'] = 'Vermeer_3_mask_vase.png'
mask_dic['space_near_vase']['4.png'] = 'Vermeer_4_mask_vase.png'
mask_dic['space_near_vase']['5.png'] = 'Vermeer_5_mask_vase.png'
mask_dic['space_near_vase']['8.png'] = 'Vermeer_2_mask_vase.png'
mask_dic['space_near_vase']['9.png'] = 'Vermeer_3_mask_vase.png'
mask_dic['space_near_vase']['10.png'] = 'Vermeer_4_mask_vase.png'
mask_dic['space_near_vase']['11.png'] = 'Vermeer_5_mask_vase.png'

mask_dic['space_near_face']['2.png'] = 'Vermeer_2_mask_vase.png'
mask_dic['space_near_face']['3.png'] = 'Vermeer_3_mask_vase.png'
mask_dic['space_near_face']['4.png'] = 'Vermeer_4_mask_vase.png'
mask_dic['space_near_face']['5.png'] = 'Vermeer_5_mask_vase.png'
mask_dic['space_near_face']['8.png'] = 'Vermeer_2_mask_vase.png'
mask_dic['space_near_face']['9.png'] = 'Vermeer_3_mask_vase.png'
mask_dic['space_near_face']['10.png'] = 'Vermeer_4_mask_vase.png'
mask_dic['space_near_face']['11.png'] = 'Vermeer_5_mask_vase.png'


blank = zeros((128,128))
mask_path = opjD('19July2015_1Jan2016_p-imaging_results/S1_2015_HVO_images_and_masks/Vermeer_masks')
for t in mask_dic:
	for n in mask_dic[t]:
		blank = 0*blank
		blank[16:96+16] = z2o(imread(opj(mask_path,mask_dic[t][n]))[:,:,0])
		mask_dic[t][n] = mask2 * blank



def process_p_images(folders_dic,task,mask_dic,position,stats_dic):

	stats_dic[d2c(task,position)] = {}

	weights = folders_dic[task][0]
	folders = folders_dic[task][1]

	img_dic = {}
	img_mean_dic = {}


	thresh = 10.

	for f,w in zip(folders,weights):
		print (f,w)
		imgs = sorted(gg(opj(f,'*.png')))
		print imgs
		for i in imgs:
			img = 1.0*imread(i)
			print i
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
	figure(d2c(task,position)); clf()
	for k in sorted(img_dic.keys(),key=natural_keys):

		ctr += 1

		img_mean_dic[k] = array(img_dic[k]).mean(axis=0) / weights_sum
		#print k
		#mi(img_mean_dic[k],k)
		do_clf = False
		if ctr == 1:
			do_clf = True
		values = []
		if k in mask_dic[position]:
			for x in range(128):
				for y in range(128):
					if mask_dic[position][k][x,y] > 0.5:
						values.append(img_mean_dic[k][x,y])
			vmean = array(values).mean()
			stats_dic[d2c(task,position)][k] = vmean
		else:
			vmean = 'not measured'
		if k in mask_dic[position]:
			mi(img_mean_dic[k]+0*mask_dic[position][k],d2c(task,position),[4,3,ctr],do_clf=do_clf,img_title=d2s(k,vmean))
			unix('mkdir -p '+opjD(Subject),False)
			#print opjD(Subject,d2f('_',k,task)+'.png')
			imsave(opjD(Subject,d2f('_',k,task)+'.png'),img_mean_dic[k])

from scipy import stats

stats_dic = {}
for task in folders_dic.keys():#['attend_face','attend_vase','read_letters']:
	for position in mask_dic.keys():
		process_p_images(folders_dic,task,mask_dic,position,stats_dic)

for position in mask_dic.keys():
	for task in folders_dic.keys():#['attend_face','attend_vase','read_letters']:
		keys = sorted(stats_dic[d2c(task,position)],key=natural_keys)
		mask_means = []
		for k in keys:
			mask_means.append(stats_dic[d2c(task,position)][k])
		mask_means = array(mask_means)
		stats_dic[d2c(task,position)] = mask_means
		stats_dic[d2c(task,position),'SE'] = mask_means.std()/sqrt(len(mask_means))	
		stats_dic[d2c(task,position,'mean')] = mask_means.mean()


"""
for position in ['face','vase']:
	T = stats.ttest_ind(stats_dic[d2c('attend_face',position)],stats_dic[d2c('attend_vase',position)],False)
	print(position,T[1])

Result:
('face', 0.038216524611342624)
('vase', 0.032202046408711389)
i.e., attending to face vs. vase yields statistially different p-image values in both
face and face regions across all four paintings.

for position in ['face','vase']:
	T = stats.ttest_ind(stats_dic[d2c('attend_face',position)],stats_dic[d2c('read_letters',position)],False)
	print(position,T[1])

"""


read_letters_face = stats_dic['read_letters,face']
read_letters_vase = stats_dic['read_letters,vase']
attend_face_face =  stats_dic['attend_face,face']
attend_face_vase = 	stats_dic['attend_face,vase']
attend_vase_face = 	stats_dic['attend_vase,face']
attend_vase_vase = 	stats_dic['attend_vase,vase']

figure('S1_2015');clf();xlim(-1,2);ylim(-1,2);plt_square()
"""
for i in range(len(read_letters_face)):
	plot([read_letters_face[i],attend_face_face[i]],[read_letters_vase[i],attend_face_vase[i]],'r-')
	plot([read_letters_face[i],attend_vase_face[i]],[read_letters_vase[i],attend_vase_vase[i]],'b-')
plot(read_letters_face,read_letters_vase,'go')
plot(attend_vase_face,attend_vase_vase,'bo')
plot(attend_face_face,attend_face_vase,'ro')
"""

from kzpy3.teg2.gps_fence.geometry import *

attend_face_angles = []
attend_vase_angles = []
attend_face_mags = []
attend_vase_mags = []
figure(Subject);clf();xlim(-2,3);ylim(-2,3);plt_square()
for i in range(len(read_letters_face)):
	plot([read_letters_face[i],attend_face_face[i]],[read_letters_vase[i],attend_face_vase[i]],'r-')
	plot([read_letters_face[i],attend_vase_face[i]],[read_letters_vase[i],attend_vase_vase[i]],'b-')
	a = angle_clockwise([attend_face_face[i]-read_letters_face[i],attend_face_vase[i]-read_letters_vase[i]],[1,0])
	if a > 180:
		a = a - 360
	m = sqrt((attend_face_face[i]-read_letters_face[i])**2 + (attend_face_vase[i]-read_letters_vase[i])**2)
	attend_face_angles.append(a)
	attend_face_mags.append(m)
	a = angle_clockwise([attend_vase_face[i]-read_letters_face[i],attend_vase_vase[i]-read_letters_vase[i]],[1,0])
	if a > 180:
		a = a - 360
	m = sqrt((attend_vase_face[i]-read_letters_face[i])**2 + (attend_vase_vase[i]-read_letters_vase[i])**2)
	attend_vase_angles.append(a)
	attend_vase_mags.append(m)
	print (attend_face_angles[-1],attend_vase_angles[-1],attend_face_mags[-1],attend_vase_mags[-1])
	pause(3)
plot(read_letters_face,read_letters_vase,'go')
plot(attend_vase_face,attend_vase_vase,'bo')
plot(attend_face_face,attend_face_vase,'ro')

T = stats.ttest_ind(attend_face_angles,attend_vase_angles,False)
print(d2s('angles, t-test, p <',T[1]))
T = stats.ttest_ind(attend_face_mags,attend_vase_mags,False)
print(d2s('mags, t-test, p <',T[1]))


"""

angles, t-test, p < 0.0190208738727
mags, t-test, p < 0.00168147982864



"""


for i in range(2,6):
	painting = scipy.misc.imresize(imread(opjD(d2n('19July2015_1Jan2016_p-imaging_results/S1_2015_HVO_images_and_masks/Vermeer_512/Vermeer_',i,'.jpg'))),[768,1024])
	for task in folders_dic.keys():#['attend_face','attend_vase','read_letters']:
		img = imread(opjD(d2n('19July2015_1Jan2016_p-imaging_results/p_images_alone/combined/',Subject,'/',i,'.png_',task,'.png')))
		avg_img_big = scipy.misc.imresize(img[(128-96)/2:128-(128-96)/2],[768,1024])
		ci = yb_color_modulation_of_grayscale_image(painting,z2o(avg_img_big)**3.0,(1.0-z2o(avg_img_big))**3.0)
		imsave(opjD(d2f('-',Subject,task,i)+'.png'),ci[25:744,25:1003])
