from kzpy3.vis import *

def load_subject(subject,kay_data_path):

    mat = scipy.io.loadmat(opj(kay_data_path,subject+'aux.mat'))
    mat.keys()
    roi = mat['roi'+subject]
    voxIdx = mat['voxIdx'+subject]
    snr = mat['snr'+subject]
    snr[np.isfinite(snr)==0] = 0

    mat = scipy.io.loadmat(opj(kay_data_path,subject+'data_trn_singletrial.mat'))
    dataTrn = mat['dataTrnSingle'+subject]

	mat = scipy.io.loadmat(opj(kay_data_path,subject+'data_val_singletrial.mat'))
	dataVal = mat['dataValSingle'+subject][:,:120]

	# note, I want the average trial data, not the single
	# contatenat dataTrn and dataVal into data
	data = np.concatenate((dataTrn, dataVal),axis=1)

    return roi,voxIdx,snr,data

def load_grayscale_photos_512(kay_data_path):
	pass

def load_texture_energy_512(kay_data_path):
	pass


def get_correlation_RF(data,voxel_num,texture_energy_images,exclude_images):
	pass

