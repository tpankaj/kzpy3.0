from kzpy3.utils import *
import os
import sys
sys.path.insert(0, './python')

import caffe
import numpy as np

caffe.set_device(0)
caffe.set_mode_gpu()
solver = caffe.SGDSolver(opjh('caffe/models/person_clothing_17Sept2015/solver.prototxt'))

niter = 500000
train_loss = []
accuracy_lst = []

def rotate_average_filters(filters):
    for i in range(len(filters)):
        f = filters[i,:,:,:].transpose((1,2,0))
        f = np.rot90(f,np.mod(i,4))
        filters[i,:,:,:] = f.transpose((2,0,1))
    for i in range(0,len(filters),4):
        f = filters[i,:,:,:]
        for j in range(1,4):
            f += filters[i+j,:,:,:]
        f /= 4.0
        for j in range(4):
            filters[i+j,:,:,:] = np.rot90(f.transpose((1,2,0)),-j).transpose((2,0,1))

def average_biases(biases):
    for i in range(0,len(biases),4):
            biases[i:(i+4)] = biases[i:(i+4)].mean()

for it in range(niter):
    try:
        solver.step(1)  # SGD by Caffe
    except:
        pass
print 'done'



