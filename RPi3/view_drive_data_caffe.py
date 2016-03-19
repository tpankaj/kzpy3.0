from kzpy3.RPi3.view_drive_data_essentials import *

CAFFE_TRAINING_MODE = 'CAFFE_TRAINING_MODE'
CAFFE_BVLC_REF_CAT_TRAINING_MODE = 'CAFFE_BVLC_REF_CAT_TRAINING_MODE'
CAFFE_BVLC_REF_TRAINING_MODE = 'CAFFE_BVLC_REF_TRAINING_MODE'
CAFFE_CAT_TRAINING_MODE = 'CAFFE_CAT_TRAINING_MODE'
MC_CAFFE_TRAINING_MODE = 'MC_CAFFE_TRAINING_MODE'
MC_CAFFE_CAT_TRAINING_MODE = 'MC_CAFFE_CAT_TRAINING_MODE'
CAFFE_DEPLOY_MODE = 'CAFFE_DEPLOY_MODE'
MC_CAFFE_DEPLOY_MODE = 'MC_CAFFE_DEPLOY_MODE'
USE_GRAPHICS = 'USE_GRAPHICS'
SAVE_ALL_RUN_DIC = 'SAVE_ALL_RUN_DIC'

run_mode = CAFFE_DEPLOY_MODE
#run_mode = CAFFE_TRAINING_MODE
#CAFFE_DATA = opjh('Desktop/RPi3_data/runs_scale_50_BW')
#CAFFE_FRAME_RANGE = (-15,-6) # (-7,-6)# 
CAFFE_DATA = opjh('Desktop/RPi3_data/runs_scl_100_RGB_test')
CAFFE_FRAME_RANGE = (-7,-6)# 

# all_runs_dic = load_objh('Desktop/RPi3_data/all_runs_dics/runs_scale_50_BW')

print(d2s('*** run_mode =',run_mode))

def get_steer_bins(all_runs_dic):
    steer_bins = {}
    steer_bins['left_max'] = []
    steer_bins['left'] = []
    steer_bins['left_min'] = []
    steer_bins['center'] = []
    steer_bins['right_min'] = []
    steer_bins['right'] = []
    steer_bins['right_max'] = []
    for k in all_runs_dic:
        print k
        run_data_dic = all_runs_dic[k]
        for i in range(len(run_data_dic['train_frames'])):
            t = run_data_dic['train_frames'][i]
            if t:
                #f = run_data_dic['img_lst'][i]
                if run_data_dic['steer'][i] < -0.6:
                    steer_bins['left_max'].append((k,i))
                elif run_data_dic['steer'][i] < -0.3:
                    steer_bins['left'].append((k,i))
                elif run_data_dic['steer'][i] < -0.05:
                    steer_bins['left_min'].append((k,i))
                elif run_data_dic['steer'][i] <= 0.05:
                    steer_bins['center'].append((k,i))
                elif run_data_dic['steer'][i] <= 0.3:
                    steer_bins['right_min'].append((k,i))
                elif run_data_dic['steer'][i] <= 0.6:
                    steer_bins['right'].append((k,i))
                elif run_data_dic['steer'][i] <= 1:
                    steer_bins['right_max'].append((k,i))
                else:
                    raise Exception('get_steer_bins error!')
    return steer_bins
def steer_bin_medians(steer_bins,all_runs_dic):
    m = []
    for b in steer_bins:
        lst = []
        for q in steer_bins[b]:
            lst.append(all_runs_dic[q[0]]['steer'][q[1]])
        m.append((b,np.median(lst),len(steer_bins[b])))
    return m
def get_rand_frame_data(steer_bins,all_runs_dic,frame_range=(-15,-6),Graphics=False):
    sbks = steer_bins.keys() + ['center'] # This + ['center'] has the effect of doubling the chance of center position result.
    b = sbks[np.random.randint(len(sbks))]
    ardks = all_runs_dic.keys()
    l = len(steer_bins[b])
    e = steer_bins[b][np.random.randint(l)]
    r = e[0]
    n = e[1]
    steer = int(100.0*all_runs_dic[r]['steer'][n])
    frames_to_next_turn = int(all_runs_dic[r]['frames_to_next_turn'][n])
    rps = int(10.0*all_runs_dic[r]['rps'][n])
    frame_names = []
    for i in range(frame_range[0]+n,frame_range[1]+n):
        frame_names.append(opj(all_runs_dic[r]['run_path'],all_runs_dic[r]['img_lst'][i]))
    return (b,r,n,steer,frames_to_next_turn,rps,frame_names)
def categorize_steer(s):
    bs = s * 7 * 0.9999
    return np.int(np.floor(bs))
def blurred_steer(c):
    if c == 0:
        s = [5,2,1,0,0,0,0]
    elif c == 1:
        s = [2,5,2,1,0,0,0]
    elif c == 2:
        s = [1,2,5,2,1,0,0]
    elif c == 3:
        s = [0,1,2,5,2,1,0]
    elif c == 4:
        s = [0,0,1,2,5,2,1]
    elif c == 5:
        s = [0,0,0,1,2,5,2]
    elif c == 6:
        s = [0,0,0,0,1,2,5]
    else:
        assert(False)
    assert len(s) == 7
    return list(z2o(np.array(s)))

if run_mode == CAFFE_TRAINING_MODE:
    all_runs_dic = get_all_runs_dic(CAFFE_DATA)
    steer_bins = get_steer_bins(all_runs_dic)
    def get_caffe_input_target(img_dic,steer_bins,all_runs_dic,frame_range=(-15,-6)):
        b,r,n,steer,frames_to_next_turn,rps,frame_names = get_rand_frame_data(steer_bins,all_runs_dic,frame_range)
        img_lst = []
        for f in frame_names:
            img_lst.append(imread_from_img_dic(img_dic,'',f)/255.0-0.5)
        if len(img_lst) == 1 and len(np.shape(img_lst[0])) == 3:
            img = img_lst[0]
            img_lst = [img[:,:,0],img[:,:,1],img[:,:,2]]
        S = steer/200.0 + 0.5
        assert(S>=0)
        assert(S<=1)
        F = frames_to_next_turn/45.0
        F = min(F,1.0)
        assert(F>=0)
        assert(F<=1)
        R = rps/75.0
        R = min(R,1.0)
        assert(R>=0)
        assert(R<=1)
        return img_lst,[S,0*F,0*R] #steer only, 17 Feb 2015 trianing
        #return img_lst,[S,F,R]

elif run_mode == CAFFE_CAT_TRAINING_MODE:
    all_runs_dic = get_all_runs_dic(CAFFE_DATA)
    steer_bins = get_steer_bins(all_runs_dic)
    def get_caffe_input_target(img_dic,steer_bins,all_runs_dic,frame_range=(-15,-6)):
        b,r,n,steer,frames_to_next_turn,rps,frame_names = get_rand_frame_data(steer_bins,all_runs_dic,frame_range)
        img_lst = []
        for f in frame_names:
            img_lst.append(imread_from_img_dic(img_dic,'',f)/255.0-0.5)
        if len(img_lst) == 1 and len(np.shape(img_lst[0])) == 3:
            img = img_lst[0]
            img_lst = [img[:,:,0],img[:,:,1],img[:,:,2]]
        S = steer/200.0 + 0.5
        assert(S>=0)
        assert(S<=1)
        steer_lst = [0,0,0,0,0,0,0]
        c = categorize_steer(S)
        assert(c<len(steer_lst))
        assert(c>=0)
        steer_lst[c] = 1.0
        return img_lst,steer_lst

elif run_mode == CAFFE_BVLC_REF_CAT_TRAINING_MODE or run_mode == CAFFE_BVLC_REF_TRAINING_MODE:
    #img_mask = np.zeros((3,227,227))+1.0
    #img_mask[:,:100,:] = 0.0
    import caffe
    # Here I use the image transformer code from the bvlc_reference net to get my images in the correct scaling and format
    # for the pretrained bvlc_reference net
    all_runs_dic = get_all_runs_dic(CAFFE_DATA)
    #all_runs_dic = load_obj(opjD('RPi3_data/all_runs_dics/runs_scl_100_RGB'))
    steer_bins = get_steer_bins(all_runs_dic)
    caffe_root = opjh('caffe')  # this file is expected to be in {caffe_root}/examples
    transformer = caffe.io.Transformer({'data': (1, 3, 227, 227)})
    transformer.set_transpose('data', (2,0,1))
    transformer.set_mean('data', np.load(opj(caffe_root,'python/caffe/imagenet/ilsvrc_2012_mean.npy')).mean(1).mean(1)) # mean pixel
    transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB
    def get_caffe_input_target(img_dic,steer_bins,all_runs_dic,frame_range=(-7,-6)):
        assert frame_range == (-7,-6) # i.e., we will only work with a single RGB image.
        b,r,n,steer,frames_to_next_turn,rps,frame_names = get_rand_frame_data(steer_bins,all_runs_dic,frame_range)
        img_lst = []
        for f in frame_names:
            cimg = caffe.io.load_image(f)
            cimg = cimg[105:,:,:]
            img_lst.append(transformer.preprocess('data',cimg))
        try:
            assert len(img_lst) == 1
            assert len(np.shape(img_lst[0])) == 3
        except:
            print "BIG PROBLEM!"
        img = img_lst[0]
        img_lst = [img[0,:,:],img[1,:,:],img[2,:,:]]
        S = steer/200.0 + 0.5
        assert(S>=0)
        assert(S<=1)
        if run_mode == CAFFE_BVLC_REF_CAT_TRAINING_MODE:
            steer_lst = [0,0,0,0,0,0,0]
            c = categorize_steer(S)
            assert(c<len(steer_lst))
            assert(c>=0)
            steer_lst = blurred_steer(c)
            return img_lst,steer_lst
        else:
            F = frames_to_next_turn/90.0
            F = min(F,1.0)
            assert(F>=0)
            assert(F<=1)
            R = rps/75.0
            R = min(R,1.0)
            assert(R>=0)
            assert(R<=1)
            return img_lst,[S,F,0*R]
        
# e.g.s for transforming filenames
# C_f='/Users/karlzipser/Desktop/RPi3_data/runs_scl_100_RGB/09Feb16_13h33m51s_scl=100_mir=0/0_1455053641.36_str=-6_spd=52_rps=0_lrn=125_rrn=105_rnd=0_scl=100_mir=0_.jpg'
# M_f='/Users/karlzipser/Desktop/RPi3_data/runs_scale_50_BW/09Feb16_13h33m51s_scl=50_mir=0/0_1455053641.36_str=-6_spd=52_rps=0_lrn=125_rrn=105_rnd=0_scl=50_mir=0_.png'
elif run_mode == MC_CAFFE_TRAINING_MODE:
    all_runs_dic = get_all_runs_dic(CAFFE_DATA)
    steer_bins = get_steer_bins(all_runs_dic)
    def get_caffe_input_target(img_dic,steer_bins,all_runs_dic,frame_range=(-15,-6)):
        b,r,n,steer,frames_to_next_turn,rps,frame_names = get_rand_frame_data(steer_bins,all_runs_dic,frame_range)
        M_img_lst = []
        C_img_lst = []
        for M_f in frame_names:
            M_img_lst.append(imread_from_img_dic(img_dic,'',M_f)/255.0-0.5)
        c_f = M_f # last frame is most recent
        c_f = c_f.replace('scale_50_BW','scl_100_RGB')
        c_f = c_f.replace('scl=50','scl=100')
        C_f = c_f.replace('png','jpg')
        C_img = imread_from_img_dic(img_dic,'',C_f)/255.0-0.5
        C_img_lst = [C_img[:,:,0],C_img[:,:,1],C_img[:,:,2]]
        S = steer/200.0 + 0.5
        assert(S>=0)
        assert(S<=1)
        F = frames_to_next_turn/45.0
        F = min(F,1.0)
        assert(F>=0)
        assert(F<=1)
        R = rps/75.0
        R = min(R,1.0)
        assert(R>=0)
        assert(R<=1)
        return M_img_lst,C_img_lst,[S,0*F,0*R]

elif run_mode == MC_CAFFE_CAT_TRAINING_MODE:
    all_runs_dic = get_all_runs_dic(CAFFE_DATA)
    steer_bins = get_steer_bins(all_runs_dic)
    def get_caffe_input_target(img_dic,steer_bins,all_runs_dic,frame_range=(-15,-6)):
        b,r,n,steer,frames_to_next_turn,rps,frame_names = get_rand_frame_data(steer_bins,all_runs_dic,frame_range)
        M_img_lst = []
        C_img_lst = []
        for M_f in frame_names:
            M_img_lst.append(imread_from_img_dic(img_dic,'',M_f)/255.0-0.5)
        c_f = M_f # last frame is most recent
        c_f = c_f.replace('scale_50_BW','scl_100_RGB')
        c_f = c_f.replace('scl=50','scl=100')
        C_f = c_f.replace('png','jpg')
        C_img = imread_from_img_dic(img_dic,'',C_f)/255.0-0.5
        C_img_lst = [C_img[:,:,0],C_img[:,:,1],C_img[:,:,2]]
        S = steer/200.0 + 0.5
        assert(S>=0)
        assert(S<=1)
        steer_lst = [0,0,0,0,0,0,0]
        c = categorize_steer(S)
        assert(c<len(steer_lst))
        assert(c>=0)
        steer_lst[c] = 1.0
        return M_img_lst,C_img_lst,steer_lst

elif run_mode == CAFFE_DEPLOY_MODE:
    img_top_folder = opjh('Desktop/RPi_data')
    _,img_dirs = dir_as_dic_and_list(img_top_folder)
    ctimes = []
    for d in img_dirs:
        ctimes.append(os.path.getmtime(opj(img_top_folder,d)))
    sort_indicies = [i[0] for i in sorted(enumerate(ctimes), key=lambda x:x[1])]
    most_recent_img_dir = img_dirs[sort_indicies[-1]]
    print most_recent_img_dir
    unix(d2s('mkdir -p',opj(img_top_folder,most_recent_img_dir+'_caffe')),False)
    def get_caffe_input_target(img_dic,_ignore1_,_ignore2_,_ignore3_):
        _,img_files = dir_as_dic_and_list(opj(img_top_folder,most_recent_img_dir))
        if len(img_files) > 9:
            img_lst = []
            for i in range(-10,-1): # = [-10, -9, -8, -7, -6, -5, -4, -3, -2]
                # we avoid loading the most recent image to avoid 'race' conditions.
                f = img_files[i]
                #print f
                img = imread_from_img_dic(img_dic,opj(img_top_folder,most_recent_img_dir),f)
                img = img.mean(axis=2)
                img = imresize(img,25)/255.0-0.5
                img_lst.append(img)
            if len(img_files) > 10:
                for f in img_files[:-10]:
                    unix(d2s('mv',opj(img_top_folder,most_recent_img_dir,f),opj(img_top_folder,most_recent_img_dir+'_caffe')),False)
        else:
            dummy = np.random.random((56,75))
            for i in range(9):
                img_lst.append(dummy)
        return img_lst,[0,0,0]

elif run_mode == MC_CAFFE_DEPLOY_MODE:
    img_top_folder = opjh('Desktop/RPi_data')
    _,img_dirs = dir_as_dic_and_list(img_top_folder)
    ctimes = []
    for d in img_dirs:
        ctimes.append(os.path.getmtime(opj(img_top_folder,d)))
    sort_indicies = [i[0] for i in sorted(enumerate(ctimes), key=lambda x:x[1])]
    most_recent_img_dir = img_dirs[sort_indicies[-1]]
    print most_recent_img_dir
    unix(d2s('mkdir -p',opj(img_top_folder,most_recent_img_dir+'_caffe')),False)
    def get_caffe_input_target(img_dic,_ignore1_,_ignore2_,_ignore3_):
        _,img_files = dir_as_dic_and_list(opj(img_top_folder,most_recent_img_dir))
        if len(img_files) > 9:
            M_img_lst = []
            C_img_lst = []
            for i in range(-10,-1): # = [-10, -9, -8, -7, -6, -5, -4, -3, -2]
                # we avoid loading the most recent image to avoid 'race' conditions.
                f = img_files[i]
                #print f
                img = imread_from_img_dic(img_dic,opj(img_top_folder,most_recent_img_dir),f)
                if i == -1:
                    C_img = img.copy()
                    C_img_lst = [C_img[:,:,0],C_img[:,:,1],C_img[:,:,2]]
                img = img.mean(axis=2)
                img = imresize(img,50)/255.0-0.5
                M_img_lst.append(img)
            if len(img_files) > 10:
                for f in img_files[:-10]:
                    unix(d2s('mv',opj(img_top_folder,most_recent_img_dir,f),opj(img_top_folder,most_recent_img_dir+'_caffe')),False)
        else:
            dummy = np.random.random((56,75))
            for i in range(9):
                img_lst.append(dummy)
        return M_img_lst,C_img_lst,[0,0,0]


elif run_mode == USE_GRAPHICS:
    from kzpy3.vis import *
    all_runs_dic = get_all_runs_dic(opjD('/Users/karlzipser/Desktop/RPi3_data/runs_checked'))
    k = sorted(all_runs_dic.keys())
    play_range = (0,15*15)
    some_data = {}
    some_data['current_key'] = k[0]
    some_data['all_runs_dic'] = all_runs_dic
    some_data['play_range'] = play_range

elif run_mode == SAVE_ALL_RUN_DIC:
    from kzpy3.utils import *
    all_runs_dic = get_all_runs_dic(CAFFE_DATA)
    save_obj(all_runs_dic,opjD('RPi3_data/all_runs_dics',CAFFE_DATA.split('/')[-1]))

else:
    print('Unknown mode')
    assert(False)









"""
Top priority items:

second car
second RPi
desktop linux machine
K40 GPU
budget (materials vs salary)
Jetson GPU

"""

    






