wd = pwd;

for sequence_num = 2

	%cd(d2s({'/Users/davidzipser/Google_Drive/Data/stimuli/2015/6/localizers/18June2015_wedge_annulus/wedge-annulus_sequence' sequence_num '_15Hz_still_lighter_grid_Fri_Jun_19_00-07-14_2015/masks'}))
	cd(d2s({'/Users/davidzipser/Google_Drive/Data/stimuli/2015/6/localizers/18June2015_wedge_annulus/wedge-annulus_sequence' sequence_num '_15Hz_still_lighter_grid_Thu_Jun_18_23-47-06_2015/masks'}))

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

	my_save(masks5Hz_96by128,d2s({'KK_visit_2015_wedge_annulus_sequence' sequence_num '_masks5Hz_96by128'}));
	my_save(masks5Hz_768by1024,d2s({'KK_visit_2015_wedge_annulus_sequence' sequence_num '_masks5Hz_768by1024'}));

	end

cd(wd)