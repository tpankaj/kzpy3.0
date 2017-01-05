function frames = convert_pngs_to_matrix(png_path)
%function mat = convert_pngs_to_matrix(png_path)
%
	d = dir([png_path,'/*.png']);
	img = imread([png_path,'/1.png']);
	frames = zeros(length(d),size(img,1),size(img,2),'single');
	for i = 1:length(d)
		img = single(imread(d2s({png_path '/' i '.png'})));
		img = squeeze(img(:,:,1));
		%mi(img,1);drawnow;
		size(img)
		frames(i,:,:) = img;
		mi(frames(i,:,:),1,[1,1,1],d2s({i}));drawnow;
	end
end

% orientation_mask_frames = convert_pngs_to_matrix('/Users/davidzipser/Google_Drive/Data/stimuli/2015/2/5Feb2015_localizer2/localizer2_orientation_5Feb2015.736000.8698/localizer2_orientation_5Feb2015_frames_masks');

% eccentricity_mask_frames = convert_pngs_to_matrix('/Users/davidzipser/Google_Drive/Data/stimuli/2015/2/5Feb2015_localizer2/localizer2_eccentricity_5Feb2015.736000.8919/localizer2_eccentricity_5Feb2015_frames_masks');



%load('/Users/davidzipser/Google_Drive/Data/stimuli/2015/2/5Feb2015_localizer2/localizer2_orientation_5Feb2015.736000.8698/mat/localizer2_orientation_5Feb2015.frames.mat')
%load('/Users/davidzipser/Google_Drive/Data/stimuli/2015/2/5Feb2015_localizer2/localizer2_eccentricity_5Feb2015.736000.8919/mat/localizer2_eccentricity_5Feb2015.frames.mat')
% for i = 1:1500
% 	mi(frames(i,:,:,:),1,[1,2,1]);
% 	m = squeeze(eccentricity_mask_frames(i,:,:,:));%squeeze(orientation_mask_frames(i,:,:,:));
% 	m(1,1)=1;m(1,2)=0;
% 	mi(m,1,[1,2,2]);
% 	pause(1/50);
% end