wd = pwd;

sequence_num = '2b'

cd(d2s({'/Volumes/30June2015_4TB_fMRI_data_drive/Desktop/Research/stimuli/Wedge_annulus/sequence2b/wedge-annulus_sequence2b_15Hz_still_lighter_grid_Fri_Jul_10_16-21-31_2015/masks'}))

masks5Hz_96by128 = zeros(96,128,1350,'uint8');
masks5Hz_768by1024 = zeros(768,1024,1350,'uint8');

j = 0;
for i = 0:3:4049
	j=j+1;
	img = imread(d2s({i '.png'}));
	img = squeeze(img(:,:,1));
	mi(img,1,[1,3,1]);
	masks5Hz_768by1024(:,:,j) = img;
	masks5Hz_96by128(:,:,j) = imresize(img,1.0/8.0);
	mi(masks5Hz_768by1024(:,:,j),1,[1,3,2],d2c({i j}));
	mi(masks5Hz_96by128(:,:,j),1,[1,3,3],d2c({i j}));
	drawnow()
end

my_save(masks5Hz_96by128,d2s({'wedge_annulus_sequence' sequence_num '_masks5Hz_96by128'}));
my_save(masks5Hz_768by1024,d2s({'wedge_annulus_sequence' sequence_num '_masks5Hz_768by1024'}));



cd(wd)