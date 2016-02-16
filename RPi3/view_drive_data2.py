
from kzpy3.vis import *

def get_run_data(run_path):
    print('get_run_data')
    _,l=dir_as_dic_and_list(run_path)
    index = []
    timestamp = []
    steer = []
    speed = []
    rps = []
    left_range = []
    right_range = []
    rand_control = []
    for m in l:
        n = m.split('_')
        p = n[0]
        index.append(int(p))
        p = n[1]
        timestamp.append(float(p))
        p = n[2].split('=')[1]
        steer.append(float(p)/100.0)
        p = n[3].split('=')[1]
        speed.append(float(p)/100.0)
        p = n[4].split('=')[1]
        rps.append(float(p)/10.0)
        p = n[5].split('=')[1]
        left_range.append(int(p))
        p = n[6].split('=')[1]
        right_range.append(int(p))
        p = n[7].split('=')[1]
        rand_control.append(int(p))
    run_data_dic = {}
    run_data_dic['run_path'] = run_path
    run_data_dic['img_lst'] = l
    run_data_dic['index'] = np.array(index)
    run_data_dic['timestamp'] = np.array(timestamp) - timestamp[0]
    run_data_dic['steer'] = np.array(steer)
    run_data_dic['speed'] = np.array(speed)
    run_data_dic['rps'] = np.array(rps)
    run_data_dic['left_range'] = np.array(left_range)
    run_data_dic['right_range'] = np.array(right_range)
    run_data_dic['rand_control'] = np.array(rand_control)
    deltas = [0]
    max_thresh = 3.0
    for i in range(1,len(run_data_dic['timestamp'])):
        d = run_data_dic['timestamp'][i]-run_data_dic['timestamp'][i-1]
        d = min(max_thresh,d)
        deltas.append(d)
    run_data_dic['timestamp_deltas'] = np.array(deltas)
    run_data_dic['frames_to_next_turn'] = frames_to_next_turn(run_data_dic,steer_thresh=0.1,max_thresh=100)
    lockout = []
    for i in range(len(run_data_dic['timestamp'])):
        d = 1
        if run_data_dic['timestamp_deltas'][i] > 0.14:
            d = 0
        if run_data_dic['rps'][i] < 0.1:
            d = 0
        lockout.append(d)
    run_data_dic['data_lockout'] = np.array(lockout)
    back_frame_range = (-5+-9,10)
    good = 0 * run_data_dic['data_lockout']
    print np.shape(run_data_dic['data_lockout'])
    for i in range(-back_frame_range[0],len(run_data_dic['timestamp'])+back_frame_range[0]):
        if run_data_dic['rand_control'][i] == 0:
            g = 1
            #print((-back_frame_range[0],len(run_data_dic['timestamp'])+back_frame_range[0]),(i+back_frame_range[0],i+back_frame_range[1]))
            for j in range(i+back_frame_range[0],i+back_frame_range[1]-1):
                if run_data_dic['data_lockout'][j] == 0:
                    g = 0
            good[i] = g
    run_data_dic['train_frames'] = good
    dsteer = 0.0 * run_data_dic['steer']
    for i in range(1,len(run_data_dic['steer'])):
        dsteer[i] = run_data_dic['steer'][i] - run_data_dic['steer'][i-1]
    run_data_dic['dsteer'] = dsteer
    return run_data_dic



def get_all_runs_dic(RPi3_data_path):
    all_runs_dic,_ = dir_as_dic_and_list(RPi3_data_path)
    for k in all_runs_dic:
        print k
        all_runs_dic[k] = get_run_data(opj(RPi3_data_path,k))
    return all_runs_dic

img_dic = {}

def imread_from_img_dic(img_dic,path,fname):
    if fname not in img_dic:
        img_dic[fname] = imread(opj(path,fname))
    return img_dic[fname]


def run_to_scaled_BW(img_dic,run_data_dic,scale_percent,mirror=False):
    mirror_str = '_mir=0'
    if mirror:
        mirror_str = '_mir=1'
    dst_path = d2n(run_data_dic['run_path'],'_scl=',scale_percent,mirror_str)
    unix(d2s('mkdir -p',dst_path))
    _,l=dir_as_dic_and_list(run_data_dic['run_path'])
    for m in l:
        n = m.split('_')
        p = int(n[2].split('=')[1])
        img = imread_from_img_dic(img_dic,run_data_dic['run_path'],m)
        img_scaled = imresize(img,scale_percent)
        img_scaled = img_scaled.mean(axis=2)
        if mirror:
            p = -p
            img_scaled = np.fliplr(img_scaled)
        n[2] = d2n('str=',p)
        f = '_'.join(n)
        f0 = f.split('_')
        f2 = f.replace('.jpg',d2n('scl=',scale_percent,mirror_str,'_.png'))
        #print(d2s(m,'to',f2))
        imsave(opj(dst_path,f2),img_scaled)

def scale_BW_mirror_all_runs(img_dic,all_runs_dic,scale_percent):
    for k in all_runs_dic:
        print k
        for mirror in [False,True]:
            print mirror
            run_to_scaled_BW(img_dic,all_runs_dic[k],scale_percent,mirror)




def frames_to_next_turn(run_data_dic,steer_thresh=0.1,max_thresh=100):
    m = 0 * run_data_dic['steer']
    len_steer = len(run_data_dic['steer'])
    for i in range(len_steer):
        ctr = i
        for j in range(i,len_steer):
            if np.abs(run_data_dic['steer'][j]) > steer_thresh:
                break
            elif run_data_dic['rps'][j] > 0:
                ctr += 1
        m[i] = min(ctr-i,max_thresh)
    return m

"""
review of runs
09Feb16_12h10m58s_scl=25_mir=1 bad for training
09Feb16_13h37m22s_scl=25_mir=0 good to 1500

09Feb16_13h40m42s_scl=25_mir=0 good to 2600
10Feb16_08h25m38s_scl=25_mir=0 delete
10Feb16_08h31m21s_scl=25_mir=0 good to 2400
10Feb16_08h56m14s_scl=25_mir=0 good to 3500
10Feb16_09h03m26s_scl=25_mir=0 problem with very high rps with wheels of ground around delete 4829 to 4876
10Feb16_09h15m53s_scl=25_mir=0 problem with very high rps with wheels of ground around delete 8185 to 8215

13Feb16_08h29m40s_scl=25_mir=0 delete
13Feb16_18h09m00s_scl=25_mir=0 too dark
13Feb16_18h17m34s_scl=25_mir=0 too dark
14Feb16_11h34m14s_scl=25_mir=0 delete
14Feb16_12h43m16s_scl=25_mir=0 delete
14Feb16_15h00m14s_scl=25_mir=0 delete
"""


def plot_run(all_runs_dic,key_index):
    global some_data
    ky = sorted(all_runs_dic.keys())[key_index]
    print ky
    some_data['current_key'] = ky
    run_data_dic = all_runs_dic[ky]
    fig = plt.figure(1,figsize=(7,2))
    plt.clf()
    plt.ion()
    plt.show()
    fig.canvas.mpl_connect('button_press_event', button_press_event)
    ts = run_data_dic['timestamp']
    fps = len(ts)/ts[-1]
    indx = 0
    ctr = 1
    while indx < len(ts):
        indx = fps*60*ctr
        plt.plot([indx,indx],[-1,3],'lightgray')
        ctr += 1
    plt.xlim([0,len(ts)])
    plt.plot(run_data_dic['steer'],'b',label='steer')
    #plt.plot(run_data_dic['dsteer'],'r',label='dsteer')
    plt.plot(2.5+run_data_dic['rand_control']/4.0,'r',label='rand_control')
    plt.plot(run_data_dic['speed'],'k',label='speed')
    plt.plot(run_data_dic['rps']/3.0,'g',label='rps/3')
    plt.plot(run_data_dic['timestamp_deltas']-0.9,'r',label='timestamp_deltas')
    plt.plot(run_data_dic['frames_to_next_turn']/100.0+2.0,'y',label='frames_to_next_turn')
    #plt.plot(run_data_dic['data_lockout']/4.0-0.5,'k',label='data_lockout')
    plt.plot(run_data_dic['train_frames']/4.0+1.5,'c',label='train_frames')
    plt.title(run_data_dic['run_path'].split('/')[-1])
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    #plt.figure(3);plt.clf();
    #plt.hist(all_runs_dic[some_data['current_key']]['timestamp_deltas'],100);
    #plot_run_timestamp_deltas(run_data_dic,max_thresh=3)



#current_key = ''
all_runs_dic = {}
some_data = {}

def animate_frames(run_data_dic,start_frame,end_frame,fig,title=''):
    for x in range(start_frame,end_frame):
        f = run_data_dic['img_lst'][x]
        r = run_data_dic['rand_control'][x]
        dlo = run_data_dic['data_lockout'][x]
        img = imread(opj(run_data_dic['run_path'],f))
        if len(np.shape(img)) > 2:
            if r > 0:
                img[:,:,1:] *= 0.5
            if dlo == 0:
                img[:,:,[0,1]] *= 0.5
        plt.figure(fig)
        plt.clf()
        mi(img,fig,img_title=title)
        plt.pause(0.0001)


def button_press_event(event):
    current_key = some_data['current_key']
    all_runs_dic = some_data['all_runs_dic']
    play_range = some_data['play_range']
    plt.figure(1)
    plt.plot([event.xdata+play_range[0],event.xdata+play_range[1]],[2,2],'k')
    run_data_dic = all_runs_dic[current_key]
    animate_frames(run_data_dic,np.int(np.floor(event.xdata))+play_range[0],np.int(np.floor(event.xdata))+play_range[1],2)

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



def get_rand_frame_data(steer_bins,all_runs_dic,frame_range=(-15,-6)):
    sbks = steer_bins.keys()
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
        frame_names.append(all_runs_dic[r]['img_lst'][i])
    if True:
        for f in frame_names:
            img = imread(opj(all_runs_dic[r]['run_path'],f))
            plt.figure(9)
            plt.clf()
            mi(img,9)
            plt.pause(0.0001)
    return (b,r,n,steer,frames_to_next_turn,rps,frame_names)



all_runs_dic = get_all_runs_dic(opjD('RPi3_data/runs'))
k = sorted(all_runs_dic.keys())
  
play_range = (0,5*15)
#i = input('Enter k index: ')

some_data['current_key'] = k[0]
some_data['all_runs_dic'] = all_runs_dic
some_data['play_range'] = play_range

#plot_run(all_runs_dic[some_data['current_key']])


"""
steer_list = []
for k in all_runs_dic:
    rd = all_runs_dic[k]
    for i in range(len(rd['train_frames'])):
        f = rd['train_frames'][i]
        if f:
            steer_list.append(rd['steer'][i])
plt.figure('steer hist')
plt.clf()
bw = 1/2.0
bins = np.arange(-1,1+2*bw,bw)-bw/2.0 # = array([-1.25, -0.75, -0.25,  0.25,  0.75,  1.25])
plt.hist(steer_list,bins);

dsteer_list = []
for k in all_runs_dic:
    rd = all_runs_dic[k]
    for i in range(len(rd['train_frames'])):
        f = rd['train_frames'][i]
        if f:
            dsteer_list.append(rd['dsteer'][i])
plt.figure('dsteer hist')
plt.clf()
bw = 1/64.0
bins = np.arange(-2,2+2*bw,bw)-bw/2.0 # = array([-1.25, -0.75, -0.25,  0.25,  0.75,  1.25])
plt.hist(dsteer_list,bins);


for b in sb['center']:
    r=b[0]
    n=b[1]
    plt.clf()
    plt.pause(0.1)
    animate_frames(all_runs_dic[r],n-14,n-5,100,d2s(r,n,all_runs_dic[r]['steer'][(n-14):n]))
    #plt.clf()
    good = raw_input('Good? ')



# choose bin
# choose random entry to get (k,i)
# for that (k,i) get list of images, get (steer, rps, frames_to_next_turn)
# [first decide if mirrored or not, then modify values]
# load images into appropriate image dictionary
"""



