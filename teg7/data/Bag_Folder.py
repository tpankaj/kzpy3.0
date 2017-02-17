from kzpy3.vis import *
import cv2

def init(bag_folders_path_meta_path,bag_folders_rgb_1to4_path, left_image_bound_to_data_name='left_image_bound_to_data.pkl',NUM_STATE_ONE_STEPS=10,accepted_states=[1]):

    BF = {}

    BF['path'] = bag_folders_rgb_1to4_path
    run_name = fname(bag_folders_rgb_1to4_path)
    cprint('Bag_Folder::__init__, run = '+run_name,'yellow','on_red')
    BF['bag_files'] = sorted(glob.glob(opj(bag_folders_rgb_1to4_path,'*.bag.pkl')))
    print opj(bag_folders_rgb_1to4_path,'*.bag.pkl')
    #cprint(d2s("""BF['bag_files'] =""",BF['bag_files']))
    if len(BF['bag_files']) == 0:
        cprint("if len(BF['bag_files']) == 0:",'red')
        return None
    BF['bag_file_num_dic'] = {}
    for bf in BF['bag_files']:
        n = atoi(bf.split('.bag')[-2].split('_')[-1])
        BF['bag_file_num_dic'][n] = bf
    left_path = opj(bag_folders_path_meta_path,left_image_bound_to_data_name)
    BF['left_image_bound_to_data'] = load_obj(left_path)

    if 'acc' not in an_element(BF['left_image_bound_to_data']):
        for ts in BF['left_image_bound_to_data']:
            BF['left_image_bound_to_data'][ts]['acc'] = [0.,9.8,0.]
    BF['data'] = {}
    BF['data']['raw_timestamps'] = sorted(BF['left_image_bound_to_data'].keys())

    BF['data']['raw_timestamp_deltas'] = [0]
    for i in range(1,len(BF['data']['raw_timestamps'])):
        BF['data']['raw_timestamp_deltas'].append(BF['data']['raw_timestamps'][i] - BF['data']['raw_timestamps'][i-1])
    BF['data']['raw_timestamp_deltas'] = array(BF['data']['raw_timestamp_deltas'])

    BF['good_timestamps_to_raw_timestamps_indicies__dic'] = {}
    BF['img_dic'] = {}
    BF['img_dic']['left'] = {}
    BF['img_dic']['right'] = {}


    if False:
        for f in BF['bag_files']:
            bag_file_img_dic = load_obj(f)
            for s in ['left','right']:
                for ts in bag_file_img_dic[s].keys():
                    BF['img_dic'][s][ts] = bag_file_img_dic[s][ts]
    good_timestamps_set = set(BF['left_image_bound_to_data'].keys()) # & set(BF['img_dic']['left'].keys()) # Note, won't have this info here now.
    bad_timestamps_list = []

    cprint('basic checking . . .','yellow')

    for ts in BF['data']['raw_timestamps']:
        """
        if not ts in BF['img_dic']['left']:
            bad_timestamps_list.append(ts)
            continue                
        if not BF['left_image_bound_to_data'][ts]['right_image'] in BF['img_dic']['right']:
            bad_timestamps_list.append(ts)
            continue
        L = BF['img_dic']['left'][ts]
        r_t = BF['left_image_bound_to_data'][ts]['right_image']
        R = BF['img_dic']['right'][r_t]
        #assert(type(L) == np.ndarray)
        if not type(L) == np.ndarray:
            bad_timestamps_list.append(ts)
            continue
        #assert(type(R) == np.ndarray)
        if not type(R) == np.ndarray:
            bad_timestamps_list.append(ts)
            continue
        #assert(shape(L) == (94, 168))
        if not  shape(L) == (94, 168):
            bad_timestamps_list.append(ts)
            continue
        #assert( shape(R) == (94, 168))    
        if not  shape(R) == (94, 168):
            bad_timestamps_list.append(ts)
            continue
        """
        SL = BF['left_image_bound_to_data']
        #assert('encoder' in SL[ts])
        """
        if not 'encoder' in SL[ts]:
            bad_timestamps_list.append(ts)
            cprint("if not 'encoder' in SL[ts]:")
            continue
        #assert('encoder' in SL[ts])
        if not 'gyro' in SL[ts]:
            bad_timestamps_list.append(ts)
            cprint("if not 'gyro' in SL[ts]:")
            continue
        #assert('encoder' in SL[ts])
        """
        if not 'motor' in SL[ts]:
            bad_timestamps_list.append(ts)
            cprint("if not 'motor' in SL[ts]:")
            continue
        #assert('encoder' in SL[ts])
        if not 'steer' in SL[ts]:
            bad_timestamps_list.append(ts)
            cprint("if not 'steer' in SL[ts]:")
            continue
        #assert('encoder' in SL[ts])
        if not 'state' in SL[ts]:
            bad_timestamps_list.append(ts)
            cprint("if not 'state' in SL[ts]:")
            continue
        #assert('encoder' in SL[ts])
        """
        if not type(SL[ts]['encoder']) == float:
            cprint("if not type(SL[ts]['encoder']) == float:")
            bad_timestamps_list.append(ts)
            continue
        #assert('encoder' in SL[ts])
        if not len(SL[ts]['gyro']) == 3:
            bad_timestamps_list.append(ts)
            cprint("Warning!!! if not len(SL[ts]['gyro']) == 3:")
            #continue
        if not len(SL[ts]['acc']) == 3:
            bad_timestamps_list.append(ts)
            cprint(" if not len(SL[ts]['acc']) == 3:")
            continue
        #assert('encoder' in SL[ts])
        """
        if not type(SL[ts]['motor']) == float:
            bad_timestamps_list.append(ts)
            cprint("if not type(SL[ts]['motor']) == float:")
            continue
        #assert('encoder' in SL[ts])
        if not type(SL[ts]['steer']) == float:
            bad_timestamps_list.append(ts)
            cprint("if not type(SL[ts]['steer']) == float:")
            continue
        #assert('encoder' in SL[ts])
        if not type(SL[ts]['state']) == float:
            bad_timestamps_list.append(ts)
            cprint("if not type(SL[ts]['state']) == float:")
            continue

    if len(bad_timestamps_list) > 0:
        good_timestamps_set -= set(bad_timestamps_list)
        cprint(d2s('Removed bad_timestamps:',len(bad_timestamps_list),'of',len(BF['data']['raw_timestamps']),'total.'),'red')
        #print bad_timestamps_list
    cprint('basic checking done','yellow')

    # Corrections. We need to adjust some State values that were interpolated.
    for ts in good_timestamps_set: # There i=was interpolation of values. For State we don't want this! Here we undo the problem.
        s = BF['left_image_bound_to_data'][ts]['state'] 
        BF['left_image_bound_to_data'][ts]['state'] = np.round(s)

    good_timestamps_list = sorted(list(good_timestamps_set))
    del good_timestamps_set

    cprint('basic checking done','yellow')
    for i in range(len(good_timestamps_list)-2): # Here we assume that isolated state 4 timepoints are rounding/sampling errors.
        t0 = good_timestamps_list[i]
        t1 = good_timestamps_list[i+1]
        t2 = good_timestamps_list[i+2]
        if BF['left_image_bound_to_data'][t1]['state'] == 4:
            if BF['left_image_bound_to_data'][t0]['state'] != 4:
                if BF['left_image_bound_to_data'][t2]['state'] != 4:
                        BF['left_image_bound_to_data'][t1]['state'] = BF['left_image_bound_to_data'][t0]['state']

    state_one_steps = 0
    for ts in good_timestamps_list:
        BF['left_image_bound_to_data'][ts]['state_one_steps'] = 0 # overwrite loaded values

    for i in range(len(good_timestamps_list)-2,-1,-1):
        if _is_timestamp_valid_data(BF,good_timestamps_list[i],accepted_states) and good_timestamps_list[i+1] - good_timestamps_list[i] < 0.1:
            state_one_steps += 1
        else:
            state_one_steps = 0
        BF['left_image_bound_to_data'][good_timestamps_list[i]]['state_one_steps'] = state_one_steps

    bad_timestamps = []
    for ts in good_timestamps_list:
        if BF['left_image_bound_to_data'][ts]['state_one_steps'] < NUM_STATE_ONE_STEPS:
            bad_timestamps.append(ts)


    
    BF['data']['good_start_timestamps'] = sorted(list(set(good_timestamps_list) - set(bad_timestamps)))
    BF['data']['good_start_indicies'] = []

    for gts in BF['data']['good_start_timestamps']:
        raw_index = BF['data']['raw_timestamps'].index(gts)
        BF['good_timestamps_to_raw_timestamps_indicies__dic'][gts] = raw_index
        BF['data']['good_start_indicies'].append(raw_index)


    if len(BF['data']['good_start_timestamps']) == 0:
        cprint("""Bag_Folder::__init__, WARNING!!!!, len(BF['data']['good_start_timestamps']) == 0, ***NO DATA***,"""+BF['path'],'red','on_yellow')
        BF['img_dic'] = {}
        return None

    BF['data']['state'] = _elements(BF,'state')
    BF['data']['steer'] = _elements(BF,'steer')
    BF['data']['motor'] = _elements(BF,'motor')
    
    """
    gyro = _elements(BF,'gyro')

    BF['data']['gyro_x'] = gyro[:,0]
    BF['data']['gyro_z'] = gyro[:,1]
    BF['data']['gyro_y'] = gyro[:,2]
    BF['data']['encoder'] = _elements(BF,'encoder')
    """
    BF['data']['state_one_steps'] = _elements(BF,'state_one_steps')
    """
    acc = _elements(BF,'acc')
    print acc
    BF['data']['acc_x'] = acc[:,0]
    BF['data']['acc_z'] = acc[:,1]
    BF['data']['acc_y'] = acc[:,2]
    """
    extremes = [
        #['gyro_x', -140,140],
        #['gyro_z', -140,140],
        #['gyro_y',-140,140],
        #['encoder', 0, 10],
        #['acc_x',-12,12],
        #['acc_y', -12,12],
        #['acc_z',-8,20],
        ['motor',0,99],
        ['steer',0,99]]
    for e in extremes:
        cprint(d2s("Bag_Folder::__init__", e[0],len(BF['data'][e[0]])),'blue')
        _fix_extremes(BF,e[0],e[1],e[2])

    return BF



def _is_timestamp_valid_data(BF,t,accepted_states=[1]):
    valid = True
    state = BF['left_image_bound_to_data'][t]['state']
    motor = BF['left_image_bound_to_data'][t]['motor']
    steer = BF['left_image_bound_to_data'][t]['steer']
    if state not in accepted_states: #[1]:#[1,3,5,6,7]: Disallowing caffe states altogether
        valid = False
    if motor < 53: # i.e., there must be at least a slight forward motor command 
        valid = False
    if True:
        if state in [3,5,6,7]: # Some strange things can happen when human takes control, steering gets stuck at max
            if steer > 99:
                valid = False
            elif steer < 1: # Can get stuck in steer = 0
                valid = False
    return valid
    


def _elements(BF,topic):
    data = []
    for t in BF['data']['raw_timestamps']:
        if topic in BF['left_image_bound_to_data'][t]:
            data.append(BF['left_image_bound_to_data'][t][topic])
        else:
            data.append(-999.999)
            print "Bag_Folder::elements Warning, data.append(-999.999), topic ="+topic
    return np.array(data)



def _fix_extremes(BF,topic,min_val,max_val):
    d = BF['data'][topic]
    mn = d[d<min_val]
    if len(mn)>0:
        cprint(d2s('Bag_Folder::fix_extremes, Warning: limiting',len(mn),topic,'values (i.e.,',dp((100*len(mn))/(1.0*len(d))),'%) to',min_val),'red')
        d[d<min_val] = min_val
    mx = d[d>max_val]
    if len(mx)>0:
        cprint(d2s('Bag_Folder::fix_extremes, Warning: limiting',len(mx),topic,'values (i.e.,',dp((100*len(mx))/(1.0*len(d))),'%) to',max_val),'red')
        d[d>max_val] = max_val
    #print(d2s(topic,":len=",len(d),",",len(mn),len(mx)))

