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
% Second version of a retinotopic and categorical localizer
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if not(exist('teststim'))
    load('~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/stimuli-stimTrn/colorstimuli.mat');
end

% 300s-12 = 288s, 8s per angle yields 36 angles. 360/36 = 10

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CELL_NUM = 1;
    stimX = 512;
    stimY = 512;
    stimXcenter = stimX/2;
    stimYcenter = stimY/2;
    fixspot_width = 2;
    fix_mask_region_radius = 5;
    mask = zeros(1,stimX,stimY,'single');
    %v = [X Y];
    ctr = 0;
    K = 50;%0.53645/2 /2;\
    min_half_wid = max(stimXcenter,stimYcenter);

    for theta = 0:(360/36):359
        ctr = ctr + 1;
        R = [cosd(theta) -sind(theta); sind(theta) cosd(theta)];
        for x = 1:stimX
            for y = 1:stimY
                X = x-stimXcenter;
                Y = y-stimYcenter;
                xysq = X^2+Y^2;
                if xysq < (7+(theta/360)^2*min_half_wid*1.4142)^2
                    mask(ctr,x,y) = 1;
                    %mask(ctr+24,x,y) = 0;
                end
%                 v=[X Y];
%                 vR = v*R;
%                 X=vR(1);Y=vR(2);
%                 if Y < 0
%                         %if abs(X/Y) < K
%                 	mask(ctr,x,y) = 1;
%                         %end
%                 end
                

%                 if and(xysq > (r0)^2, xysq < (r2)^2) 
%                     mask(ctr+24,x,y) = 0;
%                 end
            end
        end
        mask(ctr,(stimXcenter-2*fixspot_width):(stimXcenter+2*fixspot_width),(stimYcenter-2*fixspot_width):(stimYcenter+2*fixspot_width),:) = 1;
        mi(mask(ctr,:,:),1,[1,1,1],d2s({ctr}));
        my_pause(0.01);
    end
    mask = 1-mask;
    me = squeeze(sum(mask,1));mi(me)
    frame = zeros(stimX,stimY,3,'single') + 0.5;
    frame((stimXcenter-2*fixspot_width):(stimXcenter+2*fixspot_width),(stimYcenter-2*fixspot_width):(stimYcenter+2*fixspot_width),:) = 0;
    frame((stimXcenter-fixspot_width/2):(stimXcenter+fixspot_width/2),(stimYcenter-fixspot_width/2):(stimYcenter+fixspot_width/2),:) = 1;
end



if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CELL_NUM = 2;

video_name = 'localizer2_A_5Feb2015';
mkdir(d2s({'~/Desktop/' video_name '.' now}));
outputVideo = VideoWriter(d2s({'~/Desktop/' video_name '.' now '/' video_name '.' now '.avi'}),'Uncompressed AVI');%'Motion JPEG AVI');%
outputVideo.FrameRate = 5;
open(outputVideo);
frame_counter = 0;

    img512 = zeros(512,512,3,'single')+0.5;
    all_people_imgs = unique([G.semantic_sets_stimTrn('set-images_with_people')',G.semantic_sets_stimTrn('set-people_maybe_missed')',G.semantic_sets_stimTrn('set-people')']);
	people_imgs = unique([G.semantic_sets_stimTrn('set-people_full_face_frontal_MEDIUM')',G.semantic_sets_stimTrn('set-people_full_face_frontal_LARGE')']);
    animal_imgs = G.semantic_sets_stimTrn('set-animals');
    place_imgs = setdiff(G.semantic_sets_stimTrn('set-scene_with_ground_plane_and_sky'),all_people_imgs);
    place_imgs = setdiff(place_imgs,animal_imgs);
    animal_faces_imgs = G.semantic_sets_stimTrn('set-animal-full-frontal-faces');
    flat_and_close_up = G.semantic_sets_stimTrn('set-flat_and_close_up');
    
    rand_perm_masks = randperm(48);
    
    stim_list = [];
	category_counter = -1;
    temp = size(mask);
    num_masks = temp(1);
    the_text = 'My name is frank. I live in the country. I like to eat fish.';
    for m = 0:(num_masks+1)
        
        rand_perm_people = randperm(length(people_imgs));
        rand_perm_place = randperm(length(place_imgs));
        rand_perm_animal = randperm(length(animal_faces_imgs));
        rand_perm_flat = randperm(length(flat_and_close_up));

        category_counter = category_counter + 1;
        if category_counter == 5
            category_counter = 1;
        end
        if or(m==0,m==num_masks+1)
            len = 30;
        else
            len = 40;
        end
        
        for i = 1:len
            category = 0;
            %i
            img = img512;
            mask_num = 1;
            img_num = 0;
                mask_invert = false;
                if and(m>0,m<(num_masks+1))
                    if i <= 20
                        mask_num = m;
                    else
                        mask_num = m;
                        mask_invert = true;
%                         mask_num = m + num_masks/2;
%                         if mask_num > num_masks
%                             mask_num = mask_num - num_masks;
%                         end
                    end
                    if or(and(1 <= i, i <= 15), and(20 < i, i < 35))
                        if category_counter == 1
                            category = 1;
                            img_num = people_imgs(rand_perm_people(i));
                        elseif category_counter == 2
                            img_num = place_imgs(rand_perm_place(i));
                            category = 2;
                        elseif category_counter == 3
                            img_num = animal_faces_imgs(rand_perm_animal(i));
                            category = 3;
                        elseif category_counter == 4
                            img_num = flat_and_close_up(rand_perm_flat(i));
                            category = 4;
                        end
                        img(6:505,6:505,1) = sqsing(trainstim(:,:,1,img_num))/255;
                        img(6:505,6:505,2) = sqsing(trainstim(:,:,2,img_num))/255;
                        img(6:505,6:505,3) = sqsing(trainstim(:,:,3,img_num))/255;
                    end
                end
            
            this_mask = squeeze(mask(mask_num,:,:));
            if mask_invert
                this_mask = 1-this_mask;
                this_mask((stimXcenter-2*fixspot_width):(stimXcenter+2*fixspot_width),(stimYcenter-2*fixspot_width):(stimYcenter+2*fixspot_width),:) = 0;
            end
            stimulus = merge_images(img,frame,this_mask);
            stimulus_BarryLyndon_crop = uint8(255*stimulus(64:447,1:512,:));
            mi(stimulus_BarryLyndon_crop,69,[1,1,1],d2s({i}));
            drawnow;%pause(1/5);%d my_pause
             
            frame_counter = frame_counter + 1;
            stim_list(frame_counter,:) = [m mask_num frame_counter category (frame_counter-1)*1/outputVideo.FrameRate img_num];
            my_imwrite(stimulus_BarryLyndon_crop, d2s({frame_counter}),d2s({video_name '_frames'})); 
            writeVideo(outputVideo,stimulus_BarryLyndon_crop);
        end
        
    end
my_save(stim_list,[video_name '_stim_list']);
close(outputVideo);
text(stimXcenter,stimYcenter,'DONE');
end %%%%%%%%
