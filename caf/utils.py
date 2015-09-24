from kzpy3.utils import *
from kzpy3.progress import *

from cStringIO import StringIO
import scipy.ndimage as nd
import PIL.Image
from IPython.display import clear_output, Image, display
from google.protobuf import text_format
import caffe

model_folders = ['bvlc_googlenet','googlenet_places205','bvlc_reference_caffenet',
'finetune_BarryLyndon_8Sept2015','VGG_ILSVRC_16_layers','person_clothing_bigger_18Sept2015',
'bvlc_googlenet_person']

cluster_home_path = '/global/home/users/karlz'
if home_path == cluster_home_path:
    caffe.set_mode_gpu()
    caffe.set_device(0) # select GPU device if multiple devices exist

def showarray(a, fmt='jpeg'):
    a = np.uint8(np.clip(a, 0, 255))
    f = StringIO()
    PIL.Image.fromarray(a).save(f, fmt)
    display(Image(data=f.getvalue()))

def get_net(MODEL_NUM = 2):
    model_folder = model_folders[MODEL_NUM]
    model_path = opj(home_path,'caffe/models',model_folder)
    net_fn   = opj(model_path,'deploy.prototxt')
    param_fn = opj(model_path,'model.caffemodel')
    # Patching model to be able to compute gradients.
    # Note that you can also manually add "force_backward: true" line to "deploy.prototxt".
    model = caffe.io.caffe_pb2.NetParameter()
    text_format.Merge(open(net_fn).read(), model)
    model.force_backward = True
    open('tmp.prototxt', 'w').write(str(model))
    net = caffe.Classifier('tmp.prototxt', param_fn,
                           mean = np.float32([104.0, 116.0, 122.0]), # ImageNet mean, training set dependent
                           channel_swap = (2,1,0)) # the reference model has channels in BGR order instead of RGB
    print model_folders[MODEL_NUM]
    for n in net.blobs.keys():
        print (np.shape(net.blobs[n].data),n)
    return net

# a couple of utility functions for converting to and from Caffe's input image layout
def preprocess(net, img):
    return np.float32(np.rollaxis(img, 2)[::-1]) - net.transformer.mean['data']
def deprocess(net, img):
    return np.dstack((img + net.transformer.mean['data'])[::-1])