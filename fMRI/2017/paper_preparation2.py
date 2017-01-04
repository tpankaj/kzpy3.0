"""
2 January 2016

This script looks at results from scanning S1_2014 and S6_2015 during attend-vase or attend-face tasks
with Vermeer paintings. It loads the data, combines and z-scores it, loads region mask_means
and applies them to find mean p-image values for each region for each condition. Then it does
t-tests across paintings to test for signifcance in difference between activations for the
the two attention conditions for the face and vase regions.

"""



folders_dic = {}


if True:
	Subject = 'S1_2014'
	path = '/Users/karlzipser/Desktop/19July2015_1Jan2016_p-imaging_results/p_images_alone/S1_2014_reorganized'

	folders_dic['attend_face'] = ([8.,2.],[
		opj(path,'attend_face/a_8'),
		opj(path,'attend_face/b_2')])

	folders_dic['attend_vase'] = ([8.,2.],[
		opj(path,'attend_vase/a_8'),
		opj(path,'attend_vase/b2')])

	folders_dic['read_letters'] = ([8.,2.],[
		opj(path,'read_letters/a_8'),
		opj(path,'read_letters/b_2')])


if False:
	Subject = 'S6_2015'
	path = '/Users/karlzipser/Desktop/19July2015_1Jan2016_p-imaging_results/p_images_alone/S6_2015_reorganized'

	folders_dic['attend_face'] = ([1.],[
		opj(path,'attend_face/a')])

	folders_dic['attend_vase'] = ([1.],[
		opj(path,'attend_vase/a')])

	folders_dic['read_letters'] = ([1.],[
		opj(path,'read_letters/a')])



mask = zeros((128,128))
mask2 = mask.copy()
mask2[19:109,2:126] = 1.
#mask[19:109,2:126] = 1.
mask[30:128-30,20:108]=1.
q = 6
mask[128/2-q:128/2+q,128/2-q:128/2+q]=0.

mask_dic = {}
mask_dic['vase'] = {}
mask_dic['face'] = {}

mask_dic['vase']['1.png'] = '1_vase.png'
mask_dic['vase']['2.png'] = '2_vase.png'
mask_dic['vase']['3.png'] = '3_vase.png'
mask_dic['vase']['4.png'] = '4_vase.png'

mask_dic['face']['1.png'] = '1_face.png'
mask_dic['face']['2.png'] = '2_face.png'
mask_dic['face']['3.png'] = '3_face.png'
mask_dic['face']['4.png'] = '4_face.png'


blank = zeros((128,128))
mask_path = opjD('/Users/karlzipser/Desktop/19July2015_1Jan2016_p-imaging_results/S1_2014_S6_2015_images_and_masks/Vermeer_masks')
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


	thresh = 2.5
	blank = zeros((128,128))

	for f,w in zip(folders,weights):
		blank = 0*blank
		print (f,w)
		imgs = sorted(gg(opj(f,'*.png')))
		for i in imgs:
			img = 1.0*imread(i)
			blank[16:96+16] = img
			img = blank.copy()
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
			mi(img_mean_dic[k]+0*mask+0*mask_dic[position][k],d2c(task,position),[2,3,ctr],do_clf=do_clf,img_title=d2s(k,vmean))
			unix('mkdir -p '+opjD(Subject),False)
			imsave(opjD(Subject,d2f('_',k,task)+'.png'),img_mean_dic[k])
if True:
	from scipy import stats

	stats_dic = {}
	for task in ['attend_face','attend_vase','read_letters']:
		for position in ['face','vase']:
			process_p_images(folders_dic,task,mask_dic,position,stats_dic)

	for position in ['face','vase']:
		for task in ['attend_face','attend_vase','read_letters']:
			keys = sorted(stats_dic[d2c(task,position)],key=natural_keys)
			mask_means = []
			for k in keys:
				mask_means.append(stats_dic[d2c(task,position)][k])
			mask_means = array(mask_means)
			stats_dic[d2c(task,position)] = mask_means
			stats_dic[d2c(task,position),'SE'] = mask_means.std()/sqrt(len(mask_means))	
			stats_dic[d2c(task,position,'mean')] = mask_means.mean()


read_letters_vase = stats_dic['read_letters,vase']
read_letters_face = stats_dic['read_letters,face']
attend_face_face =  stats_dic['attend_face,face']
attend_face_vase = 	stats_dic['attend_face,vase']
attend_vase_face = 	stats_dic['attend_vase,face']
attend_vase_vase = 	stats_dic['attend_vase,vase']


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
	#pause(3)
plot(read_letters_face,read_letters_vase,'go')
plot(attend_vase_face,attend_vase_vase,'bo')
plot(attend_face_face,attend_face_vase,'ro')

T = stats.ttest_ind(attend_face_angles,attend_vase_angles,False)
print(d2s('angles, t-test, p <',T[1]))
T = stats.ttest_ind(attend_face_mags,attend_vase_mags,False)
print(d2s('mags, t-test, p <',T[1]))




"""
S1_2014

angles, t-test, p < 0.0426980550935
mags, t-test, p < 0.00168147982864

S6_2015
angles, t-test, p < 0.000398548924289
mags, t-test, p < 0.50678221641

S1_2015
angles, t-test, p < 0.000957474881117
mags, t-test, p < 0.0100226128327

"""

pass

for i in range(1,5):
	painting = imread(opjD(d2n('19July2015_1Jan2016_p-imaging_results/S1_2014_S6_2015_images_and_masks/Vermeer_images/',i,'.png')))
	for task in ['attend_face','attend_vase','read_letters']:
		img = imread(opjD(d2n('19July2015_1Jan2016_p-imaging_results/p_images_alone/combined/',Subject,'/',i,'.png_',task,'.png')))
		avg_img_big = scipy.misc.imresize(img[(128-96)/2:128-(128-96)/2],[768,1024])
		ci = yb_color_modulation_of_grayscale_image(painting,z2o(avg_img_big)**3.0,(1.0-z2o(avg_img_big))**3.0)
		imsave(opjD(d2f('-',Subject,task,i)+'.png'),ci[25:744,25:1003])
