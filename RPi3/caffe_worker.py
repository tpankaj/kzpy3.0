from kzpy3.caf.training.y2016.m2.from_mnist.original_with_accuracy.train import *


solver.net.copy_from(opjh('/Users/karlzipser/scratch/2016/2/16/caffe/models/from_mnist/original_with_accuracy_11px_iter_4800000.caffemodel'))
#caffe_steer = [0,0,0]
while True:
    try:
        solver.net.forward();
    except Exception, e:
        print(d2s(os.path.basename(sys.argv[0]),':',e))
    #advance(caffe_steer,solver.net.blobs['ip2'].data[0][0])
    #print '--------'
    #pprint(np.array(caffe_steer).mean())
    #time.sleep(0.333)
    try:
        steer = solver.net.blobs['ip2'].data[0][0]
        steer -= 0.5
        steer *= 100
        steer = int(steer)
        np.save(opjh('Desktop/caffe_command.npy'),steer)
        print steer
    except Exception, e:
        print(d2s(os.path.basename(sys.argv[0]),':',e))



