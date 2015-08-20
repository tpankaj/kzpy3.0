from kzpy3.vis import *
from kzpy3.progress import *
plt.ion()

from cStringIO import StringIO
import scipy.ndimage as nd
import PIL.Image
from IPython.display import clear_output, Image, display
from google.protobuf import text_format
import caffe

# caffe.set_mode_gpu()
# caffe.set_device(0) # select GPU device if multiple devices exist

def showarray(a, fmt='jpeg'):
    a = np.uint8(np.clip(a, 0, 255))
    f = StringIO()
    PIL.Image.fromarray(a).save(f, fmt)
    display(Image(data=f.getvalue()))

model_folders = ['bvlc_googlenet','googlenet_places205','bvlc_reference_caffenet']

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


imagenet_labels_filename = opj(home_path,'caffe/data/ilsvrc12/synset_words.txt')
try:
    labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')
except:
    get_ipython().system(u'../data/ilsvrc12/get_ilsvrc_aux.sh')
    labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')



def objective_L2(dst):
    dst.diff[:] = dst.data 

def make_step(net, step_size=1.5, end='inception_4c/output', 
              jitter=32, clip=True, objective=objective_L2):
    '''Basic gradient ascent step.'''

    src = net.blobs['data'] # input image is stored in Net's 'data' blob
    dst = net.blobs[end]

    ox, oy = np.random.randint(-jitter, jitter+1, 2)
    src.data[0] = np.roll(np.roll(src.data[0], ox, -1), oy, -2) # apply jitter shift
            
    net.forward(end=end)
    objective(dst)  # specify the optimization objective
    net.backward(start=end)
    g = src.diff[0]
    # apply normalized ascent step to the input image
    src.data[:] += step_size/np.abs(g).mean() * g

    src.data[0] = np.roll(np.roll(src.data[0], -ox, -1), -oy, -2) # unshift image
            
    if clip:
        bias = net.transformer.mean['data']
        src.data[:] = np.clip(src.data, -bias, 255-bias)    


def do_it(num_nodes,layer):
    img_path = opj(home_path,'scratch/2015/8/19/bvlc_reference_caffenet/'+layer)
    unix('mkdir -p ' + img_path)
    for n in range(1):#(num_nodes):
        mask7 = np.zeros((1,num_nodes))
        #n = np.random.randint(1000)
        mask7[:,n] = 1.0
        def objective_kz7(dst):
            dst.diff[:] = dst.data * mask7
        net.blobs['data'].data[0][0,:,:] = 225*np.random.random(np.shape(net.blobs['data'].data[0][1,:,:]))
        net.blobs['data'].data[0][1,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]
        net.blobs['data'].data[0][2,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]

        i_max = 100
        pb = ProgressBar(i_max)
        for i in range(i_max):
            make_step(net,end=layer,objective=objective_kz7)
            src = net.blobs['data']
            #vis = deprocess(net, src.data[0])
            pb.animate(i+1)
        print((model_folders[MODEL_NUM],n))#,labels[n]))
        vis = deprocess(net, src.data[0])
        img = np.uint8(np.clip(vis, 0, 255))
        #mi(img,opj(img_path,str(n)+'.png'))
        imsave(opj(img_path,str(n)+'.png'),img)

def do_it2(layer,net,iter_n):
    layer_shape=list(np.shape(net.blobs[layer].data));
    layer_shape[0] = 1
    layer_shape = tuple(layer_shape)
    img_path = opj(home_path,'scratch/2015/8/18/bvlc_reference_caffenet/'+layer)
    unix('mkdir -p ' + img_path)
    for n in range(layer_shape[1]):#(num_nodes):
        mask7 = np.zeros(layer_shape)
        #n = np.random.randint(1000)
        mask7[:,n] = 1.0
        def objective_kz7(dst):
            dst.diff[:] = dst.data * mask7
        net.blobs['data'].data[0][0,:,:] = 225*np.random.random(np.shape(net.blobs['data'].data[0][1,:,:]))
        net.blobs['data'].data[0][1,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]
        net.blobs['data'].data[0][2,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]

        pb = ProgressBar(iter_n)
        for i in range(iter_n):
            make_step(net,end=layer,objective=objective_kz7)
            src = net.blobs['data']
            #vis = deprocess(net, src.data[0])
            pb.animate(i+1)
        print((model_folders[MODEL_NUM],n))#,labels[n]))
        vis = deprocess(net, src.data[0])
        img = np.uint8(np.clip(vis, 0, 255))
        #mi(img,opj(img_path,str(n)+'.png'))
        imsave(opj(img_path,str(n)+'.png'),img)

def do_it3(layer,net,iter_n):

    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2,0,1))
    transformer.set_mean('data', np.load(opj(home_path,'caffe/python/caffe/imagenet/ilsvrc_2012_mean.npy')).mean(1).mean(1)) # mean pixel
    transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

    layer_shape=list(np.shape(net.blobs[layer].data));
    layer_shape[0] = 1
    layer_shape = tuple(layer_shape)
    img_path = opj(home_path,'scratch/2015/8/18/bvlc_reference_caffenet/'+layer)
    unix('mkdir -p ' + img_path)
    for n in range(layer_shape[1]):#(num_nodes):
        mask7 = np.zeros(layer_shape)
        #n = np.random.randint(1000)
        mask7[:,n] = 1.0
        def objective_kz7(dst):
            dst.diff[:] = dst.data * mask7

        try:
            cimg = caffe.io.load_image(opj(img_path,str(n)+'.png'))
            net.blobs['data'].reshape(1,3,227,227)
            net.blobs['data'].data[...] = transformer.preprocess('data', cimg)
        except:
            net.blobs['data'].data[0][0,:,:] = 225*np.random.random(np.shape(net.blobs['data'].data[0][1,:,:]))
            net.blobs['data'].data[0][1,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]
            net.blobs['data'].data[0][2,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]

        #pb = ProgressBar(iter_n)
        for i in range(iter_n):
            make_step(net,end=layer,objective=objective_kz7)
            src = net.blobs['data']
            #vis = deprocess(net, src.data[0])
            #pb.animate(i+1)
        print((model_folders[MODEL_NUM],layer,n))#,labels[n]))
        vis = deprocess(net, src.data[0])
        img = np.uint8(np.clip(vis, 0, 255))
        #mi(img,opj(img_path,str(n)+'.png'))
        imsave(opj(img_path,str(n)+'.png'),img)

def do_it4(layer,net,iter_n):

    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2,0,1))
    transformer.set_mean('data', np.load(opj(home_path,'caffe/python/caffe/imagenet/ilsvrc_2012_mean.npy')).mean(1).mean(1)) # mean pixel
    transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

    layer_shape=list(np.shape(net.blobs[layer].data));
    layer_shape[0] = 1
    layer_shape = tuple(layer_shape)
    img_path = opj(home_path,'scratch/2015/8/19/bvlc_reference_caffenet/'+layer)
    unix('mkdir -p ' + img_path)
    for n in range(5):#layer_shape[1]):#(num_nodes):
        mask7 = np.zeros(layer_shape)
        #n = np.random.randint(1000)
        xy = np.int(layer_shape[2]/2)
        mask7[0,n,xy,xy] = 1.0
        def objective_kz7(dst):
            dst.diff[:] = dst.data * mask7

        try:
            cimg = caffe.io.load_image(opj(img_path,str(n)+'.png'))
            net.blobs['data'].reshape(1,3,227,227)
            net.blobs['data'].data[...] = transformer.preprocess('data', cimg)
        except:
            net.blobs['data'].data[0][0,:,:] = 255*np.random.random(np.shape(net.blobs['data'].data[0][1,:,:]))
            net.blobs['data'].data[0][1,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]
            net.blobs['data'].data[0][2,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]

        #pb = ProgressBar(iter_n)
        for i in range(iter_n):
            make_step(net,end=layer,objective=objective_kz7)
            src = net.blobs['data']
            #vis = deprocess(net, src.data[0])
            #pb.animate(i+1)
        print((model_folders[MODEL_NUM],layer,n))#,labels[n]))
        vis = deprocess(net, src.data[0])
        img = np.uint8(np.clip(vis, 0, 255))
        #mi(img,opj(img_path,str(n)+'.png'))
        imsave(opj(img_path,str(n)+'.png'),img)



#############################

MODEL_NUM = 2
net = get_net(MODEL_NUM)

print(np.shape(net.blobs['data'].data))
src = net.blobs['data']
src.reshape(1,3,227,227)
print(np.shape(net.blobs['data'].data))

for l in ['conv1','conv2','conv3','conv4','conv5']:
    do_it4(l,net,100)
#do_it3('conv3',net,100)


