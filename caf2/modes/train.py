from kzpy3.caf2.utils.data import *

info_file = 'kzpy3/caf2/tmp/__info__.py'
c = txt_file_to_list_of_strings(opjh(info_file))
for e in c: exec(e)
#unix('rm '+info_file)


to_do_str = """
if 'all_runs_dics' in CAFFE_PHASE_DATA:
    all_runs_dic_PHASE = load_obj(CAFFE_PHASE_DATA)
else: 
    all_runs_dic_PHASE = get_all_runs_dic(CAFFE_PHASE_DATA)
steer_bins_PHASE = get_steer_bins(all_runs_dic_PHASE)
"""
for phase in ['TRAIN','TEST']:
    lsr = to_do_str.replace('PHASE',phase)
    exec(lsr)

def get_caffe_input_target(steer_bins,all_runs_dic,frame_range):
    b,r,n,steer,frames_to_next_turn,rps,frame_names = get_rand_frame_data(steer_bins,all_runs_dic,frame_range)
    img_lst = []
    for f in frame_names:
        img = imread(f)/255.0-0.5
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
    return img_lst,[S,F,R]

