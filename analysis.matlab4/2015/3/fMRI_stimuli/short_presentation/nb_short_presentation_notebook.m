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


if 1 %%%%%%%% load Vermeer images %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
	
	v = zeros(6,384,512,3,'single');
	blank = zeros(384,512,3,'single')+0.5;
	blank_fix = blank;
	blank_fix(190:194,254:258,:)=0;
	
	for p = 1:6
	    v(p,:,:,:) = imread(d2s({'~/Desktop/Artists/Vermeer_512/Vermeer_' p '.jpg'}));
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
	the_world = zeros(1050,1050,3);
end

% img1 = center_img_A_in_img_B(display_1024_768,the_world);
% mi(img1,1);
% return

if 1 %%%%%%%% display Vermeer images %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 2;
	%fixspot = zeros(8,8,3);
	fixspot = zeros(4,4,3);
	%fixspot(3:5,3:5,:)=1;
	fixspot(2:3,2:3,:)=1;
	%tic
	for k = 1:100
		for j = 1:6
			i = randi(6);
			img1 = center_img_A_in_img_B(fixspot,display_1024_768);
			%img2 = center_img_A_in_img_B(fixspot,sqsing(v(i,:,:,:))/255);
			img2 = sqsing(v(i,:,:,:))/255;
			img1 = center_img_A_in_img_B(img1,the_world);
			img2 = center_img_A_in_img_B(img2,display_1024_768);
			img2 = center_img_A_in_img_B(img2,the_world);
			img3 = center_img_A_in_img_B(display_1024_768,the_world);


			mi(img1,1);
			delay_time = max(2,2+1*randn);
			pause(delay_time);
tic
for n = 1:1
			mi(img2,1);
			%toc
			pause(180/1000);

			% mi(img1,1);
			% delay_time = max(2,2+1*randn);
			% pause(80/1000);
end
toc


			mi(img3,1);
			%tic
			pause(1);

		end
	end
end
