"""



"""

from kzpy3.vis import *
if '/Users/' in home_path:
    from kzpy3.misc.OSX_free_memory import OSX_free_memory





click_ts = []
def button_press_event(event):
    global click_ts
    #print len(click_ts)
    ts = event.xdata
    click_ts.append(ts)
    print click_ts[-2:]

def z2o_plot(x,y,y_offset,plt_str='.',label='no label'):
    return plt.plot(x,z2o(y)+y_offset,plt_str,label=label)



class Bag_Folder:
    def __init__(self, path):
        self.path = path
        self.files = sorted(glob.glob(opj(path,'.preprocessed','*.bag.pkl')))
        file_path = opj(path,'.preprocessed','left_image_bound_to_data.pkl')
        #print file_path
        if len(gg(file_path)) == 0:
            file_path = opj(path,'.preprocessed','left_image_bound_to_data2.pkl')
        print "Bag_Folder: loading "+file_path
        self.left_image_bound_to_data = load_obj(file_path)
        self.img_dic = {}
        self.timestamps = sorted(self.left_image_bound_to_data.keys())
        for t in self.timestamps:
            s = self.left_image_bound_to_data[t]['state'] # There is interpolation of values. For state we don't want this!
            self.left_image_bound_to_data[t]['state'] = np.round(s) # Here we undo the problem.

        for i in range(len(self.timestamps)-2): # Here we assume that isolated state 4 timepoints are rounding/sampling errors.
            t0 = self.timestamps[i]
            t1 = self.timestamps[i+1]
            t2 = self.timestamps[i+2]
            if self.left_image_bound_to_data[t1]['state'] == 4:
                if self.left_image_bound_to_data[t0]['state'] != 4:
                    if self.left_image_bound_to_data[t2]['state'] != 4:
                            self.left_image_bound_to_data[t1]['state'] = self.left_image_bound_to_data[t0]['state']

        state_one_steps = 0
        for i in range(len(self.timestamps)-2,-1,-1):
            self.left_image_bound_to_data[self.timestamps[i]]['state_one_steps'] = 0 # overwrite loaded values
            if self.is_timestamp_valid_data(self.timestamps[i]) and self.timestamps[i+1] - self.timestamps[i] < 0.3:
                state_one_steps += 1
            else:
                state_one_steps = 0
            self.left_image_bound_to_data[self.timestamps[i]]['state_one_steps'] = state_one_steps
        self.data = {}
        self.data['timestamps'] = np.array(self.timestamps)
        self.data['state'] = self.elements('state')
        self.data['steer'] = self.elements('steer')
        self.data['motor'] = self.elements('motor')
        acc = self.elements('acc')
        self.data['acc_x'] = acc[:,0]
        self.data['acc_z'] = acc[:,1]
        self.data['acc_y'] = acc[:,2]
        gyro = self.elements('gyro')
        self.data['gyro_x'] = gyro[:,0]
        self.data['gyro_z'] = gyro[:,1]
        self.data['gyro_y'] = gyro[:,2]
        self.data['encoder'] = self.elements('encoder')
        self.data['state_one_steps'] = self.elements('state_one_steps')


    def load_all_bag_files(self):
        for f in self.files:
            bag_file_img_dic = load_obj(f)
            for t in bag_file_img_dic['left'].keys():
                self.img_dic[t] = bag_file_img_dic['left'][t]

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
        
    ######################### GRAPHICS #############################################
    #
    def plot_L_file(self,fig_num=1,by_index=False):
        plt.rcParams['toolbar'] = 'toolbar2'
        steer=self.elements('steer')
        motor=self.elements('motor')
        encoder=self.elements('encoder')
        gyro=self.elements('gyro')   
        #ts,acc=elements(L,'acc') 
        state=self.elements('state')
        ts = self.timestamps
        
        ts_filtered,state_filtered = self.filtered_elements('state')
        _,motor_filtered = self.filtered_elements('motor')
        _,steer_filtered = self.filtered_elements('steer')
        _,gyro_filtered = self.filtered_elements('gyro')
        _,encoder_filtered = self.filtered_elements('encoder')
 
        if by_index:
            ts = range(len(ts))
            ts_filtered = range(len(ts_filtered))
        
        plt.plot(ts,motor,'0.7')
        plt.plot(ts,np.array(gyro)/10.,'0.7')
        #plt.plot(ts,np.array(acc)-10.,'0.7')
        plt.plot(ts,encoder,'0.7')
        plt.plot(ts,state,'0.7')
        plt.plot(ts,steer,'0.7')
        plt.plot(ts_filtered,state_filtered,'.')
        plt.plot(ts_filtered,steer_filtered,'.')

    def plot_click_L_file(self,fig_num=1,by_index=False):
        fig = plt.figure(fig_num,figsize=(14,4))
        plt.rcParams['toolbar'] = 'toolbar2'
        plt.clf()
        plt.ion()
        plt.show()
        fig.canvas.mpl_connect('button_press_event', button_press_event)
        self.plot_L_file(1,by_index)

    def elements(self,topic):
        data = []
        for t in self.timestamps:
            data.append(self.left_image_bound_to_data[t][topic])
        return np.array(data)

    def filtered_elements(self,topic):
        other = self.elements(topic)
        filtered = []
        ts_filtered = []
        for i in range(len(other)):
            if self.is_timestamp_valid_data(self.timestamps[i]):
               filtered.append(other[i])
               ts_filtered.append(self.timestamps[i]) 
        return ts_filtered,np.array(filtered)


    def play(self,start_t,stop_t,use_cv2=False,step=1):
        import cv2
        cv2.namedWindow('left',1)
        ts = sorted( self.img_dic.keys())
        print len(ts)
        img = np.zeros((94, 168,3),np.uint8)
        for i in range(0,len(ts),step):
            if ts[i] >= start_t and ts[i] < stop_t:
                if ts[i] in self.left_image_bound_to_data:
                    print ts[i],self.left_image_bound_to_data[ts[i]]['state']

                    im = self.img_dic[ts[i]].copy()
                    img[:,:,0] = im
                    img[:,:,1] = im
                    img[:,:,2] = im
                    #img = self.img_dic[ts[i]].copy()
                    steer_rect_color = [255,0,0]
                    #apply_rect_to_img(img,self.left_image_bound_to_data[ts[i]]['steer'],0,99,steer_rect_color,steer_rect_color,0.9,0.1,center=True,reverse=True)
                    apply_rect_to_img(img,self.left_image_bound_to_data[ts[i]]['acc'][0],-50,50,steer_rect_color,steer_rect_color,0.1,0.1,center=True,reverse=False)
                    apply_rect_to_img(img,self.left_image_bound_to_data[ts[i]]['acc'][1],-50,50,steer_rect_color,steer_rect_color,0.2,0.1,center=True,reverse=False)
                    apply_rect_to_img(img,self.left_image_bound_to_data[ts[i]]['acc'][2],-50,50,steer_rect_color,steer_rect_color,0.3,0.1,center=True,reverse=False)
                    #apply_rect_to_img(img,self.left_image_bound_to_data[ts[i]]['gyro'][0],-50,50,steer_rect_color,steer_rect_color,0.2,0.1,center=True,reverse=False)
                    m = max(0,self.left_image_bound_to_data[ts[i]]['motor']-49)
                    #apply_rect_to_img(img,m,0,49,steer_rect_color,steer_rect_color,0.1,0.1,center=False,reverse=False)
                    if use_cv2: # cv2 is fast, but slows if matplotlib figure is open.
                        cv2.imshow('left',img.astype('uint8'))
                        if cv2.waitKey(1) & 0xFF == ord('q'):   
                            return      
                    #t0 = time.time()   
                    else:
                        mi(self.img_dic[ts[i]],2,img_title=str(ts[i]))
                    plt.pause(0.033)#max(0.03 - time.time()-t0,0))
                else:
                    print "no data"        
        if use_cv2:
            cv2.destroyWindow('left')
    #
    ######################################################################
    





"""


class Bair_Car_Data:
    """ """
    def __init__(self, path):
        self.bag_folders_dic = {}        
        bag_folder_paths = sorted(glob.glob(opj(path,'*')))
        bag_folder_paths_dic = {}
        for b in bag_folder_paths:
            bag_folder_paths_dic[b] = True

        temp = []
        for b in bag_folder_paths_dic.keys():
            if bag_folder_paths_dic[b]:
                temp.append(b)
        bag_folder_paths = temp
        self.bag_folders_weighted = []
        for f in bag_folder_paths:
            n = len(gg(opj(f,'.preprocessed','*.bag.pkl')))
            m = len(gg(opj(f,'.preprocessed','left*')))
            print (n,m,f)
            if n > 0 and m > 0:
                self.bag_folders_dic[f] = Bag_Folder(f)
                for i in range(max(n/10,1)):
                    self.bag_folders_weighted.append(f)


    def check_memory(self):
        free_propotion = 1.0
        free_gigabytes = 999999.0
        if '/Users/' not in home_path: # OSX doesn't have the memory() function that linux has.
            m=memory()
            #print m['free']/(1.0*m['total'])
            #while m['free']/(1.0*m['total']) < 0.15:
            free_propotion = m['free']/(1.0*m['total'])
            #print free_propotion
        else:
            free_gigabytes = OSX_free_memory()
        if free_propotion < 0.15 or free_gigabytes < 3.0:
            b = random.choice(self.bag_folders_dic.keys())
            self.bag_folders_dic[b].bag_files_dic = {}
            #print "Deleting "+b+" bag files."
            #del self.bag_folders_dic[b]

    def get_data(self, target_topics, num_data_steps, num_frames):
        #print 'Bair_Car_Data::get_data'
        self.check_memory()
        if True:#try:
            if self.bag_folder == None:
                b = random.choice(self.bag_folders_weighted)
                if b not in self.bag_folders_dic:
                    self.bag_folders_dic[b] = Bag_Folder(b)
                    print d2s("len(self.bag_folders_dic) =",len(self.bag_folders_dic))
                self.bag_folder = self.bag_folders_dic[b]
                self.bag_folder.reset()

            data = self.bag_folder.get_data(target_topics, num_data_steps, num_frames)
        else: #except Exception, e:
            #print e 
            #print "Bair_Car_Data ***************************************"
            data = None

        if data == None:
            self.bag_folder = None
            return self.get_data(target_topics, num_data_steps, num_frames)
        return data
"""