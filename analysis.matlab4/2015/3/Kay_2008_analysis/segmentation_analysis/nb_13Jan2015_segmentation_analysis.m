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
GRAPHICS = 0;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Segmentation analysis
% 13 January 2015
% Birgit made the segmentations on 500 x 500 pixel images. I previously
% translated these into structures with 512 x 512 images (using
% import_Birgit_2014_11_4_500px.m and similarly named scripts in
% analysis.matlab3.
% I now want to put these into image matricies of the same dimensionality
% as the grayscale stimuli.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% In cell 1, I make and save these four data sets as:
%   stimTrn512_segmentations_human_heads_int8.735977.2433.mat
%   stimTrn512_segmentations_human_shirts_int8.735977.2434.mat
%   stimTrn512_segmentations_animal_heads_int8.735977.2453.mat
%   stimTrn512_segmentations_animal_torsos_int8.735977.2454.mat
%
% In cell 2, I look at the distribution of human and animal heads.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% In cell 10, I load data needed for the cross image analysis
%
% In cell 20, I replicate the analysis I did previously. There is some
% concern about the effect of the size of the head region vs. the size of
% the shirt/torso region. To deal with this, I would have to adjust the
% masks to have equal areas. That will be done later.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 10;
    if not(exist('S1_Pimages_15Oct2014'))
        fprintf('loading S1_Pimages_15Oct2014.735977.3739.mat\n');
        load('~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/after_January_2015/S1_Pimages_15Oct2014.735977.3739.mat');
    end
    if not(exist('stimTrn512_segmentations_animal_heads_int8'))
        load('~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/stimuli-stimTrn/segmentations/stimTrn512_segmentations_animal_heads_int8.735977.2453.mat');
        load('~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/stimuli-stimTrn/segmentations/stimTrn512_segmentations_animal_torsos_int8.735977.2454.mat');
        load('~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/stimuli-stimTrn/segmentations/stimTrn512_segmentations_human_heads_int8.735977.2433.mat');
        load('~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/stimuli-stimTrn/segmentations/stimTrn512_segmentations_human_shirts_int8.735977.2434.mat');
    end
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 20; %% THIS NEEDS TO BE CLEANED UP
    %segmentation_strs = {'stimTrn512_segmentations_animal_heads_int8' 'stimTrn512_segmentations_animal_torsos_int8'};
    segmentation_strs = {'stimTrn512_segmentations_human_heads_int8' 'stimTrn512_segmentations_human_shirts_int8'};
    pimage_types = {'average' 'predicted'};
    
    clear mean_vals; %this is important!!!!
    
    Pimages = S1_Pimages_15Oct2014;
    for seg = 1:2;
    segmentation = eval(segmentation_strs{seg});
    
    ctr = 0;
    h = waitbar(0,['Now processing ' fix_(segmentation_strs{seg})]);
    i_shuffled = 1:1750;%randperm(1750); % NOTE shuffling option
    for i = 1:1750
        waitbar(i/1750);
        mask = sqsing(segmentation(i_shuffled(i),:,:)); % NOTE shuffling option
        if length(find(mask>0))
            ctr = ctr + 1;
            pimg = squeeze(Pimages.roi(V1V2).stim(TRN).predicted(i,:,:));
            pimg512 = doubleMatrixSize(doubleMatrixSize(pimg));
            masked_vals = pimg512(find(mask>0));
            
            mean_vals(seg,ctr) = mean(masked_vals);
            pixel_counts(seg,ctr) = length(find(mask>0));
            if GRAPHICS
                mi(mask,1,[2,2,1]);
                mi(pimg,1,[2,2,2]);
                mi(mask.*pimg512,1,[2,2,3]);
                %mp({mask.*pimg512,'o'},1,[2,2,4]);
                fsp(1,[2,2,4]);
                hist(masked_vals,100); title(median(masked_vals));
            end
        end
    end
    close(h);
    end
    
    fsp(6,[1,2,1]);hist(mean_vals(1,:));title(median(mean_vals(1,:)));fsp(6,[1,2,2]);hist(mean_vals(2,:));title(median(mean_vals(2,:)));
end

if 0 % No need to rerun this because results saved, 13Jan2015 %%%%%%%%%%%%%%
CELL_NUM = 1;

    if not(exist('Birgit_2014_10_28_head_shirt_segmentations'))
        fprintf('loading Birgit_2014_10_28_head_shirt_segmentations.735902.335.mat\n');
        load('~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/stimuli-stimTrn/segmentations/Birgit_2014_10_28_head_shirt_segmentations.735902.335.mat');
    end
    if not(exist('Birgit_2014_11_4_head_torso_segmentations'))
        fprintf('loading Birgit_2014_11_4_head_torso_segmentations.735907.4489.mat\n');
        ('~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/stimuli-stimTrn/segmentations/Birgit_2014_11_4_head_torso_segmentations.735907.4489.mat');
    end

    segmentations = { Birgit_2014_10_28_head_shirt_segmentations Birgit_2014_11_4_head_torso_segmentations };
    fields = {'head_mask' 'shirt_mask'};
    target_names = {{'stimTrn512_segmentations_human_heads_int8' 'stimTrn512_segmentations_human_shirts_int8'}...
        {'stimTrn512_segmentations_animal_heads_int8' 'stimTrn512_segmentations_animal_torsos_int8'}};
    
    for s = 1:length(segmentations)
        for f = 1:length(fields)
            tn = target_names{s}{f}
            eval( [tn ' = zeros(1750,512,512,''int8'');'] );
            h = waitbar(0,['Now processing ' tn]);
            for i = 1:length(segmentations{s})
                waitbar(i/1750);
                mask_original = eas( segmentations{s}, { i fields{f} } );
                if length(mask_original) > 0
                    mask = 0 * mask_original;
                    mask( find( mask_original > 0.1 ) ) = 1;
                    eval( [tn '(i,:,:) = mask;'] );
                    if GRAPHICS
                        if length(mask) > 0
                            mi( mask, CELL_NUM, [1,3,1], d2s({i}));
                            mp( {mask,'o'}, CELL_NUM, [1,3,2], d2s({i}));
                            fsp(CELL_NUM,[1,3,3]);
                            hist(reshape(mask,512^2,1),100);
                            drawnow;%pause(0.5);
                        end
                    end
                end
            end
            close(h);
            eval(['my_save(' tn ', ''' tn ''')']);
        end
    end
end


if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 2;
    mi(sum(stimTrn512_segmentations_human_heads_int8,1),CELL_NUM, [1,3,1])
    mi(sum(stimTrn512_segmentations_animal_heads_int8,1),CELL_NUM, [1,3,2])
    mi(sum(stimTrn512_segmentations_human_heads_int8,1)+sum(stimTrn512_segmentations_animal_heads_int8,1),CELL_NUM, [1,3,3])
end
