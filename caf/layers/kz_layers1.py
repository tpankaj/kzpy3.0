# These examples are from various files distributed with caffe

from kzpy3.utils import *
import caffe




class SimpleLayer0(caffe.Layer):
    """A layer that just multiplies by one."""

    def setup(self, bottom, top):
        pass

    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)

    def forward(self, bottom, top):
        top[0].data[...] = 1.0 * bottom[0].data

    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 1.0 * top[0].diff


class SimpleLayer1(caffe.Layer):
    """A layer that sometimes reverses contrast."""

    def setup(self, bottom, top):
        pass

    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)

    def forward(self, bottom, top):
    	r = np.random.random()
    	#print(r)
    	if r < 0.5:
        	top[0].data[...] = bottom[0].data - 0.5
        else:
        	top[0].data[...] = 1.0 - bottom[0].data - 0.5

    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 1.0 * top[0].diff # don't know what this should be, but perhaps it doesn't matter for a data layer


class SimpleLayer2(caffe.Layer):
    """A layer that adds distractors."""

    def setup(self, bottom, top):
        pass

    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)
    
    def forward(self, bottom, top):
        tp = zeros((1,1,28,28))
        n = 12
        n2 = 10
        for i in range(100):
            top[0].data[i,:,:,:] = bottom[0].data[i,:,:,:] - 0.5
            mx = top[0].data[i,:,:,:].max()
            top[0].data[i,:,:,:n] += bottom[0].data[randint(100),:,:,-n:]
            top[0].data[i,:,:,-n:] += bottom[0].data[randint(100),:,:,:n]
            top[0].data[i,:,:n2,:] += bottom[0].data[randint(100),:,-n2:,:]
            top[0].data[i,:,-n2:,:] += bottom[0].data[randint(100),:,:n2,:]
            tp = top[0].data[i,:,:,:]
            tp[tp>mx] = mx


            #top[0].data[i,:,:,:] += np.random.random(shape(bottom[0].data[r,:,:,:]))
    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 1.0 * top[0].diff # don't know what this should be, but perhaps it doesn't matter for a data layer


class SimpleLayer3(caffe.Layer):
    """A layer that addds distractcors, sometimes reverses contrast."""

    def setup(self, bottom, top):
        pass

    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)
    
    def forward(self, bottom, top):
        tp = zeros((1,1,28,28))
        n = 12
        n2 = 10
        for i in range(100):
            top[0].data[i,:,:,:] = bottom[0].data[i,:,:,:] - 0.5
            mx = top[0].data[i,:,:,:].max()
            top[0].data[i,:,:,:n] += bottom[0].data[randint(100),:,:,-n:]
            top[0].data[i,:,:,-n:] += bottom[0].data[randint(100),:,:,:n]
            top[0].data[i,:,:n2,:] += bottom[0].data[randint(100),:,-n2:,:]
            top[0].data[i,:,-n2:,:] += bottom[0].data[randint(100),:,:n2,:]
            tp = top[0].data[i,:,:,:]
            tp[tp>mx] = mx
            if np.random.random(1)[0] > 0.5:
                top[0].data[i,:,:,:] = mx-tp

            #top[0].data[i,:,:,:] += np.random.random(shape(bottom[0].data[r,:,:,:]))
    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 1.0 * top[0].diff # don't know what this should be, but perhaps it doesn't matter for a data layer

xy_offset = [0,0]
class SimpleLayer4(caffe.Layer):
    """"""

    def setup(self, bottom, top):
        pass

    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)
    
    def forward(self, bottom, top):
        #xy_offset[0] = np.random.randint(3)
        #xy_offset[1] = np.random.randint(3)
        img = imread(opjD('img.jpg'))
        x1 = xy_offset[0]
        x2 = x1+298
        y1 = xy_offset[1]
        y2 = y1+224
        #print(shape(top[0].data))
        #print(shape(img))
        top[0].data[0,0,:,:] = img[:,:,2]
        top[0].data[0,1,:,:] = img[:,:,1]
        top[0].data[0,2,:,:] = img[:,:,0]
    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 1.0 * top[0].diff # don't know what this should be, but perhaps it doesn't matter for a data layer


class SimpleLayer5(caffe.Layer):
    """"""

    def setup(self, bottom, top):
        pass

    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)
    
    def forward(self, bottom, top):
        tp = zeros((1,1,28,28))
        top[0].data[0,:] = np.random.rand(11)
        top[0].data[0,0] = xy_offset[0]
        top[0].data[0,1] = xy_offset[1]

            #top[0].data[i,:,:,:] += np.random.random(shape(bottom[0].data[r,:,:,:]))
    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 1.0 * top[0].diff # don't know what this should be, but perhaps it doesn't matter for a data layer

