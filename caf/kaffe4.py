from kzpy3.caf.utils import *


##########################################################
#
def backprop_diffs_to_data(model_name,layers,objective_dic,net,iter_n):
    
    objectives = []
    for l in layers:
        objectives.append(objective_dic[l])

    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2,0,1))
    transformer.set_mean('data', np.load(opj(home_path,'caffe/python/caffe/imagenet/ilsvrc_2012_mean.npy')).mean(1).mean(1)) # mean pixel
    transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB
    '''
    layer_shape=list(np.shape(net.blobs[layer].data));
    layer_shape[0] = 1
    layer_shape = tuple(layer_shape)
    if layer == "conv1/7x7_s2": # special case where net.forward changes layer shape
        layer_shape = (1,64,114,114)
    if layer == "conv2/3x3": # special case where net.forward changes layer shape
        layer_shape = (1,192,57,57)
    '''
    img_path = opj(home_path,'scratch/2015/9/24/'+model_name)#+'/'+layer.replace('/','-'))
    
    unix('mkdir -p ' + img_path)
    img_path += '/'+'-'.join(layers).replace('/','-')# 'layer' #'/'+layer.replace('/','-')


    net.blobs['data'].data[0][0,:,:] = 225*np.random.random(np.shape(net.blobs['data'].data[0][1,:,:]))
    net.blobs['data'].data[0][1,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]
    net.blobs['data'].data[0][2,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]

    pb = ProgressBar(iter_n)
    print(d2c(model_name,' '.join(layers)))
    print(d2s('\tstart =',time.ctime()))
    save_time = time.time()
    n = 0
    for i in range(iter_n):
        for layer,objective in zip(layers,objectives):
            valid = make_step2(net,end=layer,objective=objective)
            src = net.blobs['data']
            k = 3
            #src.data[0,:,:k,:]=0
            #src.data[0,:,:,:k]=0
            #src.data[0,:,-k:,:]=0
            #src.data[0,:,:,-k:]=0
            src.data[0] = 200*z2o(zscore(src.data[0],2.5))-100
            #print((src.data.max(),src.data.min()))
            vis = deprocess(net, src.data[0])
            if np.mod(i,10.0)==0:
                if home_path != cluster_home_path:
                    pb.animate(i+1)
            if not valid:
                print('make_step not valid.')
                break
            
            if home_path != cluster_home_path:
                if time.time()-save_time > 15:
                    vis = deprocess(net, src.data[0])
                    img = np.uint8(255*z2o(zscore(vis,2.5)))
                    #img = np.uint8(np.clip(vis, 0, 255))
                    imsave(opj(img_path+'.png'),img)
                    save_time = time.time()
    print(d2s('\tend =',time.ctime()))
    print((model_name,layer,n))#,labels[n]))
    vis = deprocess(net, src.data[0])
    img = np.uint8(np.clip(vis, 0, 255))
    #mi(img,opj(img_path,str(n)+'.png'))
    imsave(opj(img_path+'.png'),img)
#
##########################################################

##########################################################
#
if True:
    MODEL_NUM = 0
    model_name = model_folders[MODEL_NUM]
    net = get_net(model_name)
    print(np.shape(net.blobs['data'].data))
    
    img = imread(opjh('caffe/examples/images/cat.jpg'))
    img = img[:,:,:3]

    if model_name == 'VGG_ILSVRC_16_layers':
        net.blobs['data'].reshape(1,3,224,224)
        img = imresize(img,(224,224,3))
    else:
        net.blobs['data'].reshape(1,3,227,227)
        img = imresize(img,(227,227,3))
    print(np.shape(net.blobs['data'].data))

    net.blobs['data'].data[0,0,:,:] =img[:,:,2]
    net.blobs['data'].data[0,1,:,:] =img[:,:,1]
    net.blobs['data'].data[0,2,:,:] =img[:,:,0]

    net.forward();
    activations = {}
    for k in net.blobs.keys():
        activations[k] = net.blobs[k].data.copy()

    objective_dic = get_objective_dic(model_name,activations)

    ml = objective_dic.keys()

    if __name__ == '__main__':
        backprop_diffs_to_data(
            model_name,
            [ml[0],ml[1],ml[2],ml[3]],
            objective_dic,
            net,1000)

