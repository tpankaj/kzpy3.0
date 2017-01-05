import scipy.io
import cortex

omat=scipy.io.loadmat('/Users/davidzipser/Desktop/pycortex_HVO_vols/ori_vol.mat')
emat=scipy.io.loadmat('/Users/davidzipser/Desktop/pycortex_HVO_vols/ecc_vol.mat')
zmat=scipy.io.loadmat('/Users/davidzipser/Desktop/pycortex_HVO_vols/zc_sum1.mat')

ecc_vol=cortex.Volume(emat['zc_sum1'],"HVO","HVO_1Mar2015")
ori_vol=cortex.Volume(omat['zc_sum1'],"HVO","HVO_1Mar2015")
zc_vol=cortex.Volume(zmat['zc_sum1'],"HVO","HVO_1Mar2015")

cortex.webshow({'zc_sum':zc_vol,'eccentricity':ecc_vol,'orientation':ori_vol})
