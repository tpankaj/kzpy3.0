from kzpy3.utils import *
from kzpy3.misc.progress import *
import nibabel as nib
import nipy
import scipy.spatial

"""
import kzpy3.fMRI.data.preprocess_part_VI;reload(kzpy3.fMRI.data.preprocess_part_VI);from kzpy3.fMRI.data.preprocess_part_VI import *

13 Nov. 2015
e.g.,
make_p_images(opjD(''),'S1_2015',2015,7,10,0,'pp_a0',['Wedge_annulus'],['sequence1','sequence2'],'Phase_two_BIC_research','all',USE_Z_SCORING=True)
"""

def make_p_images(work_path,subject,year,month,day,session,pp,sub_experiments,conditions,experiment,num_to_average,
		mapping_year=False,mapping_month=False,mapping_day=False,mapping_session=False,mapping_pp=False,USE_Z_SCORING=False):
	'''
	'''
	if not mapping_year:
	    mapping_year = year
	if not mapping_month:
	    mapping_month = month
	if not mapping_day:
	    mapping_day = day
	if not mapping_session:
	    mapping_session = session
	if not mapping_pp:
	    mapping_pp = pp

	USE_STD_SCORING = not USE_Z_SCORING

	print('USE_Z_SCORING = ' + str(USE_Z_SCORING))

	print('Loading RF stats')
	rf_path = opj(work_path,'Research/data/subjects',subject,str(mapping_year),str(mapping_month),str(mapping_day),str(mapping_session),'stats',mapping_pp)
	rf_x_vol_nii = nib.load(opj(rf_path,'rf_x_vol.Wedge_annulus.nii.gz'))
	rf_y_vol_nii = nib.load(opj(rf_path,'rf_y_vol.Wedge_annulus.nii.gz'))
	rf_r_vol_nii = nib.load(opj(rf_path,'rf_r_vol.Wedge_annulus.nii.gz'))
	std1_vol_nii = nib.load(opj(work_path,'Research/data/experiments',experiment,'Wedge_annulus/sequence1/subjects',subject,str(mapping_year),str(mapping_month),str(mapping_day),str(mapping_session),'stats',mapping_pp,'all_average.nii.gz'))
	std2_vol_nii = nib.load(opj(work_path,'Research/data/experiments',experiment,'Wedge_annulus/sequence2/subjects',subject,str(mapping_year),str(mapping_month),str(mapping_day),str(mapping_session),'stats',mapping_pp,'all_average.nii.gz'))
	rf_x_vol=rf_x_vol_nii.get_data()
	rf_y_vol=rf_y_vol_nii.get_data()
	rf_r_vol=rf_r_vol_nii.get_data()
	std1_vol = std1_vol_nii.get_data()
	std2_vol = std2_vol_nii.get_data()

	print(experiment)
	for sub_ex in sub_experiments:
		print('\t'+sub_ex)
		for task in conditions:
			print('\t\t'+task)
			stats_path = opj(work_path,'Research/data/experiments',experiment,sub_ex,task,'subjects',subject,str(year),str(month),str(day),str(session),'stats',pp)
			print('\t\t\tload ' + opj(stats_path,'betas.nipy_GLM.nii.gz'))
			nii1=nib.load(opj(stats_path,'betas.nipy_GLM.nii.gz'))
			aa1 = nii1.get_data()


			points = []
			selected_xyz = []

			for x in range(np.shape(rf_x_vol)[0]):
			    for y in range(np.shape(rf_x_vol)[1]):
			        for z in range(np.shape(rf_x_vol)[2]):
			            if rf_r_vol[x,y,z] > 0.9:
			                points.append([rf_x_vol[x,y,z],rf_y_vol[x,y,z]])
			                selected_xyz.append([x,y,z])
			print(len(selected_xyz))

			xy2p,p2xys = get_mappings(points,W=128,N=30)

			z_aa1 = 0.0*aa1



			if USE_Z_SCORING:
			    for xyz in selected_xyz:
			        x,y,z = xyz[0],xyz[1],xyz[2]
			        sd = np.std(aa1[x,y,z,:])
			        if np.isfinite(sd):
			            if not sd == 0:
			                z_aa1[x,y,z,:] = aa1[x,y,z,:] - np.mean(aa1[x,y,z,:])
			                z_aa1[x,y,z,:] /= sd
			elif USE_STD_SCORING:
			    for xyz in selected_xyz:
			        x,y,z = xyz[0],xyz[1],xyz[2]
			        sd = (np.std(std1_vol[x,y,z,:])+np.std(std2_vol[x,y,z,:]))/2.0#np.std(aa1[x,y,z,:])#
			        if np.isfinite(sd):
			            if not sd == 0:
			                z_aa1[x,y,z,:] = aa1[x,y,z,:] - aa1[x,y,z,-1] # NOTE, EXPECT LAST STIMULUS TO BE THE BLANK!!!! #np.mean(aa1[x,y,z,:]) #np.mean(aa1[x,y,z,:])
			                z_aa1[x,y,z,:] /= sd
			else:
			    os.sys.exit('UNKNOWING SCORING')


			p_image_png_dir = opj(stats_path,'p_images/png_std')
			p_image_npy_dir = opj(stats_path,'p_images/npy')
			os.system('mkdir -p ' + p_image_png_dir)
			os.system('mkdir -p ' + p_image_npy_dir)
			for TR in range(np.shape(aa1)[3]):
			    vs = []
			    for xyz in selected_xyz:
			        vs.append(z_aa1[xyz[0],xyz[1],xyz[2],TR])
			    img = get_activation_image_new(xy2p,vs,W=128,num_to_average=num_to_average)
			    scipy.misc.imsave(opj(p_image_png_dir,str(TR)+'.png'),img)
			    np.save(opj(p_image_npy_dir,str(TR)+'.npy'),img)



def get_activation_image_new(xy2p,vs,H=96,W=128,num_to_average = 'all'):
	X,Y = H,W
	img3 = np.zeros((H,W))
	if num_to_average == 'all':
		num_to_average = len(xy2p[0,0][1]) # need to insure this will be a good coordinate
	else:
		assert num_to_average > 0
		assert num_to_average <= len(xy2p[0,0][1])
	for x in range(X):
		for y in range(Y):
			v = 0.0
			for i in range(num_to_average):
				j = np.int(xy2p[x,y][1][i])
				v += vs[j]
				img3[x,y] = v/num_to_average
	return img3






def get_points(W = 512,parameter = 0.8649):
    X,Y = W,W
    points = []
    a = np.zeros((X,Y))
    for x in range(X):
        for y in range(Y):
            r = np.sqrt((x-W/2.0)**2+(y-W/2.0)**2)/(W/2.0*np.sqrt(2.0))
            #r = np.max((0.75,r))
            if r > 0.995:
                r = 0.995
            if np.random.rand() > r:
                if np.random.rand() > parameter:
                    a[x,y] = 1
                    points.append([x,y])
    points = np.array(points)                
    mi(a, img_title = str(np.sum(a)/(W**2)))
    return points

def get_points_SPECIAL_384x512(W = 512,parameter = 0.8649):
    X,Y = W,W
    points = []
    a = np.zeros((X,Y))
    for x in range(63,384+64):
        for y in range(Y):
            r = np.sqrt((x-W/2.0)**2+(y-W/2.0)**2)/(W/2.0*np.sqrt(2.0))
            #r = np.max((0.75,r))
            if r > 0.995:
                r = 0.995
            if np.random.rand() > r:
                if np.random.rand() > parameter:
                    a[x,y] = 1
                    points.append([x,y])
    points = np.array(points)                
    mi(a, img_title = str(np.sum(a)/(W**2)))
    return points

def get_points_SPECIAL_1(W = 512,parameter = 0.8649):
    X,Y = W,W
    points = []
    a = np.zeros((X,Y))
    for x in range(X):
        for y in range(Y):
            if (x>200 and x<300) and (y>200 and y<300):
                r = 0.98
            else:
                r = np.sqrt((x-W/2.0)**2+(y-W/2.0)**2)/(W/2.0*np.sqrt(2.0))
            if r > 0.995:
                r = 0.995
            if np.random.rand() > r:
                if np.random.rand() > parameter:
                    a[x,y] = 1
                    points.append([x,y])
    points = np.array(points)                
    mi(a, img_title = str(np.sum(a)/(W**2)))
    return points

def get_points_SPECIAL_2(W = 512,parameter = 0.8649):
    X,Y = W,W
    points = []
    a = np.zeros((X,Y))
    for x in range(X):
        for y in range(Y):
            r = 2*np.sqrt((x-W/2.0)**2+(y-W/2.0)**2)/(W/2.0*np.sqrt(2.0))
            if r > 0.995:
                r = 0.995
            if np.random.rand() > r:
                if np.random.rand() > parameter:
                    a[x,y] = 1
                    points.append([x,y])
    points = np.array(points)                
    mi(a, img_title = str(np.sum(a)/(W**2)))
    return points

def get_mappings(points,W=512,N = 30):
    tree = scipy.spatial.KDTree(points)
   
    X,Y = W,W
    xy2p = np.zeros((W,W,2,N))

    pb = ProgressBar(X)
    for x in range(X):
        pb.animate(x+1)
        for y in range(Y):
            xy2p[x,y] = tree.query([x,y],N)
    p2xys = {}
    for p in range(len(points)):
        p2xys[p] = []
    pb = ProgressBar(X)
    for x in range(X):
        pb.animate(x+1)
        for y in range(Y):
            p2xys[xy2p[x,y][1][0]].append([x,y])
    return xy2p,p2xys

def get_mappings_SPECIAL_384x512(points,W=512):
    tree = scipy.spatial.KDTree(points)
    N = 5
    X,Y = W,W
    xy2p = np.zeros((W,W,2,N))

    pb = kzpy.img.ProgressBar(X)
    for x in range(63,384+64):
        pb.animate(x+1)
        for y in range(Y):
            xy2p[x,y] = tree.query([x,y],N)
    p2xys = {}
    for p in range(len(points)):
        p2xys[p] = []
    pb = kzpy.img.ProgressBar(X)
    for x in range(63,384+64):
        pb.animate(x+1)
        for y in range(Y):
            p2xys[xy2p[x,y][1][0]].append([x,y])
    return xy2p,p2xys

def get_activations(p2xys,img):
    vs = np.zeros(len(p2xys))
    for i in range(len(p2xys)):
        v = 0.0;
        ctr = 0.0;
        for p in p2xys[i]:
            v += img[p[0],p[1]]
            ctr += 1.0
        vs[i] = v/ctr
    return vs

def get_activation_image(xy2p,vs,W=512):
    X,Y = W,W
    img3 = np.zeros((W,W))
    for x in range(X):
        for y in range(Y):
            v = 0.0
            j = xy2p[x,y][1][0]
            v = vs[j]
            img3[x,y] = v
    return img3

def get_activation_image_avg(xy2p,vs,W=512):
    X,Y = W,W
    img3 = np.zeros((W,W))
    for x in range(X):
        for y in range(Y):
            v = 0.0
            for i in range(len(xy2p[x,y][1])):
                j = xy2p[x,y][1][i]
                v += vs[j]
            img3[x,y] = v/float(len(xy2p[x,y][1]))
    return img3

def get_activation_image_new(xy2p,vs,W=512,num_to_average = 'all'):
    X,Y = W,W
    img3 = np.zeros((W,W))
    if num_to_average == 'all':
        num_to_average = len(xy2p[0,0][1]) # need to insure this will be a good coordinate
    else:
        assert num_to_average > 0
        assert num_to_average <= len(xy2p[0,0][1])
    for x in range(X):
        for y in range(Y):
            v = 0.0
            for i in range(num_to_average):
                j = np.int(xy2p[x,y][1][i])
                v += vs[j]
            img3[x,y] = v/num_to_average
    return img3

def get_activation_image_SPECIAL_384x512(xy2p,vs,W=512):
    X,Y = W,W
    img3 = np.zeros((W,W))
    for x in range(63,384+64):
        for y in range(Y):
            v = 0.0
            j = xy2p[x,y][1][0]
            v = vs[j]
            img3[x,y] = v
    return img3



