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
% Making face-attention sequences
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CELL_NUM = 2;

video_name = 'face_attention1_10Feb2015';
mkdir(d2s({'~/Desktop/' video_name '.' now}));
outputVideo = VideoWriter(d2s({'~/Desktop/' video_name '.' now '/' video_name '.' now '.avi'}),'Uncompressed AVI');%'Motion JPEG AVI');%
outputVideo.FrameRate = 5;
open(outputVideo);

    stimX = 512;
    stimY = 512;
    stimXcenter = stimX/2;
    stimYcenter = stimY/2;
    fixspot_width = 2;
    %frame_counter = 0;

    img512 = zeros(512,512,3,'single')+0.5;
    
    stim_list = [];

    BLANK = 1;
    SCENE1 = 2;
    SCENE2 = 3;
    
    stimuli(BLANK).img = img512;
    stimuli(BLANK).y_attend = 0;
    stimuli(BLANK).x_attend = 0;
    
    stimuli(SCENE1).img = zeroToOneRange(  sqsing(stimTrn512_int8(1,:,:)) );;
    stimuli(SCENE1).y_attend = 347;
    stimuli(SCENE1).x_attend = 213;
    
    stimuli(SCENE2).img = zeroToOneRange(  sqsing(stimTrn512_int8(1469,:,:)) );;
    stimuli(SCENE2).y_attend = 144;
    stimuli(SCENE2).x_attend = 424;
    
    s_min = 2;
    s_max = length(stimuli);
    s = s_min-1;
    for j = 0:5
        if and(j>0,j<5)
            s = s + 1;
            if s > s_max
                s = s_min;
            end
        end
        for i = 1:(6*outputVideo.FrameRate)
            
            if or(j==0,j==5)
                stimulus = stimuli(BLANK).img;
            else
                if or(i < 11,i>4*outputVideo.FrameRate)
                    stimulus = stimuli(BLANK).img;
                    if i < 2
                        g = zeroToOneRange( gaussian_matrix2(stimX,40,stimuli(s).x_attend-stimX/2,stimuli(s).y_attend-stimX/2));
                        for c = 1:3
                            stimulus(:,:,c) = stimulus(:,:,c) + g/20;

                        end
                    end
                else
                    stimulus = stimuli(s).img;
                end
            end


                stimulus((stimXcenter-2*fixspot_width):(stimXcenter+2*fixspot_width),(stimYcenter-2*fixspot_width):(stimYcenter+2*fixspot_width),:) = 0;
                stimulus((stimXcenter-fixspot_width/2):(stimXcenter+fixspot_width/2),(stimYcenter-fixspot_width/2):(stimYcenter+fixspot_width/2),:) = 1;


                stimulus_crop = uint8(255*stimulus(64:447,1:512,:));
                mi(stimulus_crop,69,[1,1,1],d2c({j i}));

                drawnow;
                pause(1/outputVideo.FrameRate/100);%d my_pause

                frame_counter = frame_counter + 1;
                stim_list(frame_counter,:) = [m mask_num frame_counter category (frame_counter-1)*1/outputVideo.FrameRate img_num];
                my_imwrite(stimulus_crop, d2s({frame_counter}),d2s({video_name '_frames'})); 
                writeVideo(outputVideo,stimulus_crop);
        end
    end    

%my_save(rand_perm_masks,[video_name '_randperm']);
my_save(stim_list,[video_name '_stim_list']);
close(outputVideo);
end %%%%%%%%
