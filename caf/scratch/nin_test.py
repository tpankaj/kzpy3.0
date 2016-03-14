net = caffe.Classifier(
	'/Users/karlzipser/Google_Drive/models_caffe/nin_imagenet_conv_sandbox/deploy.prototxt',
	'/Users/karlzipser/Google_Drive/models_caffe/nin_imagenet_conv_sandbox/model.caffemodel',
	mean = np.float32([104.0, 116.0, 122.0]),
	channel_swap = (2,1,0))


for l in [(k, v.data.shape) for k, v in net.blobs.items()]:
    print l

transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,0,1))
transformer.set_mean('data', np.load(opj(home_path,'caffe/python/caffe/imagenet/ilsvrc_2012_mean.npy')).mean(1).mean(1)) # mean pixel
transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

net.blobs['data'].reshape(1,3,224,224)



plt.plot(net.blobs['pool4'].data[0,:,0,0])
