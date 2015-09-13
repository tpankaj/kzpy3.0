import os
os.chdir('..')
import sys
sys.path.insert(0, './python')

import caffe
import numpy as np
###  from pylab import *
#### %matplotlib inline

# losses will also be stored in the log
caffe.set_device(0)
caffe.set_mode_gpu()
# We create a solver that fine-tunes from a previously trained network.
solver = caffe.SGDSolver('/global/home/users/karlz/scratch/models_caffe/finetune_BarryLyndon_8Sept2015/solver.prototxt')
#solver.net.copy_from('/global/home/users/karlz/scratch/models_caffe/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel')
# For reference, we also create a solver that does no finetuning.
#scratch_solver = caffe.SGDSolver('models/finetune_flickr_style/solver.prototxt')

niter = 500000
train_loss = []
accuracy_lst = []

def rotate_average_filters(filters_rot):
    for i in range(len(filters)):
        f = filters_rot[i,:,:,:].transpose((1,2,0))
        f = np.rot90(f,mod(i,4))
        filters_rot[i,:,:,:] = f.transpose((2,0,1))
    for i in range(0,len(filters),4):
        f = filters_rot[i,:,:,:]
        for j in range(1,4):
            f += filters_rot[i+j,:,:,:]
        f /= 4.0
        for j in range(4):
            filters_rot[i+j,:,:,:] = np.rot90(f.transpose((1,2,0)),j).transpose((2,0,1))


for it in range(niter):
    for k in ['conv1', 'conv2', 'conv3', 'conv4']:
        rotate_average_filters(net.params[k][0].data)
        
    solver.step(1)  # SGD by Caffe
    train_loss.append([it,solver.net.blobs['loss'].data])
    if it % 10 == 0:
        print 'iter %d, finetune_loss=%f' % (it, train_loss[it][1])
    if it % 100 == 0:    
        test_iters = 10
        accuracy = 0
        for it in np.arange(test_iters):
            solver.test_nets[0].forward()
            accuracy += solver.test_nets[0].blobs['accuracy'].data
        accuracy /= test_iters
        accuracy_lst.append([it,accuracy])
        print '*** Accuracy for fine-tuning:', accuracy          
print 'done'



