"""Example of loading and displaying a .nii.gz file"""
from kzpy3.vis import *

import nibabel as nib

def coronal(vol,z_start,rows,columns,fig=2):
    #pylab.rcParams['figure.figsize'] = big_figure_size
    """Show a brain in horizontal slices"""
    r,c = rows,columns
    num_slices = r * c
    for z in range(z_start,z_start+num_slices):
        mi(np.rot90(vol[:,z,:]),fig,[r,c,z-z_start+1],str(z))


nii=nib.load('/Users/karlzipser/Data/subjects/HVO/2015/3/29/fsl/mc_to_006a_of_9Feb2015/20150329_102756mbboldmb620mmAPPSNs004a001.feat/mean_func.nii.gz')

volume = nii.get_data()

coronal(volume,9,7,7)
plt.ion()
plt.show()
