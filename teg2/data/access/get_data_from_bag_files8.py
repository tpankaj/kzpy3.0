
from kzpy3.vis import *


class Bag_Folder:
    def __init__(self, path, NUM_STATE_ONE_STEPS=15):
        self.path = path
        cprint('Bag_Folder::__init__, path = '+path,'yellow','on_red')
        self.files = sorted(glob.glob(opj(path,'.preprocessed','*.bag.pkl')))
        left_path = opj(path,'.preprocessed','left_image_bound_to_data2.pkl')
        if len(gg(left_path)) == 0:
            left_path = opj(path,'.preprocessed','left_image_bound_to_data.pkl')
        self.left_image_bound_to_data = load_obj(left_path)
        self.img_dic = {}
        self.img_dic['left'] = {}
        self.img_dic['right'] = {}
        self.incremental_index = 0
        for f in self.files:
            bag_file_img_dic = load_obj(f)
            for s in ['left','right']:
                for ts in bag_file_img_dic[s].keys():
                    self.img_dic[s][ts] = bag_file_img_dic[s][ts]
        good_timestamps_set = set(self.left_image_bound_to_data.keys()) & set(self.img_dic['left'].keys())
        bad_timestamps_list = []
        cprint('basic checking . . .','yellow')
        for ts in good_timestamps_set:
            if not self.left_image_bound_to_data[ts]['right_image'] in self.img_dic['right']:
                bad_timestamps_list.append(ts)
                continue
            L = self.img_dic['left'][ts]
            r_t = self.left_image_bound_to_data[ts]['right_image']
            R = self.img_dic['right'][r_t]
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
            SL = self.left_image_bound_to_data
            #assert('encoder' in SL[ts])
            if not 'encoder' in SL[ts]:
                bad_timestamps_list.append(ts)
                continue
            #assert('encoder' in SL[ts])
            if not 'gyro' in SL[ts]:
                bad_timestamps_list.append(ts)
                continue
            #assert('encoder' in SL[ts])
            if not 'motor' in SL[ts]:
                bad_timestamps_list.append(ts)
                continue
            #assert('encoder' in SL[ts])
            if not 'steer' in SL[ts]:
                bad_timestamps_list.append(ts)
                continue
            #assert('encoder' in SL[ts])
            if not 'state' in SL[ts]:
                bad_timestamps_list.append(ts)
                continue
            #assert('encoder' in SL[ts])
            if not type(SL[ts]['encoder']) == float:
                bad_timestamps_list.append(ts)
                continue
            #assert('encoder' in SL[ts])
            if not len(SL[ts]['gyro']) == 3:
                bad_timestamps_list.append(ts)
                continue
            #assert('encoder' in SL[ts])
            if not type(SL[ts]['motor']) == float:
                bad_timestamps_list.append(ts)
                continue
            #assert('encoder' in SL[ts])
            if not type(SL[ts]['steer']) == float:
                bad_timestamps_list.append(ts)
                continue
            #assert('encoder' in SL[ts])
            if not type(SL[ts]['state']) == float:
                bad_timestamps_list.append(ts)
                continue
            if 'acc' in SL[ts]:
                #assert(len(SL[ts]['acc']) == 3)
                if not len(SL[ts]['acc']) == 3:
                    bad_timestamps_list.append(ts)    
                    continue
            else:
                SL[ts]['acc'] = [0.,0.,0.]

        if len(bad_timestamps_list) > 0:
            for bt in bad_timestamps_list:
                good_timestamps_set.remove(bt)
            cprint(d2s('Removed bad_timestamps:',len(bad_timestamps_list),'of',len(good_timestamps_set),'total.'),'red')
            #print bad_timestamps_list
        cprint('basic checking done','yellow')

        # Corrections. We need to adjust some State values that were interpolated.
        for ts in good_timestamps_set: # There i=was interpolation of values. For State we don't want this! Here we undo the problem.
            s = self.left_image_bound_to_data[ts]['state'] 
            self.left_image_bound_to_data[ts]['state'] = np.round(s)

        good_timestamps_list = sorted(list(good_timestamps_set))
        del good_timestamps_set

        for i in range(len(good_timestamps_list)-2): # Here we assume that isolated state 4 timepoints are rounding/sampling errors.
            t0 = good_timestamps_list[i]
            t1 = good_timestamps_list[i+1]
            t2 = good_timestamps_list[i+2]
            if self.left_image_bound_to_data[t1]['state'] == 4:
                if self.left_image_bound_to_data[t0]['state'] != 4:
                    if self.left_image_bound_to_data[t2]['state'] != 4:
                            self.left_image_bound_to_data[t1]['state'] = self.left_image_bound_to_data[t0]['state']

        state_one_steps = 0
        for i in range(len(good_timestamps_list)-2,-1,-1):
            self.left_image_bound_to_data[good_timestamps_list[i]]['state_one_steps'] = 0 # overwrite loaded values
            if self.is_timestamp_valid_data(good_timestamps_list[i]) and good_timestamps_list[i+1] - good_timestamps_list[i] < 0.3:
                state_one_steps += 1
            else:
                state_one_steps = 0
            self.left_image_bound_to_data[good_timestamps_list[i]]['state_one_steps'] = state_one_steps

        bad_timestamps = []
        for ts in good_timestamps_list:
            if self.left_image_bound_to_data[ts]['state_one_steps'] < NUM_STATE_ONE_STEPS:
                bad_timestamps.append(ts)

        self.data = {}
        self.data['good_start_timestamps'] = sorted(list(set(good_timestamps_list) - set(bad_timestamps)))

        if len(self.data['good_start_timestamps']) == 0:
            cprint("""WARNING!!!!, len(self.data['good_start_timestamps']) == 0, ***NO DATA***,"""+self.path,'red','on_yellow')
            self.img_dic = {}
            return None

        self.data['state'] = self.elements('state')
        self.data['steer'] = self.elements('steer')
        self.data['motor'] = self.elements('motor')
        
        gyro = self.elements('gyro')

        self.data['gyro_x'] = gyro[:,0]
        self.data['gyro_z'] = gyro[:,1]
        self.data['gyro_y'] = gyro[:,2]
        self.data['encoder'] = self.elements('encoder')
        self.data['state_one_steps'] = self.elements('state_one_steps')

        acc = self.elements('acc')
        self.data['acc_x'] = acc[:,0]
        self.data['acc_z'] = acc[:,1]
        self.data['acc_y'] = acc[:,2]

        extremes = [['gyro_x', -140,140],
            ['gyro_z', -140,140],
            ['gyro_y',-140,140],
            ['encoder', 0, 10],
            ['acc_x',-12,12],
            ['acc_y', -12,12],
            ['acc_z',-8,20],
            ['motor',0,99],
            ['steer',0,99]]
        for e in extremes:
            cprint(d2s("Bag_Folder::__init__", e[0],len(self.data[e[0]])),'blue')
            self.fix_extremes(e[0],e[1],e[2])




    def is_timestamp_valid_data(self,t):
        valid = True
        state = self.left_image_bound_to_data[t]['state']
        motor = self.left_image_bound_to_data[t]['motor']
        steer = self.left_image_bound_to_data[t]['steer']
        if state not in [1,3,5,6,7]:
            valid = False
        if motor < 51: # i.e., there must be at least a slight forward motor command 
            valid = False    
        if state in [3,5,6,7]: # Some strange things can happen when human takes control, steering gets stuck at max
            if steer > 99:
                valid = False
            elif steer < 1: # Can get stuck in steer = 0
                valid = False
        return valid
        
    def elements(self,topic):
        data = []
        for t in self.data['good_start_timestamps']:
            if topic in self.left_image_bound_to_data[t]:
                data.append(self.left_image_bound_to_data[t][topic])
            else:
                print 'def elements(self,topic)::returning nothing'
                return []
        return np.array(data)


    def fix_extremes(self,topic,min_val,max_val):
        d = self.data[topic]
        mn = d[d<min_val]
        if len(mn)>0:
            cprint(d2s('Bag_Folder::fix_extremes, Warning: limiting',len(mn),topic,'values (i.e.,',(100*len(mn))/(1.0*len(d)),'%) to',min_val),'red')
            d[d<min_val] = min_val
        mx = d[d>max_val]
        if len(mx)>0:
            cprint(d2s('Bag_Folder::fix_extremes, Warning: limiting',len(mx),topic,'values (i.e.,',(100*len(mx))/(1.0*len(d)),'%) to',max_val),'red')
            d[d>max_val] = max_val
        #print(d2s(topic,":len=",len(d),",",len(mn),len(mx)))

    def get_data(self,topics=['steer','motor'],num_topic_steps=10,num_image_steps=2,randomized=False):
        if self.incremental_index >= len(self.data['good_start_timestamps']):
            return 'end_of_bag_folder_reached'
        start_index = self.incremental_index
        data_dic = {}
        data_dic['path'] = self.path
        data_dic['timestamp'] = self.data['good_start_timestamps'][start_index]
        data_dic['state'] = self.data['state'][start_index]
        for tp in topics:
            data_dic[tp] = self.data[tp][start_index:(start_index+num_topic_steps)]

        data_dic['left'] = []
        data_dic['right'] = []    
        for n in range(num_image_steps):
            t = self.data['good_start_timestamps'][start_index+n]
            data_dic['left'].append(self.img_dic['left'][t])
            t_ = self.left_image_bound_to_data[t]['right_image']
            data_dic['right'].append(self.img_dic['right'][t_])

        # assert that data_dic holds what it is supposed to hold.
        for tp in topics:
            assert type(data_dic[tp]) == np.ndarray
            assert len(data_dic[tp]) == num_topic_steps
        for s in ['left','right']:
            assert type(data_dic[s]) == list
            assert len(data_dic[s]) == num_image_steps
            for i in range(num_image_steps):
                assert type(data_dic[s][i]) == np.ndarray
                assert shape(data_dic[s][i]) == (94, 168)
        self.incremental_index
        return data_dic


def get_data_sequence(BF):
    caffe_steer_color_color = [255,0,0]
    human_steer_color_color = [0,0,255]
    for i in range(1000):
        d = BF.get_data()
        img = np.zeros((shape(d['right'][0])[0],shape(d['right'][0])[1],3),'uint8')
        img[:,:,0] = d['right'][0].copy()
        img[:,:,1] = d['right'][0].copy()
        img[:,:,2] = d['right'][0].copy()
        BF.incremental_index += 1
        if np.int(d['state']) in [3,6]: #caffe is steering
            steer_rect_color = caffe_steer_color_color
        else:
            steer_rect_color = human_steer_color_color
        apply_rect_to_img(img,d['steer'][0],0,99,steer_rect_color,steer_rect_color,0.9,0.1,center=True,reverse=True)
        mi(img)
        plt.pause(0.00001)
