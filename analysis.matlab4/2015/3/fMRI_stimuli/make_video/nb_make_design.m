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
% 11 March 2015
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	% if not(exist('frames'))
	% 	load('~/Data/experiments/vermeer_attend_face_or_read_letters/vermeer1to10/frames.mat');
	% end
	if not(exist('images'))
		for i = 1:6
			images(i,:,:,:) = imread(d2s({'~/Data/stimuli/2015/2/11Feb2015_Vermeer_reading_videos/Vermeer_512/Vermeer_' i '.jpg'}));
	 	end
	 	images(7,:,:,:) = 128;
	 end
		% for i = 1:6
		% 	images(i,:,:,:) = imrotate(squeeze(images(i,:,:,:)),180);%imread(d2s({'~/Data/stimuli/2015/2/11Feb2015_Vermeer_reading_videos/Vermeer_512/Vermeer_' i '.jpg'}));
	 % 	end



	FIXATE = 		100;
	READ = 			101;
	ATTEND_FACE = 	102;
	ATTEND_VASE = 	103;
	REST = 			104;

	BLANK_FRAME = 7;
	display_acceleration = 100;
	frame_duration = 1/5/display_acceleration;
	frame_nums = 1:6;%[42 241 271 302 332 362];
	attention_tasks = [ATTEND_VASE ATTEND_FACE READ];

	display_frames_mean = 20;
	blank_frames_mean = 2*5;
	display_frames_jitter_plus_minus = 5;


	fixspot1 = zeros(4,4,3);
	fixspot1(2:3,2:3,:)=255;
	fixspot2 = zeros(4,4,3);
	fixspot2(2:3,2:3,1)=255;
	fixspot3 = zeros(4,4,3);
	fixspot3(2:3,2:3,2)=255;
	fixspot4 = zeros(4,4,3);
	fixspot4(2:3,2:3,3)=255;


	clear m;

	randperm_frame_nums = frame_nums(randperm(length(frame_nums)));
	ctr = 0;

	for i = 1:6
		ctr = ctr + 1; m{ctr} = {[randi(100) randi(100)]-50 [FIXATE] 0*(1:2) + BLANK_FRAME};
	end
	ctr = ctr + 1; m{ctr} = {[0 0] [FIXATE] 0*(1:(6*5)) + BLANK_FRAME};

	for experiment_block = 1:4
		for at = 1:length(attention_tasks)
			attention_task = attention_tasks(at);
			for i = 1:length(randperm_frame_nums)
				ctr = ctr + 1; m{ctr} = {[0 0] [FIXATE attention_task] 0*(1:display_frames_mean) + randperm_frame_nums(i)};
				num_blank_frames = blank_frames_mean + randi(2*display_frames_jitter_plus_minus+1)-1-display_frames_jitter_plus_minus;
				ctr = ctr + 1; m{ctr} = {[0 0] [FIXATE attention_task] 0*(1:num_blank_frames) + BLANK_FRAME};
			end
			ctr = ctr + 1; m{ctr} = {[0 0] [FIXATE] 0*(1:(20)) + BLANK_FRAME};
		end
		for i = 1:6
			ctr = ctr + 1; m{ctr} = {[randi(100) randi(100)]-50 [FIXATE] 0*(1:2) + BLANK_FRAME};
		end
		ctr = ctr + 1; m{ctr} = {[0 0] [FIXATE] 0*(1:(20)) + BLANK_FRAME};
		ctr = ctr + 1; m{ctr} = {[0 0] [REST] 0*(1:(20)) + BLANK_FRAME};
		ctr = ctr + 1; m{ctr} = {[0 0] [FIXATE] 0*(1:(20)) + BLANK_FRAME};
	end

	ctr = ctr + 1; m{ctr} = {[0 0] [FIXATE] 0*(1:(6*5)) + BLANK_FRAME};
	ctr = ctr + 1; m{ctr} = {[0 0] [REST] 0*(1:(20)) + BLANK_FRAME};

	frame_count = 0;



	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	video_name = '11Mar2015';
	mkdir(d2s({'~/Desktop/' video_name '.' now}));
	outputVideo = VideoWriter(d2s({'~/Desktop/' video_name '.' now '/' video_name '.' now '.avi'}),'Motion JPEG AVI');%'Uncompressed AVI');%
	outputVideo.FrameRate = 5;
	outputVideo.Quality = 99;
	open(outputVideo);
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



	for i = 1:length(m)
		i
		moment.fix.x = m{i}{1}(1);
		moment.fix.y = m{i}{1}(2);
		moment.tasks = m{i}{2};
		moment.frames = m{i}{3};
		moment
		for j = 1:length(moment.frames)
			frame = squeeze(images(moment.frames(j),:,:,:));
			frame_count = frame_count + 1;
			if ismember(FIXATE,moment.tasks)
				fixspot = fixspot1;
				if ismember(ATTEND_VASE,moment.tasks)
					fixspot = fixspot2;
				end
				if ismember(ATTEND_FACE,moment.tasks)
					fixspot = fixspot3;
				end
				if ismember(READ,moment.tasks)
					fixspot = fixspot4;
				end
				
				frame = place_img_A_in_img_B(fixspot,frame, moment.fix.x,moment.fix.y);
			end
			mi(frame,1,[1,1,1],d2c({frame_count}));
			hold on;
			text(100,100,d2s({moment.tasks}));
			hold off

			writeVideo(outputVideo,frame);
			pause(frame_duration);
		end
	end

	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	close(outputVideo);
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
