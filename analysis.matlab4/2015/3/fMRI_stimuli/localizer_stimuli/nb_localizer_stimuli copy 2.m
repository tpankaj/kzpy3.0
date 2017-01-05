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
% Description . . .
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if not(exist('teststim'))
    load('~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/stimuli-stimTrn/colorstimuli.mat');
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CELL_NUM = 1;
    stimX = 512;
    stimY = 512;
    stimXcenter = stimX/2;
    stimYcenter = stimY/2;
    fixspot_width = 2;
    mask = zeros(48,stimX,stimY,'single')+1;
    %v = [X Y];
    ctr = 0;
    K = 0.53645/2;
    for theta = 0:15:359
        min_half_wid = min(stimXcenter,stimYcenter);
        r1 = min_half_wid*theta/360;
        r0 = 0.9*r1-10;
        r2 = 1.1*r1+10;
        ctr = ctr + 1;

        R = [cosd(theta) -sind(theta); sind(theta) cosd(theta)];
        for x = 1:stimX
            for y = 1:stimY
                X = x-stimXcenter;
                Y = y-stimYcenter;
                v=[X Y];
                vR = v*R;
                X=vR(1);Y=vR(2);
                if Y < 0
                        if abs(X/Y) < K
                            mask(ctr,x,y) = 0;
                        end
                end
                xysq = X^2+Y^2;
                if xysq < 5^2
                    mask(ctr,x,y) = 0;
                    mask(ctr+24,x,y) = 0;
                end
                if and(xysq > (r0)^2, xysq < (r2)^2)
                    mask(ctr+24,x,y) = 0;
                end
            end
        end
    end
    %mi(mask(ctr,:,:,:),1);
    %theta
    %      my_pause
    %     my_imwrite(squeeze(mask(ctr,:,:)),d2s({'mask_' theta}));
    %end
    %mi(sum(mask,1),2);
    frame = zeros(stimX,stimY,3,'single') + 0.5;
    frame((stimXcenter-fixspot_width/2):(stimXcenter+fixspot_width/2),(stimYcenter-fixspot_width/2):(stimYcenter+fixspot_width/2),:) = 1;
end



if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CELL_NUM = 2;
    
    
outputVideo = VideoWriter(d2s({'~/Desktop/localizer1_1Feb2015.avi'}),'Uncompressed AVI');%'Motion JPEG AVI');%
outputVideo.FrameRate = 6.667;
open(outputVideo);

    
    
    
    
    p = 0.15;
    t = 0;
    m = 1;
    img512 = zeros(512,512,3,'single')+0.5;
    people_imgs = G.semantic_sets_stimTrn('set-images_with_people');
    animal_imgs = G.semantic_sets_stimTrn('set-animals');
    %people_imgs = unique([G.semantic_sets_stimTrn('set-people_full_face_frontal_SMALL')',G.semantic_sets_stimTrn('set-people_full_face_frontal_MEDIUM')',G.semantic_sets_stimTrn('set-people_full_face_frontal_LARGE')']);
    place_imgs = setdiff(G.semantic_sets_stimTrn('set-scene_with_ground_plane_and_sky'),people_imgs);
    place_imgs = setdiff(place_imgs,animal_imgs);
    clock
    for i = 1:1000
        if iseven(m)
            %'people'
            img_num = people_imgs(randi(length(people_imgs)));
        else
            %'place'
            img_num = place_imgs(randi(length(place_imgs)));
        end
        %img = get_Kay_image('Trn',img_num);
        img = img512;
        img(6:505,6:505,1) = sqsing(trainstim(:,:,1,img_num))/255;
        img(6:505,6:505,2) = sqsing(trainstim(:,:,2,img_num))/255;
        img(6:505,6:505,3) = sqsing(trainstim(:,:,3,img_num))/255;
        t = t + p;
        if t > 4
            img = 0*img+0.5;
            %img(1,1)=1;img(1,2)=-1;
        end
        stimulus = merge_images(img,frame,squeeze(mask(m,:,:)));
        stimulus_BarryLyndon_crop = uint8(255*stimulus(96:415,1:512,:));
        mi(stimulus_BarryLyndon_crop,69)
        
%for ii = 1:10
    writeVideo(outputVideo,stimulus_BarryLyndon_crop);
%end
        pause(p/1.3);
        if t > 6
            %toc
            t = 0;
            m = m + 1;
            m
            if m>48
                clock
                return
            end
            %tic
        end
    end
    
close(outputVideo);
end %%%%%%%%
