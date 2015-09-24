from kzpy3.caf.utils import *


def objective_L2(dst):
    dst.diff[:] = dst.data 

  
def make_step2(
    net,
    step_size=1.5,
    end='inception_4c/output', 
    jitter=2,
    clip=True,
    objective=objective_L2):
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
    denom = np.abs(g).mean()
    if denom:
        src.data[:] += step_size/denom * g
    else:
        print(d2s('Warnging: denom =',denom))
        return False

    src.data[0] = np.roll(np.roll(src.data[0], -ox, -1), -oy, -2) # unshift image
            
    if clip:
        bias = net.transformer.mean['data']
        src.data[:] = np.clip(src.data, -bias, 255-bias)
    return True  





def do_it6(MODEL_NUM,layer,net,iter_n,mask7,start=0):

    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2,0,1))
    transformer.set_mean('data', np.load(opj(home_path,'caffe/python/caffe/imagenet/ilsvrc_2012_mean.npy')).mean(1).mean(1)) # mean pixel
    transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

    layer_shape=list(np.shape(net.blobs[layer].data));
    layer_shape[0] = 1
    layer_shape = tuple(layer_shape)
    if layer == "conv1/7x7_s2": # special case where net.forward changes layer shape
        layer_shape = (1,64,114,114)
    if layer == "conv2/3x3": # special case where net.forward changes layer shape
        layer_shape = (1,192,57,57)

    img_path = opj(home_path,'scratch/2015/9/24/'+model_folders[MODEL_NUM])#+'/'+layer.replace('/','-'))
    
    unix('mkdir -p ' + img_path)
    img_path += '/'+layer.replace('/','-')

    def objective_kz7(dst):
        dst.diff[:] = mask7

    net.blobs['data'].data[0][0,:,:] = 225*np.random.random(np.shape(net.blobs['data'].data[0][1,:,:]))
    net.blobs['data'].data[0][1,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]
    net.blobs['data'].data[0][2,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]

    pb = ProgressBar(iter_n)
    print(d2c(model_folders[MODEL_NUM],layer))
    print(d2s('\tstart =',time.ctime()))
    save_time = time.time()
    n = 0
    for i in range(iter_n):
        valid = make_step2(net,end=layer,objective=objective_kz7)
        src = net.blobs['data']
        #vis = deprocess(net, src.data[0])
        if np.mod(i,10.0)==0:
            if home_path != cluster_home_path:
                pb.animate(i+1)
        if not valid:
            print('make_step not valid.')
            break
        
        if home_path != cluster_home_path:
            if time.time()-save_time > 15:
                vis = deprocess(net, src.data[0])
                img = np.uint8(np.clip(vis, 0, 255))
                imsave(opj(img_path+'.png'),img)
                save_time = time.time()
    print(d2s('\tend =',time.ctime()))
    print((model_folders[MODEL_NUM],layer,n))#,labels[n]))
    vis = deprocess(net, src.data[0])
    img = np.uint8(np.clip(vis, 0, 255))
    #mi(img,opj(img_path,str(n)+'.png'))
    imsave(opj(img_path+'.png'),img)

'''
def do_it7(model_name,net,layers,objectives):

    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2,0,1))
    transformer.set_mean('data', np.load(opj(home_path,'caffe/python/caffe/imagenet/ilsvrc_2012_mean.npy')).mean(1).mean(1)) # mean pixel
    transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

    layer_shape=list(np.shape(net.blobs[layer].data));
    layer_shape[0] = 1
    layer_shape = tuple(layer_shape)
    if layer == "conv1/7x7_s2": # special case where net.forward changes layer shape
        layer_shape = (1,64,114,114)
    if layer == "conv2/3x3": # special case where net.forward changes layer shape
        layer_shape = (1,192,57,57)

    img_path = opj(home_path,'scratch/2015/9/24/'+model_folders[MODEL_NUM]+'/'+layer.replace('/','-'))
    
    unix('mkdir -p ' + img_path)

    def objective_kz7(dst):
        dst.diff[:] = mask7

    net.blobs['data'].data[0][0,:,:] = 225*np.random.random(np.shape(net.blobs['data'].data[0][1,:,:]))
    net.blobs['data'].data[0][1,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]
    net.blobs['data'].data[0][2,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]

    pb = ProgressBar(iter_n)
    print(d2c(model_folders[MODEL_NUM],layer))
    print(d2s('\tstart =',time.ctime()))
    save_time = time.time()
    n = 0
    for i in range(iter_n):
        valid = make_step2(net,end=layer,objective=objective_kz7)
        src = net.blobs['data']
        #vis = deprocess(net, src.data[0])
        if np.mod(i,10.0)==0:
            if home_path != cluster_home_path:
                pb.animate(i+1)
        if not valid:
            print('make_step not valid.')
            break
        
        if home_path != cluster_home_path:
            if time.time()-save_time > 15:
                vis = deprocess(net, src.data[0])
                img = np.uint8(np.clip(vis, 0, 255))
                imsave(opj(img_path,str(n)+'.png'),img)
                save_time = time.time()
    print(d2s('\tend =',time.ctime()))
    print((model_folders[MODEL_NUM],layer,n))#,labels[n]))
    vis = deprocess(net, src.data[0])
    img = np.uint8(np.clip(vis, 0, 255))
    #mi(img,opj(img_path,str(n)+'.png'))
    imsave(opj(img_path,str(n)+'.png'),img)
'''
#############################

if True:
    MODEL_NUM = 1
    net = get_net(MODEL_NUM)
    print(np.shape(net.blobs['data'].data))
    src = net.blobs['data']
    if model_folders[MODEL_NUM] == 'VGG_ILSVRC_16_layers':
        src.reshape(1,3,224,224)
    else:
        src.reshape(1,3,227,227)
    print(np.shape(net.blobs['data'].data))
    
    img = imread(opjh('caffe/examples/images/cat.jpg'))
    img = img[:,:,:3]
    img = imresize(img,(227,227,3))

    net.blobs['data'].data[0,0,:,:] =img[:,:,2]
    net.blobs['data'].data[0,1,:,:] =img[:,:,1]
    net.blobs['data'].data[0,2,:,:] =img[:,:,0]
    net.forward();
    activations = {}
    for k in net.blobs.keys():
        activations[k] = net.blobs[k].data.copy()
    lay = 'inception_5b/output' #'fc7'#'inception_4a/5x5'  #'conv1/7x7_s2'# 'conv2/3x3'# 'inception_4e/output' # 'prob' #'inception_5b/output' #  'inception_4e/output'#'prob' #'inception_3a/1x1'
    a = activations[lay]/(10.0*activations[lay].max())
    #a[0,4,45,45] = 1
    for l in [lay]:#['conv1/7x7_s2']:#inception_layers: #['fc6']:
       do_it6(MODEL_NUM,l,net,6000,a,0)

