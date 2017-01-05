if not(exist('nii','var'))
    nii = load_untouch_nii('/Users/davidzipser/Desktop/Data/subjects/Phantom/2015/1/17Jan2014_MB_test_Zipser_Pilot_13Nov2014/fsl/20150117_112950mbboldmb615mmAPPSNs002a001.nii.gz');
end
img = nii.img;
mi(img(:,60,:,150),1,[1,4,2])
mi(img(:,60,:,1),1,[1,4,1])
a=img(:,60,:,150)-img(:,60,:,1);
n=75;
a(:,1,n)=10+0*a(:,1,n);
mi(a,1,[1,4,3])

nn = 10;
ts = sqsing(img((108/2-nn):(108/2+nn),60,n,:))';
tss = sum(ts,2);
tss = zeroToOneRange(tss);
mp({tss,'r-'},1,[1,4,4]);

