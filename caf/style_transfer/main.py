from kzpy3.caf.style_transfer.stran import *

"""
python kzpy3/caf/style_transfer/main.py

"""

def build_net(model_path, net_fn, param_fn, args, data_mean=None):
    """
    Loads an imagenet classifier, building the net and transformer

    ----------
    Parameters
    ----------
    model_path : str
        Path where the model is saved
    net_fun : str
        Filename of 'deploy.prototxt' for the model, containing
        the definition of the model architecture
    param_fun : str
        Filename of parameter file, usually ends in '.caffemodel'
    scale : int
        Scale the size of the input by scale
    data_mean : array, shape (3,)
        Mean for each color (defaults to imgenet means)

    -------
    Returns
    -------
    net: caffe net
        Caffe network object
    transformer: caffe Transformer
        Transformer that takes in HWK images and puts them into the
        appropriate format for the caffe model
        see: https://github.com/BVLC/caffe/blob/master/python/caffe/io.py
    """
    # scale = args.img_scale
    caffe_root = args.caffe_root
    net_fn = os.path.join(model_path, net_fn)
    param_fn = os.path.join(model_path, param_fn)
    if data_mean is None:
        mean_path = os.path.join(caffe_root, "python", "caffe", "imagenet",
                                 "ilsvrc_2012_mean.npy")
        data_mean = np.load(mean_path).mean((1, 2))

    net = caffe.Net(net_fn, param_fn, caffe.TEST)

    _, k, h, w = net.blobs['data'].data.shape
    net.blobs['data'].reshape(1, k, h, w)  # Only one image

    # Input preprocessing
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2, 0, 1))  # HWK to KHW
    transformer.set_mean('data', data_mean)  # color channel means
    transformer.set_raw_scale('data', 255)  # Scale for network input
    transformer.set_channel_swap('data', (2, 1, 0))  # BGR instead of RGB

    return net, transformer





def fn_gen(d, ext='jpg'):
    """
    Helper method to generate filenames

    Parameters
    ----------
    d : dict
        Dictionary giving options and their values to be converted to a string
    ext : str
        Extension for filename

    Returns
    -------
    fn : str
        Filename with options
    """
    fn = ''
    for i, k in enumerate(d.keys()):
        if i > 0:
            fn += '__'
        fn += str(k) + '_' + str(d[k])
    fn = fn.replace('.', "")
    return fn + '.' + ext
    


if __name__ == '__main__':
    parser = ArgumentParser('Invert a sum of layer matching costs')
    parser.add_argument('--gpu', type=int, default=-1,
                        help="Index of gpu, gpu=-1")
    parser.add_argument('--network', type=str, default='vgg',
                        help="Name of network, vgg or bvlc_googlenet")
    parser.add_argument('--caffe_root', type=str, default='laptop',
                        help='caffe_root, if computer or cluster, do nothing')
    parser.add_argument('--n_itr', type=int, default=10000,
                        help='Number of iterations to run descent')
    parser.add_argument('--data_folder', type=str, default='data/',
                        help='Folder containing the data')
    parser.add_argument('--output_dir', type=str, default='output/',
                        help='Directory to save images')
    parser.add_argument('--content_file', type=str,
                        default='content/bridge.jpg',
                        help='Filename for content image')
    parser.add_argument('--style_file', type=str,
                        default='style/starry_night.jpg',
                        help='Filename for style image')
    parser.add_argument('--sc_ratio', type=float, default=4.,
                        help='Ratio of style weight to content weight')
    parser.add_argument('--img_scale', type=int, default=1,
                        help='Ratio to scale size of input. Try 1 or 2')
    args = parser.parse_args()

    if args.caffe_root == 'cluster':
        args.caffe_root = '/global/home/users/agan/caffe'
    elif args.caffe_root == 'laptop':
        args.caffe_root = '/Users/karlzipser/caffe'

    print 'The network is ' + args.network
    if args.network == 'vgg':
        model_folder = 'models/VGG_ILSVRC_19_layers'
        net_fn = 'deploy_headless.prototxt'
        # param_fn = 'vgg_normalised.caffemodel'
        param_fn = 'VGG_ILSVRC_19_layers.caffemodel'
    elif args.network == 'bvlc_googlenet':
        model_folder = 'models/bvlc_googlenet'
        net_fn = 'deploy.prototxt'
        param_fn = 'bvlc_googlenet.caffemodel'
    else:
        raise ValueError('Unrecognized network')
    model_path = os.path.join(args.caffe_root, model_folder)

    if args.gpu >= 0:
        caffe.set_mode_gpu()
        caffe.set_device(args.gpu)
    elif args.gpu == -1:
        caffe.set_mode_cpu()
    else:
        raise ValueError('Unrecognized gpu mode')

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    net, transformer = build_net(
        model_path, net_fn, param_fn, args)
    style_files = ['starry_night.jpg']
    '''
    style_files = ['starry_night.jpg',
                   'legos.jpg', 'scream.jpg',
                   'seated_nude.jpg', 'wave.jpg',
                   'grainstacks.jpg', 'household_object.jpg',
                   'kq_swift.jpg', 'vasily.jpg']
    '''
    style_files = [os.path.join('style', fn) for fn in style_files]
    sc_ratios = [args.sc_ratio]

    options = list(itertools.product(style_files, sc_ratios))
    for style_file, sc_ratio in options:
        args.style_file = style_file
        args.sc_ratio = sc_ratio
        st = StyleTransfer(net, transformer, args)
        x, _ = st.lbfgs_cost_optimizer()
        fn = fn_gen({'content': args.content_file.replace('.jpg', ''),
                     'ratio_x100': int(args.sc_ratio * 100),
                     'style': args.style_file.replace('.jpg', '')})
        st.save_image(x, fn)
