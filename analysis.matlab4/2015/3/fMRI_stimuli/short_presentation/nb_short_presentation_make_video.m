%%%%%%%%%%% Standard Notebook Beginning %%%%%%%%%%%%
%
clc; fprintf('%s\n',[mfilename ' (' mfilename('fullpath') '.m)']);
this_filename = mfilename('fullpath');
this_file_text = fileread([this_filename,'.m']);
if not(exist('G'))
    error('NOTE: run local_startup.m manually at the beginning of the Matlab session.');
end
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
GRAPHICS = 1;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Short presentation stimuli, 22 Feb. 2015
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


if 0 %%%%%%%% load Vermeer images %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
	
	
	blank = zeros(512,512,3,'single')+0.5;
	blank_fix = blank;
	blank_fix(254:258,254:258,:)=0;
	
	d = dir('~/Desktop/temp2/*.png');
	num_pictures = length(d);
	v = zeros(num_pictures,512,512,3,'single');
	for p = 1:num_pictures
		img = imread(d2s({'~/Desktop/temp2/' d(p).name}));
	    v(p,:,:,:) = img;
	end

	display_1024_768 = zeros(768,1024,3)+0.5;
	m = gaussian_matrix2( 1024, 250 ).^1;
	m = imresize(m,[768,1024]);
	%m = m(((1024-768)/2):(1024-(1024-768)/2-1),:);
	m = m .^1;
	m = 0.5*zeroToOneRange(m);
	display_1024_768(:,:,1) = m;
	display_1024_768(:,:,2) = m;
	display_1024_768(:,:,3) = m;

end

% img1 = center_img_A_in_img_B(display_1024_768,the_world);
% mi(img1,1);
% return

if 1 %%%%%%%% display Vermeer images %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 2;
	display_1024_768 = 0*display_1024_768+0.5;
	video_name = 'short_presentation_25Feb2015';
	mkdir(d2s({'~/Desktop/' video_name '.' now}));
	outputVideo = VideoWriter(d2s({'~/Desktop/' video_name '.' now '/' video_name '.' now '.avi'}),'Motion JPEG AVI');%'Uncompressed AVI');%
	outputVideo.FrameRate = 5;
	outputVideo.Quality = 99;
	open(outputVideo);


	num_seconds = 288;
	num_frames = num_seconds * outputVideo.FrameRate;
	f = 0;
	imgs_shown = 0;
	frame_record = [];
	delay_record = [];
	picture_order = [1:num_pictures 1:num_pictures 1:num_pictures];
	picture_order = picture_order(randperm(length(picture_order)));
	picture_order = video_details.picture_order;

	xy_ctr = 0;
	xy_record = [];
	clear video_details;

	fixspot = zeros(8,8,3);
	%fixspot = zeros(4,4,3);
	fixspot(3:6,3:6,:)=1;
	%fixspot(2:3,2:3,:)=1;

	for k = 1:10
		x = randi(400)-200;
		y = randi(400)-200;
		xy_ctr = xy_ctr + 1;
		xy_record(xy_ctr,:) = [x y];
		img1 = place_img_A_in_img_B(fixspot,display_1024_768, x,y);
		mi(img1);
		for j = 1:3
			writeVideo(outputVideo,img1);
		end
	end


	%fixspot = zeros(8,8,3);
	fixspot = zeros(4,4,3);
	%fixspot(3:5,3:5,:)=1;
	fixspot(2:3,2:3,:)=1;

	for k = 1:length(picture_order)
			
			if f > num_frames
				break;
			end
			img_num = picture_order(k);
			[k img_num]
			img1 = center_img_A_in_img_B(fixspot,display_1024_768);
	
			img2 = sqsing(v(img_num,:,:,:))/255;
			
			img2 = center_img_A_in_img_B(img2,display_1024_768);
			img2 = center_img_A_in_img_B(fixspot,img2);

			img3 = display_1024_768;

			
			
			delay_frames = max(1*outputVideo.FrameRate,1*outputVideo.FrameRate+outputVideo.FrameRate*randn);
			delay_record(k) = delay_frames;
			for j = 1:delay_frames
				f = f + 1;
				frame_record(f) = -1;
				mi(img1,1);
				writeVideo(outputVideo,img1);
			end


			for j = 1:1
				f = f + 1;
				imgs_shown = imgs_shown + 1
				mi(img2,1);
				frame_record(f) = img_num;
				writeVideo(outputVideo,img2);
			end

			

			for j = 1:(outputVideo.FrameRate*1)
				f = f + 1;
				frame_record(f) = -3;
				mi(img3,1);
				writeVideo(outputVideo,img3);
			end

	end
	fixspot = zeros(8,8,3);
	%fixspot = zeros(4,4,3);
	fixspot(3:6,3:6,:)=1;
	%fixspot(2:3,2:3,:)=1;

	for k = 1:10
		x = randi(400)-200;
		y = randi(400)-200;
		xy_ctr = xy_ctr + 1;
		xy_record(xy_ctr,:) = [x y];
		img1 = place_img_A_in_img_B(fixspot,display_1024_768, x,y);
		for j = 1:3
			mi(img1);
			writeVideo(outputVideo,img1);
		end
	end
	close(outputVideo);
	
	video_details.frame_record = frame_record;
	video_details.delay_record = delay_record;
	video_details.picture_order = picture_order;
	video_details.xy_record = xy_record;
	my_save(video_details,'video_details');
end

if 0
	ctr = 0;
	painting1 = imread('~/Desktop/rogier-van-der-weyden-descent-from-the-cross-c-14361.jpg');
	size_painting1 = size(painting1);
	for i = 1:1000
		mi(painting1,1);
		[x,y]=ginput(1);
		x1 = x-256;
		x2 = x+255;
		y1 = y-256;
		y2 = y+255;
		if x1 > 0
			if x2 <= size_painting1(2)
				if y1 > 0
					if y2 <= size_painting1(1)
						detail = painting1(y1:y2,x1:x2,:);
						size(detail)
						mi(detail,2);
						ctr = ctr + 1;
						imwrite(detail,d2s({'~/Desktop/temp2/' ctr '.png'}),'png');
					end
				end
			end
		end
	end
end
