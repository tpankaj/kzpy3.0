from kzpy3.vis import *
from kzpy3.progress import *


CS = [] # - Comment String
def CS_(comment,section='',print_latest=True):
    str = '# - '
    if len(section) > 0:
        str = str + section + ': '
    str = str + comment
    CS.append(str)
    if print_latest:
        print(CS[-1])


def load_subject(subject,kay_data_path):
    mat = scipy.io.loadmat(opj(kay_data_subject_path,subject+'aux.mat'))
    roi = mat['roi'+subject]
    voxIdx = mat['voxIdx'+subject]
    snr = mat['snr'+subject]
    snr[np.isfinite(snr)==0] = 0

    mat = scipy.io.loadmat(opj(kay_data_subject_path,subject+'data.mat'))
    dataTrn = mat['dataTrn'+subject]
    dataVal = mat['dataVal'+subject]

    data = np.concatenate((dataTrn, dataVal),axis=1)

    # - Some voxels have nan's. This is because of the way voxels are aligned across sessions.
    # So we need to identify the finite ones.
    good_voxels = good_voxel_identify(data)

    return roi,voxIdx,snr,data,good_voxels


def load_grayscale_photos_512(kay_data_path):
    mat = scipy.io.loadmat(opj(kay_data_path,'photos','grayscale','stimTrn512_int8.mat'))
    stimTrn = mat['stimTrn512_int8']
    mat = scipy.io.loadmat(opj(kay_data_path,'photos','grayscale','stimVal512_uint8.mat'))
    stimVal = mat['stimVal512_uint8']
    return np.concatenate((stimTrn, stimVal),axis=0)


def load_texture_energy_512(kay_data_path):
    mat = scipy.io.loadmat(opj(kay_data_path,'photos','texture_energy','stimTrnHP_SD6.mat'))
    stimTrnHP_SD6 = mat['stimTrnHP_SD6']
    mat = scipy.io.loadmat(opj(kay_data_path,'photos','texture_energy','stimValHP_SD6.mat'))
    stimValHP_SD6 = mat['stimValHP_SD6']
    hp512 = np.concatenate((stimTrnHP_SD6, stimValHP_SD6),axis=0)
    return hp512


def hp512_to_hp128(hp512):
    pb = ProgressBar(np.shape(hp512)[0])
    hp128 = np.zeros((np.shape(hp512)[0],128,128))
    for i in range(np.shape(hp512)[0]):
        hp128[i,:,:] = scipy.misc.imresize(hp512[i,:,:],[128,128])
        pb.animate(i+1)
    return hp128


def load_texture_energy_128(kay_data_path):
    mat = scipy.io.loadmat(opj(kay_data_path,'photos','texture_energy','hp128.mat'))
    hp128 = mat['hp128']
    return hp128


def get_correlation_RF(data,voxel_num,hp128,use_images):
    voxel_responses = data[voxel_num,use_images]
    correlation_RF = np.zeros((128,128))
    for x in range(128):
        for y in range(128):
            pixel_values = hp128[use_images,x,y]
            correlation_RF[x,y] = np.corrcoef(voxel_responses,pixel_values)[0,1]
    correlation_RF[np.isfinite(correlation_RF)==0] = 0
    return correlation_RF


def mask_surround(img,r=60):
    c = np.size(img[0]) / 2.0
    for x in range(np.shape(img)[0]):
        for y in range(np.shape(img)[0]):
            if np.sqrt((x-c)**2+(y-c)**2) > r:
                img[x,y] = 0

                
                
                
# - I make different sets of images so that I can map RFs with different holdout images
def get_use_image_sets(subject,kay_data_path):
    use_image_sets = {}
    for ex in range(0,1750,120):
        images = range(1750+120)
        exclude = (ex,ex+120)
        if exclude[1] > 1680:
            exclude = (exclude[0],1750)
        #print exclude
        exclude_images = range(exclude[0],exclude[1])
        use_images = list(images)
        for e in exclude_images:
            use_images.remove(e)
        use_image_sets[(exclude[0],exclude[1])] = use_images
    use_image_sets[1750,1870] = range(0,1750)

    print sorted(use_image_sets.keys())

    for e in sorted(use_image_sets.keys()):
        s = 'mkdir -p ' + opj(kay_data_path,'subject-'+subject,'rfs/exclude_'+str(e[0])+'.'+str(e[1]))
        print s
    # - Look at use_image_sets to see how they skip images
    plt.plot(use_image_sets[(0,120)])
    plt.plot(use_image_sets[(960,1080)])
    plt.plot(use_image_sets[(1750,1870)])
    return use_image_sets


                
                
mask = np.zeros((128,128))+1.0
mask_surround(mask)


def map_correlation_RFs(correlation_RFs, data,hp128,use_rois,use_images):
    pb = ProgressBar(np.shape(data)[0])
    for i in range(np.shape(data)[0]):
        if roi[i] in use_rois:
            correlation_RFs[i] = mask * get_correlation_RF(data,i,hp128,use_images)
            showarray(correlation_RFs[i])
            pb.animate(i+1)
            clear_output(wait=True)
            
            
def get_contiguity_proportion(img,sd,GRAPHICS = False):
    
    if sd > 0:
        blurred_img = scipy.ndimage.gaussian_filter(img, sigma=sd)
    else:
        blurred_img = img
        
    peak = np.unravel_index(blurred_img.argmax(),blurred_img.shape)
    peak_correlation = blurred_img[peak]
    
    thresh_img = blurred_img.copy()
    #thresh_img -= thresh_img.min()
    #thresh_img /= thresh_img.max()
    #thresh_img *= thresh_img

    mx = thresh_img.max()
    
    thresh_img[thresh_img<0.666*mx]=0
    thresh_img[thresh_img>0]=1

    s = [[1,1,1],
             [1,1,1],
             [1,1,1]]

    labels, numLabels = scipy.ndimage.label(thresh_img,structure=s)

    peak_label = labels[peak[0],peak[1]]
    contig = labels.copy()
    contig[contig !=peak_label] = 0
    contig[contig ==peak_label] = 1

    contiguity_proportion = contig.sum()/float(thresh_img.sum())
    
    if GRAPHICS:
        temp = blurred_img.copy()
        temp[(peak[0]-1):(peak[0]+1),(peak[1]-1):(peak[1]+1)] = 0
        print(peak)
        print(peak_correlation)
        mi(img,1,[2,3,1],'original')
        mi(blurred_img,1,[2,3,2],'blurred')
        mi(temp,1,[2,3,3],'blurred, peak marked')
        mi(thresh_img,1,[2,3,4],'threshold')
        mi(labels,1,[2,3,5],img_title=str(peak_label))
        mi(contig,1,[2,3,6],img_title=('contig'))
        print(contiguity_proportion)
        
    normalized_rf = contig * (blurred_img-0.666*peak_correlation)
    normalized_rf /= np.sum(np.sum(1.0*normalized_rf))
    
    return contiguity_proportion,peak,peak_correlation,normalized_rf
                
                
def good_voxel_identify(data):
    n_voxels = np.shape(data)[0]
    good_voxels = np.zeros(n_voxels) + 1
    for i in range(n_voxels):
        if np.isnan(data[i,:]).any():
            good_voxels[i] = 0
    return good_voxels


def binarize_rf_img(img,thresh=0):
    b = 0.0*img
    b[img>thresh] = 1.0
    b[img<=thresh] = 0
    return b


def sum_and_coverage_info(use_rois,roi,selected_normalized_rfs,GRAPHICS = False):
    sum_of_normalized_rfs = np.zeros((128,128))
    coverage_of_normalized_rfs = np.zeros((128,128))
    for i in selected_normalized_rfs.keys():
        if roi[i] in use_rois:
            sum_of_normalized_rfs += selected_normalized_rfs[i]
            coverage_of_normalized_rfs += binarize_rf_img(selected_normalized_rfs[i])
    coverage_of_five = binarize_rf_img(coverage_of_normalized_rfs,5-0.1)
    if GRAPHICS:
        mi(sum_of_normalized_rfs,1,[1,3,1],img_title='sum_of_normalized_rfs')
        mi(coverage_of_normalized_rfs,1,[1,3,2],img_title='coverage_of_normalized_rfs')
        mi(coverage_of_five,1,[1,3,3],img_title='coverage')
    return sum_of_normalized_rfs,coverage_of_normalized_rfs,coverage_of_five



def make_p_image(stim_num,data,use_rois,roi,selected_normalized_rfs,sum_of_normalized_rfs):
    p = np.zeros((128,128))
    for i in selected_normalized_rfs.keys():
        if roi[i] in use_rois:
            p += selected_normalized_rfs[i] * data[i,stim_num]
    p /= sum_of_normalized_rfs
    return p


def z_score_model_voxel(m):
    z = m - np.mean(m)
    z /= np.std(m)
    z1 = 1.0*z
    sdn = 2.18
    z1[z1<-sdn] = -sdn
    z1 += sdn+0.00001
    z1 /= 2.0*sdn
    z2 = np.log(z1)
    z3 = z2 - np.mean(z2)
    z3 /= np.std(z2)
    return z3





# - Get rf stats
def get_rf_stats(correlation_rfs,good_voxels):
    normalized_rfs = {}
    contiguity_proportions = {}
    peak_correlations = {}
    peak_xys = {}
    pb = ProgressBar(len(correlation_rfs.keys()))
    ctr = 0
    for v in correlation_rfs.keys():
        if good_voxels[v]:
            crf = mask*correlation_rfs[v]
            contiguity_proportion,peak,peak_correlation,normalized_rf = get_contiguity_proportion(crf,0,GRAPHICS = False)
            # - sd=0 means no blurring
            contiguity_proportions[v] = contiguity_proportion
            peak_correlations[v] = peak_correlation
            peak_xys[v] = peak
            normalized_rfs[v] = normalized_rf
            pb.animate(ctr+1)
            ctr += 1
    return normalized_rfs,contiguity_proportions,peak_correlations,peak_xys




# - Find selected voxels
def find_selected_voxels(peak_correlations,roi,good_voxels,contiguity_proportions):
    pc = []
    cp = []
    bad = []
    selected_voxels = {}
    pc_thresh = 0.1
    cp_thresh = 0.7
    for i in peak_correlations.keys():
        if good_voxels[i] == 1:
            if roi[i] in [1,2]:
                if np.isfinite(peak_correlations[i]):
                    pc.append(peak_correlations[i])
                    cp.append(contiguity_proportions[i])
                    if peak_correlations[i] >= pc_thresh:
                        if contiguity_proportions[i] >= cp_thresh:
                            selected_voxels[i] = True
                else:
                    bad.append(i)
    ppff = PP[FF]
    PP[FF] = 7,7
    plt.scatter(pc,cp)
    plt.figure()
    print(len(selected_voxels))
    PP[FF]=7,2
    plt.hist(cp,bins=100);
    plt.figure()
    plt.hist(pc,bins=100);
    PP[FF] = ppff
    return selected_voxels

def yb_color_modulation_of_grayscale_image(img,y,b,opt_lower_contrast=True):

    if len(np.shape(img))>2:
        img = np.mean(img,axis=2)
        
    if np.std(img) > 0:
        img = z2o(img)

    if opt_lower_contrast:
        #print('low contrast option')
        img = (1.0+img)/3.0

    y = z2o(y)
    b = z2o(b)

    ci = np.zeros((np.shape(img)[0],np.shape(img)[1],3))
    
    for i in range(3):
        ci[:,:,i] = 1.0*img
    #ci = ci/np.max(ci) # might want to use this.

    for i in range(3):
        ci[:,:,i] *= (1-y)
    for i in [0,1]:
        ci[:,:,i] += y

    for i in range(3):
        ci[:,:,i] *= (1-b)
    for i in [2]:
        ci[:,:,i] += b
        
    return ci
