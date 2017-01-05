
%nii=load_untouch_nii('/Users/davidzipser/Google_Drive/Data/subjects/Phantom/2015/3/13/nii/20150313_190659mbboldmb620mmAPPSNs004a001.nii.gz');

img = nii.img;

means = zeros(340,2);
ca;

for z = 1:60
	
	for i = 1:340
		means(i,z) = mean(mean(mean(img(:,:,z,i))));
	end
	mp({zscore(means(:,z)) + 5*z,'b-'},1,[1 1 1],d2s({z}));hold on;%([0 340 0 200]);
	%pause
end