from kzpy3.utils import *
from kzpy3.misc.progress import *

def get_WA_mask_sequence(n,Research_path):
	s_path = opj(Research_path,'stimuli/Wedge_annulus/sequence'+str(n),'KK_visit_2015_wedge_annulus_sequence'+str(n)+'_masks5Hz_96by128')
	mat = scipy.io.loadmat(s_path)
	s = mat['KK_visit_2015_wedge_annulus_sequence'+str(n)+'_masks5Hz_96by128']
	s = s[:,:,(5*6):] # NEED TO DEAL WITH DELETE FRAMES
	frame_5Hz_times = 0.2 * np.arange(0,np.shape(s)[2])
	return s,frame_5Hz_times
def get_WA_mask_sequence_ab(n,Research_path):
	s_path = opj(Research_path,'stimuli/Wedge_annulus/sequence'+str(n),'wedge_annulus_sequence'+str(n)+'_masks5Hz_96by128')
	mat = scipy.io.loadmat(s_path)
	s = mat['wedge_annulus_sequence'+str(n)+'_masks5Hz_96by128']
	s = s[:,:,(5*6):] # NEED TO DEAL WITH DELETE FRAMES
	frame_5Hz_times = 0.2 * np.arange(0,np.shape(s)[2])
	return s,frame_5Hz_times



def KK_getcanonicalhrf():
	# - KK's cannonical hrf from getcanonicalhrf.m
	KK_hrf_10Hz_str = '0;5.34e-06;3.55e-05;0.000104;0.00022;0.000388;0.00061;0.000886;0.00122;0.00159;0.00202;0.00249;0.003;0.00354;0.00411;0.00471;0.00533;0.00596;0.0066;0.00725;0.0079;0.00855;0.0092;0.00984;0.0105;0.0111;0.0117;0.0122;0.0128;0.0133;0.0138;0.0143;0.0148;0.0152;0.0156;0.016;0.0163;0.0166;0.0169;0.0171;0.0174;0.0176;0.0177;0.0179;0.018;0.0181;0.0181;0.0181;0.0182;0.0181;0.0181;0.018;0.018;0.0178;0.0177;0.0176;0.0174;0.0173;0.0171;0.0169;0.0167;0.0164;0.0162;0.0159;0.0157;0.0154;0.0151;0.0148;0.0146;0.0143;0.014;0.0136;0.0133;0.013;0.0127;0.0124;0.0121;0.0118;0.0114;0.0111;0.0108;0.0105;0.0102;0.00985;0.00954;0.00923;0.00893;0.00862;0.00832;0.00803;0.00773;0.00744;0.00716;0.00688;0.0066;0.00633;0.00607;0.00581;0.00555;0.0053;0.00505;0.00481;0.00458;0.00435;0.00412;0.0039;0.00369;0.00348;0.00328;0.00308;0.00289;0.0027;0.00252;0.00234;0.00217;0.002;0.00184;0.00168;0.00153;0.00139;0.00124;0.00111;0.000974;0.000846;0.000722;0.000603;0.000488;0.000377;0.000271;0.000168;6.96e-05;-2.51e-05;-0.000116;-0.000203;-0.000287;-0.000367;-0.000443;-0.000516;-0.000586;-0.000653;-0.000716;-0.000777;-0.000835;-0.00089;-0.000942;-0.000991;-0.00104;-0.00108;-0.00112;-0.00116;-0.0012;-0.00123;-0.00127;-0.0013;-0.00133;-0.00135;-0.00138;-0.0014;-0.00142;-0.00144;-0.00146;-0.00147;-0.00149;-0.0015;-0.00151;-0.00152;-0.00153;-0.00154;-0.00155;-0.00155;-0.00156;-0.00156;-0.00156;-0.00156;-0.00157;-0.00156;-0.00156;-0.00156;-0.00156;-0.00155;-0.00155;-0.00154;-0.00154;-0.00153;-0.00153;-0.00152;-0.00151;-0.0015;-0.00149;-0.00148;-0.00147;-0.00146;-0.00145;-0.00144;-0.00143;-0.00142;-0.00141;-0.0014;-0.00138;-0.00137;-0.00136;-0.00135;-0.00133;-0.00132;-0.00131;-0.00129;-0.00128;-0.00127;-0.00125;-0.00124;-0.00122;-0.00121;-0.0012;-0.00118;-0.00117;-0.00115;-0.00114;-0.00113;-0.00111;-0.0011;-0.00108;-0.00107;-0.00106;-0.00104;-0.00103;-0.00101;-0.001;-0.000987;-0.000973;-0.00096;-0.000947;-0.000933;-0.00092;-0.000907;-0.000894;-0.000881;-0.000868;-0.000855;-0.000843;-0.00083;-0.000818;-0.000805;-0.000793;-0.000781;-0.000769;-0.000758;-0.000746;-0.000734;-0.000723;-0.000711;-0.0007;-0.000689;-0.000678;-0.000667;-0.000657;-0.000646;-0.000636;-0.000625;-0.000615;-0.000605;-0.000595;-0.000585;-0.000576;-0.000566;-0.000557;-0.000547;-0.000538;-0.000529;-0.00052;-0.000511;-0.000503;-0.000494;-0.000486;-0.000477;-0.000469;-0.000461;-0.000453;-0.000445;-0.000438;-0.00043;-0.000422;-0.000415;-0.000408;-0.000401;-0.000393;-0.000387;-0.00038;-0.000373;-0.000366;-0.00036;-0.000353;-0.000347;-0.000341;-0.000335;-0.000329;-0.000323;-0.000317;-0.000311;-0.000305;-0.0003;-0.000294;-0.000289;-0.000284;-0.000278;-0.000273;-0.000268;-0.000263;-0.000258;-0.000254;-0.000249;-0.000244;-0.00024;-0.000235;-0.000231;-0.000226;-0.000222;-0.000218;-0.000214;-0.00021;-0.000206;-0.000202;-0.000198;-0.000194;-0.000191;-0.000187;-0.000184;-0.00018;-0.000177;-0.000173;-0.00017;-0.000167;-0.000163;-0.00016;-0.000157;-0.000154;-0.000151;-0.000148;-0.000145;-0.000143;-0.00014;-0.000137;-0.000134;-0.000132;-0.000129;-0.000127;-0.000124;-0.000122;-0.000119;-0.000117;-0.000115;-0.000113;-0.00011;-0.000108;-0.000106;-0.000104;-0.000102;-9.99e-05;-9.79e-05;-9.6e-05;-9.41e-05;-9.22e-05;-9.04e-05;-8.86e-05;-8.68e-05;-8.51e-05;-8.34e-05;-8.17e-05;-8.01e-05;-7.85e-05;-7.69e-05;-7.54e-05;-7.39e-05;-7.24e-05;-7.09e-05;-6.95e-05;-6.81e-05;-6.67e-05;-6.54e-05;-6.4e-05;-6.28e-05;-6.15e-05;-6.02e-05;-5.9e-05;-5.78e-05;-5.66e-05;-5.55e-05;-5.44e-05;-5.33e-05;-5.22e-05;-5.11e-05;-5.01e-05;-4.9e-05;-4.8e-05;-4.71e-05;-4.61e-05;-4.52e-05;-4.42e-05;-4.33e-05;-4.24e-05;-4.16e-05;-4.07e-05;-3.99e-05;-3.91e-05;-3.82e-05;-3.75e-05;-3.67e-05;-3.59e-05;-3.52e-05;-3.45e-05;-3.37e-05;-3.3e-05;-3.24e-05;-3.17e-05;-3.1e-05;-3.04e-05;-2.98e-05;-2.91e-05;-2.85e-05;-2.79e-05;-2.74e-05;-2.68e-05;-2.62e-05;-2.57e-05;-2.51e-05;-2.46e-05;-2.41e-05;-2.36e-05;-2.31e-05;-2.26e-05;-2.21e-05;-2.17e-05;-2.12e-05;-2.08e-05;-2.03e-05;-1.99e-05;-1.95e-05;-1.91e-05;-1.87e-05;-1.83e-05;-1.79e-05;-1.75e-05;-1.72e-05;-1.68e-05;-1.64e-05;-1.61e-05;-1.58e-05;-1.54e-05;-1.51e-05;-1.48e-05;-1.45e-05;-1.42e-05;-1.38e-05;-1.36e-05;-1.33e-05;-1.3e-05;-1.27e-05;-1.24e-05;-1.22e-05;-1.19e-05;-1.17e-05;-1.14e-05;-1.12e-05;-1.09e-05;-1.07e-05;-1.05e-05;-1.02e-05;-1e-05;-9.81e-06;-9.6e-06;-9.39e-06;-9.19e-06;-8.99e-06;-8.8e-06;-8.61e-06;-8.43e-06;-8.25e-06;-8.07e-06;-7.89e-06;-7.72e-06;-7.56e-06;-7.39e-06;-7.24e-06;-7.08e-06;-6.93e-06;-6.78e-06;-6.63e-06;-6.49e-06;-6.35e-06;-6.21e-06;-6.08e-06'
	KK_hrf_10Hz = []
	for n in KK_hrf_10Hz_str.split(';'):
	    KK_hrf_10Hz.append(np.float(n))
	KK_hrf_10Hztimes = np.arange(len(KK_hrf_10Hz))/10.0
	KK_hrf_5Hz = KK_hrf_10Hz[::2]
	KK_hrf_5Hztimes = np.arange(len(KK_hrf_5Hz))/5.0
	KK_hrf_10Hz = np.array(KK_hrf_10Hz)
	KK_hrf_5Hz = np.array(KK_hrf_5Hz)
	return KK_hrf_5Hz
	#ppff=PP[FF];PP[FF]=4,1
	#plt.plot(KK_hrf_10Hztimes,KK_hrf_10Hz/np.max(KK_hrf_10Hz),'.')
	#plt.plot(KK_hrf_5Hztimes,KK_hrf_5Hz/np.max(KK_hrf_5Hz),'o')
	#PP[FF]=ppff


def convolve_s_with_hrf(S,S_times,hrf,TR_times):
	X = np.shape(S)[0]
	Y = np.shape(S)[1]
	s_conv_hrf = np.zeros((X,Y,len(TR_times)))
	pb = ProgressBar(X)
	for x in range(X):
		pb.animate(x+1)
		for y in range(Y):
			s = S[x,y,:]
			hp = np.convolve(s, hrf)[:(np.shape(s)[0])]
			hp_interp = np.interp(TR_times,S_times,hp)
			s_conv_hrf[x,y,:] = hp_interp
	return s_conv_hrf


def rf_peak_xy(s_conv_hrf,a,TR_times,fig,graphics=True):
	X = np.shape(s_conv_hrf)[0]
	Y = np.shape(s_conv_hrf)[1]
	rf = np.zeros((X,Y))
	#pb = ProgressBar(X)
	for x in range(X):
		#pb.animate(x+1)
		for y in range(Y):
			rf[x,y] = np.corrcoef(s_conv_hrf[x,y],a)[0,1]
	peak = np.unravel_index(rf.argmax(), rf.shape)
	if graphics:
		PP[FF]=4,4
		plt.figure(fig+': rf')
		plt.clf()
		mi(rf,fig+': rf',[1,1,1],img_title=(peak,np.max(rf)))   
		PP[FF]=13,2
		x,y = peak
		hp_interp = s_conv_hrf[x,y,:]
		plt.figure(fig+': time course')
		plt.clf()
		plt.plot(TR_times,z21r(hp_interp),'gx')
		plt.plot(TR_times,8*z21r(a),'r')
	return rf,peak


'''
import pRF;reload(pRF); from pRF import *
hrf = KK_getcanonicalhrf()


aa2 = Research[select_keys(Research,['all_average','sequence2',':data'])[0]]

s1,frame_5Hz_times = sequence(1)
sc1 = convolve_s_with_hrf(s1,frame_5Hz_times,hrf,TR_times)
s2,frame_5Hz_times = sequence(2)
sc2 = convolve_s_with_hrf(s2,frame_5Hz_times,hrf,TR_times)


aa = np.load('/Users/karlzipser/Desktop/aa.npy')
TR_times = 0.9 * np.arange(0,np.shape(aa)[3])
r_sorted_xyz_list = np.load('/Users/karlzipser/Google_Drive/Research/data/subjects/S1_2014/2015/6/20/0/stats/mc_20150620_110252mbboldmb620mmAPPSNs003a001/r_sorted_xyz_list.npy')
gv = tuple(r_sorted_xyz_list[-1])
rf_peak_xy(s_conv_hrf,aa[gv])

s1_peaks = {}
s2_peaks = {}

for i in range(len(r_sorted_xyz_list)):
	ni = -(i+1)
	xyz = tuple(r_sorted_xyz_list[ni])
	s1_peaks[xyz] = rf_peak_xy(sc1,aa1[tuple(r_sorted_xyz_list[ni])],TR_times,'sc1',False)
	s2_peaks[xyz] = rf_peak_xy(sc2,aa2[tuple(r_sorted_xyz_list[ni])],TR_times,'sc2',False)
	print((ni,xyz,s1_peaks[xyz],s2_peaks[xyz]))
	#nothing = raw_input('paused...')



'''
True

