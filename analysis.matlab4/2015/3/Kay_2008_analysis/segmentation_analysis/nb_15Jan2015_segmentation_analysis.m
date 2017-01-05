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
NO = 0;
GO = 1;
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
% 14 January 2015
% My next goal is to make modified versions of the shirt/torso segmentations
% that keep the same (or fewer) pixels than the head segmentations.
% I do this is cell 30. There are several animal images in which the sky seems
% to bleed into the segmentation. This needs to be corrected by inspecting
% every segmentation for animals and humans. The great majority of the
% segmentations are good, however, so this is not urgent.
% The results with these modified segmentations are consistent with my
% basic impression with the original segmentations (these analyses done
% with cell 1. I now duplicate this cell to cell 100 and clean it up to
% automate over all conditions.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 15 January 2015
% First goal today is to save color versions of segmentations to pptx
% files, in order to easily inspect for flaws (such as I mentioned
% yesterday) [cell 40]. Also, change the threshold for assigning 1 in the masks to
% try to correct these [cell 1, no effect]. Then I want to bring Birgit's new texture
% segmentations into the system [cell 50]. Since she segmented up to the
% edges of figures, I modified the semgentations, shrinking them by 20 (or
% 10) pixels in Gimp, saving as
% "stimTrn512_segs_extended_texture_regions_without_edges_int8.735979.5032.mat"
% Then I need to automate the analysis for
% all parameters. I should make these cells into functions, as useful.
%
% 1:32 p.m. I saved a copy of this script as
% "nb_15Jan2015_segmentation_analysis_earlier.m". Now I am taking out cells
% that will be accessed via special functions (e.g., cell 40 changed to 41,
% using "segmentations_to_pptx.m". Also taking out outdated cells (1 and
% 20).
%
% 2:37 p.m., I corrected flaws in the animal segmentation skys, and took out
% insects [cell 99], then recalculated the modified toro segmentations
% (cell 30), saving the new segmentation as "stimTrn512_segmentations_animal_torsos_modified_int8.735979.6045.mat"
% 
% Now I need to genearlize the overall analysis in cell 100.

%%%%%%%%%%%%% load required data %%%%%%%%%%%%%%%%%%
if GO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 10;
    if not(exist('S1_Pimages_15Oct2014'))
        fprintf('loading S1_Pimages_15Oct2014.735977.3739.mat\n');
        load('~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/after_January_2015/S1_Pimages_15Oct2014.735977.3739.mat');
    end
    if not(exist('S2_Pimages_15Oct2014'))
        fprintf('loading S2_Pimages_15Oct2014.735977.3775.mat\n');
        load('~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/after_January_2015/S2_Pimages_15Oct2014.735977.3775.mat');
    end
    if not(exist('stimTrn512_segmentations_animal_heads_int8'))
        load('~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/stimuli-stimTrn/segmentations/stimTrn512_segmentations_animal_heads_int8.735979.5968.mat');
        load('~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/stimuli-stimTrn/segmentations/stimTrn512_segmentations_animal_torsos_int8.735979.5969.mat');
        load('~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/stimuli-stimTrn/segmentations/stimTrn512_segmentations_human_heads_int8.735977.2433.mat');
        load('~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/stimuli-stimTrn/segmentations/stimTrn512_segmentations_human_shirts_int8.735977.2434.mat');
    end
    if not(exist('stimTrn512_segmentations_human_shirts_modified_int8'))
        load('~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/stimuli-stimTrn/segmentations/stimTrn512_segmentations_human_shirts_modified_int8.735978.2355.mat');
    end
    if not(exist('stimTrn512_segmentations_animal_torsos_modified_int8'))
        'stimTrn512_segmentations_animal_torsos_modified_int8'
        load('~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/stimuli-stimTrn/segmentations/stimTrn512_segmentations_animal_torsos_modified_int8.735979.6045.mat');
    end
%     if not(exist(''))
%         load('.mat');
%     end
    
    if not(exist('stimTrn512_segmentations_extended_texture_regions_int8'))
        load('~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/stimuli-stimTrn/segmentations/stimTrn512_segmentations_extended_texture_regions_int8.735979.4325.mat');
    end
    if not(exist('stimTrn512_segs_extended_texture_regions_without_edges_int8'))
        load('~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/stimuli-stimTrn/segmentations/stimTrn512_segs_extended_texture_regions_without_edges_int8.735979.5032.mat');
    end
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%








%%%%%%%%%%%%%%%%%% second pass at analysis %%%%%%%%%%%%%
if NO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 100; %% updated from cell 20.
    %segmentation_strs = {'stimTrn512_segmentations_animal_heads_int8' 'stimTrn512_segmentations_animal_torsos_modified_int8'};
    %segmentation_strs = {'stimTrn512_segmentations_human_heads_int8' 'stimTrn512_segmentations_human_shirts_modified_int8'};
    segmentation_strs = {'stimTrn512_segs_extended_texture_regions_without_edges_int8'};%{'stimTrn512_segmentations_extended_texture_regions_int8'};
    pimage_types = {'average' 'predicted'};
    
    clear mean_vals; %this is important!!!!
    
    Pimages = S1_Pimages_15Oct2014;
    for seg = 1:1;
        segmentation = eval(segmentation_strs{seg});

        ctr = 0;
        h = waitbar(0,['Now processing ' fix_(segmentation_strs{seg})]);
        i_shuffled = 1:1750;% randperm(1750); %NOTE shuffling option 
        for i = 1:1750
            waitbar(i/1750);
            mask = sqsing(segmentation(i,:,:));
            if length(find(mask>0))
                ctr = ctr + 1;
                pimg = squeeze(Pimages.roi(V1V2).stim(TRN).predicted(i_shuffled(i),:,:));  % NOTE shuffling option
                pimg512 = doubleMatrixSize(doubleMatrixSize(pimg));%%squeeze(stimTrnHP_SD6(i_shuffled(i),:,:));%%%
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
        fg = 24;
        fsp(fg,[1,2,seg]);hist(mean_vals(seg,:));xlabel(fix_(segmentation_strs{seg}));title(median(mean_vals(seg,:)));
    end
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%










%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% looking at distributions of heads across photos.
if NO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 2;
    mi(sum(stimTrn512_segmentations_human_heads_int8,1),CELL_NUM, [1,3,1])
    mi(sum(stimTrn512_segmentations_animal_heads_int8,1),CELL_NUM, [1,3,2])
    mi(sum(stimTrn512_segmentations_human_heads_int8,1)+sum(stimTrn512_segmentations_animal_heads_int8,1),CELL_NUM, [1,3,3])
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%





%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% New function-based version of cell 40. Look at segmentations in color. Write results to pptx file...
if GO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 41;
GRAPHICS = 1;
    stim_str = 'Trn';
    segmentation1 = []; segmentation2 = []; segmentation3 = [];
    segmentation1_name = []; segmentation2_name = []; segmentation3_name = [];
    
%%%%%%%%%%%%%%%%%%%%% specify segmentations and slides below %%%%%%%%%%%%%%
%
%   the_slide = '~/Desktop/textures.pptx';
%   segmentation1_name = 'stimTrn512_segmentations_extended_texture_regions_int8';
%   segmentation2_name = 'stimTrn512_segs_extended_texture_regions_without_edges_int8';
% 
%    the_slide = '~/Desktop/humans.pptx';
%    segmentation1_name = 'stimTrn512_segmentations_human_heads_int8';
%    segmentation2_name = 'stimTrn512_segmentations_human_shirts_int8';
%    segmentation3_name = 'stimTrn512_segmentations_human_shirts_modified_int8';
% 
    the_slide = '~/Desktop/animals.pptx';
    segmentation1_name = 'stimTrn512_segmentations_animal_heads_int8';
    segmentation2_name = 'stimTrn512_segmentations_animal_torsos_int8';
    segmentation3_name = 'stimTrn512_segmentations_animal_torsos_modified_int8';
%
%%%%%%%%%%%%%%%%%%%%% end specify segmentations and slides %%%%%%%%%%%%%%%%

    if length(segmentation1_name)>0
        segmentation1 = eval(segmentation1_name);
    end
    if length(segmentation2_name)>0
        segmentation2 = eval(segmentation2_name);
    end
    if length(segmentation3_name)>0
        segmentation3 = eval(segmentation3_name);
    end
    segmentations_to_pptx( G.stimTrn512_int8, segmentation1, segmentation2, segmentation3,  the_slide, d2c({segmentation1_name segmentation2_name segmentation3_name}) );
    
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%







%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Modify segmentations so that body has the same number of pixels as the
% head (unless it had fewer to begin with, in which case it is unchanged.
if NO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 30;
GRAPHICS = 1;
%     head_name = 'stimTrn512_segmentations_human_heads_int8';
%     body_name = 'stimTrn512_segmentations_human_shirts_int8';
    head_name = 'stimTrn512_segmentations_animal_heads_int8';
    body_name = 'stimTrn512_segmentations_animal_torsos_int8';
    
    head_segmentations = eval(head_name);
    body_segmentations = eval(body_name);
    body_segmentations_modified = 0 * body_segmentations;

    for i = 1:1750
        h = sqsing( head_segmentations(i,:,:) );
        if summ( h ) > 0
            [x y] = find(h); cent=round([mean(x) mean(y)]);
            b = sqsing( body_segmentations(i,:,:) );
            b_mod = select_positive_pixel_count_nearest_specified_center( b, summ(h), cent );
            body_segmentations_modified(i,:,:) = b_mod;
            if GRAPHICS
                ci = gray_image_to_color(h);
                ci(:,:,2) = b;
                ci(:,:,3)= b_mod;
                mi(ci,1,[1,4,1],d2s({i}));
                drawnow;
            end
        end
    end
%   Saving done manually since only two conditions.
   stimTrn512_segmentations_animal_torsos_modified_int8 = body_segmentations_modified;
   my_save(stimTrn512_segmentations_animal_torsos_modified_int8,'stimTrn512_segmentations_animal_torsos_modified_int8');
    
%     stimTrn512_segmentations_human_shirts_modified_int8 = body_segmentations_modified
%     my_save(stimTrn512_segmentations_human_shirts_modified_int8,'stimTrn512_segmentations_human_shirts_modified_int8');
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%






%%%%%%%%%%%%%%%%%% 15 January 2015, put Birgit's texture segmentations into system %%%%%%%%%%%%%
if NO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 50;
GRAPHICS = 1;
    image_path = '~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/stimuli-stimTrn/segmentations/Birgit_2015_1_14_512px_textures_without_edges';
    segmentation_name = 'stimTrn512_segs_extended_texture_regions_without_edges_int8';
%     image_path = '~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/stimuli-stimTrn/segmentations/Birgit_2015_1_14_512px_textures';
%     segmentation_name = 'stimTrn512_segmentations_extended_texture_regions_int8';
    
    %%%%
    segmentations = zeros(1750,512,512,'int8');

    [indicies,names] = get_set_of_indicies2_2( image_path, 'png' );
    
    for j = 1:length(indicies)
        i = indicies(j);
        i
        filepathname = fullfile(image_path, names{j});
        mask = zeroToOneRange( imread(filepathname));

        mask( find( mask > 0.5 ) ) = 1;
        mask( find( mask < 1 ) ) = 0;
        if maxx(mask) > 1
            error('if maxx(mask) > 1');
        end
        if minn(mask) < 0
            error('if minn(mask) < 0');
        end

        segmentations(i,:,:) = mask;
        
        if GRAPHICS
            mi(mask,1,[1,1,1],d2c({names{j} i}));pause(0.2);
        end
    end

    eval(['my_save( segmentations,  ''', segmentation_name, ''' );']);
end



%%%%%%%%%%%%%%%%%% 15 January 2015, correct flaws in animals %%%%%%%%%%%%%
if NO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 99;

zero_out_these_non_animals = [6 1510 1308 1285 886 590 501 362 373 212]
remove_sky_flaw_in_these = [9 57 230];

%     stimTrn512_segmentations_animal_with_insect_heads_int8 = stimTrn512_segmentations_animal_heads_int8;
%     stimTrn512_segmentations_animal_with_insect_torsos_int8 = stimTrn512_segmentations_animal_torsos_int8;

    if 0 %%% zero out the insects --- done
        for j = 1:length(zero_out_these_non_animals)
            i = zero_out_these_non_animals(j);
            stimTrn512_segmentations_animal_heads_int8(i,:,:) = 0 * stimTrn512_segmentations_animal_heads_int8(i,:,:);
            stimTrn512_segmentations_animal_torsos_int8(i,:,:) = 0 * stimTrn512_segmentations_animal_torsos_int8(i,:,:);
            mi(stimTrn512_segmentations_animal_with_insect_heads_int8(i,:,:),1,[2,3,1]);
            mi(stimTrn512_segmentations_animal_with_insect_torsos_int8(i,:,:),1,[2,3,2]);
            mi(stimTrn512_segmentations_animal_heads_int8(i,:,:),1,[2,3,4]);
            mi(stimTrn512_segmentations_animal_torsos_int8(i,:,:),1,[2,3,5]);
            mi(G.stimTrn512_int8(i,:,:),1,[2,3,3]);
            pause;
        end
    end
    if 0 %%% fix skys --done
        for j = 1:length(remove_sky_flaw_in_these)
            i = remove_sky_flaw_in_these(j);
%             stimTrn512_segmentations_animal_heads_int8(i,:,:) = 0 * stimTrn512_segmentations_animal_heads_int8(i,:,:);
%             stimTrn512_segmentations_animal_torsos_int8(i,:,:) = 0 * stimTrn512_segmentations_animal_torsos_int8(i,:,:);
            a = squeeze(stimTrn512_segmentations_animal_heads_int8(i,:,:));
            b = squeeze(stimTrn512_segmentations_animal_torsos_int8(i,:,:));

            mi(a,1,[2,3,1]);
            mi(b,1,[2,3,2]);
            
            a(1:125,:)=0;b(1:125,:)=0;
            stimTrn512_segmentations_animal_heads_int8(i,:,:)=a;
            stimTrn512_segmentations_animal_torsos_int8(i,:,:)=b;
            
            mi(stimTrn512_segmentations_animal_heads_int8(i,:,:),1,[2,3,4]);
            mi(stimTrn512_segmentations_animal_torsos_int8(i,:,:),1,[2,3,5]);
            mi(G.stimTrn512_int8(i,:,:),1,[2,3,3]);
            pause;
        end
    end
    my_save(stimTrn512_segmentations_animal_heads_int8,'stimTrn512_segmentations_animal_heads_int8');
    my_save(stimTrn512_segmentations_animal_torsos_int8,'stimTrn512_segmentations_animal_torsos_int8');
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%% older stuff below %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%