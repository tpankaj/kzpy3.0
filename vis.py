from kzpy3.utils import *

'''
e.g.
from kzpy3.vis import *; kzpy_vis_test()
'''

import matplotlib.pyplot as plt  # the Python plotting package

PP,FF = plt.rcParams,'figure.figsize'

def kzpy_vis_test():
    img_dic = get_some_images()
    ppff = PP[FF]
    PP[FF] = 3,3
    mi(img_dic['bay'],'bay')
    PP[FF] = ppff
    plt.figure('hist')
    plt.hist(np.random.randn(10000),bins=100)
    True

def mi( image_matrix, figure_num = 1, subplot_array = [1,1,1], \
        img_title = '', img_xlabel = 'x', img_ylabel = 'y', cmap = 'gray', toolBar = False ):
    """My Imagesc, displays a matrix as grayscale image

        e.g.,

            from kzpy import *
            from kzpy.img import *
            mi(np.random.rand(256,256),99,[1,1,1],'random matrix')

    """
    if toolBar == False:
        plt.rcParams['toolbar'] = 'None'
    else:
        plt.rcParams['toolbar'] = 'toolbar2'

    f = plt.figure(figure_num)

    if True:
        f.subplots_adjust(bottom=0.05)
        f.subplots_adjust(top=0.95)
        f.subplots_adjust(wspace=0.1)
        f.subplots_adjust(hspace=0.1)
        f.subplots_adjust(left=0.05)
        f.subplots_adjust(right=0.95)
    if False:
        f.subplots_adjust(bottom=0.0)
        f.subplots_adjust(top=0.95)
        f.subplots_adjust(wspace=0.0)
        f.subplots_adjust(hspace=0.1)
        f.subplots_adjust(left=0.0)
        f.subplots_adjust(right=1.0)
    f.add_subplot(subplot_array[0],subplot_array[1],subplot_array[2])
    imgplot = plt.imshow(image_matrix, cmap)
    imgplot.set_interpolation('nearest')
    plt.axis('off')
    if len(img_title) > 0:# != 'no title':
        plt.title(img_title)




def yb_color_modulation_of_grayscale_image(img,y,b,opt_lower_contrast=True):

    if len(np.shape(img))>2:
        img = np.mean(img,axis=2)
    img = z2o(img)

    if opt_lower_contrast:
        print('low contrast option')
        img = (1.0+img)/3.0

    y = z2o(y)
    b = z2o(b)

    ci = np.zeros((np.shape(img)[0],np.shape(img)[1],3))
    print(np.shape(ci))
    for i in range(3):
        ci[:,:,i] = 1.0*img
    ci = ci/np.max(ci)

    for i in range(3):
        ci[:,:,i] *= (1-y)
    for i in [0,1]:
        ci[:,:,i] += y

    for i in range(3):
        ci[:,:,i] *= (1-b)
    for i in [2]:
        ci[:,:,i] += b
        
    return ci

    
 
def get_some_images():
    '''
    Load some images that can be used for demos, etc.
    e.g., img_dic = get_some_images(); mi(img_dic['bay'])
    '''
    img_dic = {}
    img_dic['bay'] = imread(opj(home_path,'Pictures','bay2.png'))
    return img_dic

