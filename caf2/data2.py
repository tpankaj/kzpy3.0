from kzpy3.caf2.data1 import *

def select_get_caffe_input_target(run_mode,CAFFE_DATA):
    if run_mode == CAFFE_TRAINING_MODE:
        if 'all_runs_dics' in CAFFE_DATA:
            all_runs_dic = load_obj(CAFFE_DATA)
        else: 
            all_runs_dic = get_all_runs_dic(CAFFE_DATA)
        steer_bins = get_steer_bins(all_runs_dic)
        def get_caffe_input_target(img_dic,steer_bins,all_runs_dic,frame_range=(-15,-6)):
            b,r,n,steer,frames_to_next_turn,rps,frame_names = get_rand_frame_data(steer_bins,all_runs_dic,frame_range)
            img_lst = []
            for f in frame_names:
                img = imread_from_img_dic(img_dic,'',f)/255.0-0.5
                #img = -img # temp
                img_lst.append(img)
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
            #return img_lst,[S,0*F,0*R] #steer only, 17 Feb 2015 trianing
            return img_lst,[S,F,R]

    elif run_mode == CAFFE_TRAJECTORY_TRAINING_MODE:
        if 'all_runs_dics' in CAFFE_DATA:
            all_runs_dic = load_obj(CAFFE_DATA)
        else: 
            all_runs_dic = get_all_runs_dic(CAFFE_DATA)
        steer_bins = get_steer_bins(all_runs_dic)
        def get_caffe_input_target(img_dic,steer_bins,all_runs_dic,frame_range=(-15,-6)):
            steer_lst,rps_lst,frame_names = get_rand_frame_trajectory_data(steer_bins,all_runs_dic,frame_range=(-15,-6),trajectory_range=(-15,15))
            img_lst = []
            for f in frame_names:
                img = imread_from_img_dic(img_dic,'',f)/255.0-0.5
                #img = -img # temp
                img_lst.append(img)
            if len(img_lst) == 1 and len(np.shape(img_lst[0])) == 3:
                img = img_lst[0]
                img_lst = [img[:,:,0],img[:,:,1],img[:,:,2]]
            
            S_lst = np.array(steer_lst)/200.0 + 0.5
            assert(S_lst.min()>=0)
            assert(S_lst.max()<=1)

            R_lst = np.array(rps_lst)/75.0
            R_lst[R_lst>1.0] = 1.0
            assert(R_lst.min()>=0)
            assert(R_lst.max()<=1)
            return img_lst,list(S_lst)+list(R_lst)

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

    else:
        print('Unknown mode')
        assert(False)

    return get_caffe_input_target


