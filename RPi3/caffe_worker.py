import caffe
from kzpy3.utils import *

os.chdir(home_path) # this is for the sake of the train_val.prototxt

solver = caffe.SGDSolver(opjh("kzpy3/caf/training/y2016/m2/from_mnist/original_with_accuracy/solver_11px_scl50.prototxt"))

solver.net.copy_from(opjh('scratch/2016/2/16/caffe/models/from_mnist/original_with_accuracy_11px_scl50_steer_only/original_with_accuracy_11px_scl50_iter_1200000.caffemodel'))

while True:
    try:
        solver.net.forward();
    except Exception, e:
        print(d2s(os.path.basename(sys.argv[0]),':',e))
    try:
        steer = solver.net.blobs['ip2'].data[0][0]
        steer -= 0.5
        steer *= 100
        steer = int(steer)
        np.save(opjh('Desktop/caffe_command.npy'),steer)
        print steer
    except Exception, e:
        print(d2s(os.path.basename(sys.argv[0]),':',e))



