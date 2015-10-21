from kzpy3.utils import *

def save_nii(new_data, original_img, new_name):
    """Save data as Nifti with reference header info."""
    new_img = nib.Nifti1Image(new_data, original_img.get_affine(), original_img.get_header())
    nib.save(new_img, new_name)
def spm_global(vol): 
    """This from M. Brett's pna course notebook."""
    T = np.mean(vol) / 8
    return np.mean(vol[vol > T])