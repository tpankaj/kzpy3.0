# These examples are from various files distributed with caffe

from kzpy3.utils import *
import caffe





class SimpleLayer4(caffe.Layer):
    def setup(self, bottom, top):
        global sessions_dic
        if not sessions_dic:
            print('Loading sessions_dic:')
            sessions_dic = get_sessions_dic(opjh('Desktop/RPi_data'))
        pass
    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)
    def forward(self, bottom, top):
        global target_lst
        global ctr,last_time,mask
        if np.mod(ctr,10) == 0:
            print time.time()-last_time
            last_time = time.time()
        img_lst,target_lst = get_img_lst_and_target_lst(sessions_dic)
        x1 = 0
        x2 = x1+298
        y1 = 0
        y2 = y1+224
        for i in range(9):
            top[0].data[0,i,:,:] = (img_lst[i][:,:,1]/255.0-0.5)*mask
        ctr += 1
    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 1.0 * top[0].diff # don't know what this should be, but perhaps it doesn't matter for a data layer





class SimpleLayer5(caffe.Layer):
    """"""
    
    def setup(self, bottom, top):
        pass

    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)
    
    def forward(self, bottom, top):
        global target_lst
        for i in range(len(target_lst)):
            top[0].data[0,i] = target_lst[i]


    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 1.0 * top[0].diff # don't know what this should be, but perhaps it doesn't matter for a data layer

