%%%%%%%%%%% Standard Notebook Beginning %%%%%%%%%%%%
%
clc; fprintf('%s\n',[mfilename ' (' mfilename('fullpath') '.m)']);
this_filename = mfilename('fullpath');
this_file_text = fileread([this_filename,'.m']);
if not(exist('G','var'))
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
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 16 January 2015
% Now I need to genearlize the overall analysis in cell 100. This is done
% in cell 110.
% I want to update the modification of equal head/torso area to remove
% examples where head is substantially greater than torso. This is done in
% cell 120. The new segmentations are referred to as 'modified2' for both
% head and torso/shirt.
%
% In cell 130 I begin looking at bar charts of the data.
% For animals, I would like to find a subset of images for which torso and
% head have similar levels of activation in the model P-images. There are
% some subtleties in doing this properly. It has to be done at the level of
% the segmentations, before measuring the mean activation values.
%
% I am thinking there may be an eccentricity confound in the results. To test this,
% divide the images into groups such that the face is more eccentric versus that the
% body is more eccentric. Cell 2 is relvant here.
% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 18 January 2015, Sunday
% I modified cell 10 to make a more general way of loading essential data.
%
% In cell 140 I attempt to sort images by predicted response to animal
% torso in order to choose animal images that have comparable predicted activation in
% both head and torso.
% Cell 150 is a second pass at bar charts.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 21 January 2015, Wednesday
% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%% load required data %%%%%%%%%%%%%%%%%%
if GO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
CELL_NUM = 10;

    kay = '/fMRI_top_node/data.fMRI/experiment-Kay_2008';
    aJ = '/after_January_2015/';
    sF = '/stimuli-stimTrn/segmentations/';
    essential_data = {...
        {'S1_Pimages_15Oct2014',[G.Desktop kay aJ 'S1_Pimages_15Oct2014.735977.3739.mat']},...
        {'S2_Pimages_15Oct2014',[G.Desktop kay aJ 'S2_Pimages_15Oct2014.735977.3775.mat']},...
        {'S3_Pimages_15Oct2014',[G.Desktop kay aJ 'S3_Pimages_15Oct2014.735977.3819.mat']},...
        {'stimTrn512_segmentations_animal_heads_int8',[G.Desktop kay sF 'stimTrn512_segmentations_animal_heads_int8.735979.5968.mat']},...
        {'stimTrn512_segmentations_animal_torsos_int8',[G.Desktop kay sF 'stimTrn512_segmentations_animal_torsos_int8.735979.5969.mat']},...
        {'stimTrn512_segmentations_human_heads_int8',[G.Desktop kay sF 'stimTrn512_segmentations_human_heads_int8.735977.2433.mat']},...
        {'stimTrn512_segmentations_human_shirts_int8',[G.Desktop kay sF 'stimTrn512_segmentations_human_shirts_int8.735977.2434.mat']},...
        {'stimTrn512_segmentations_human_shirts_modified2_int8',[G.Desktop kay sF 'stimTrn512_segmentations_human_heads_modified2_int8.735980.257.mat']},...
        {'stimTrn512_segmentations_human_shirts_modified2_int8',[G.Desktop kay sF 'stimTrn512_segmentations_human_shirts_modified2_int8.735980.257.mat']},...
        {'stimTrn512_segmentations_animal_torsos_modified2_int8',[G.Desktop kay sF 'stimTrn512_segmentations_animal_heads_modified2_int8.735980.2582.mat']},...
        {'stimTrn512_segmentations_animal_torsos_modified2_int8',[G.Desktop kay sF 'stimTrn512_segmentations_animal_torsos_modified2_int8.735980.2582.mat']},...   
        {'stimTrn512_segmentations_extended_texture_regions_int8',[G.Desktop kay sF 'stimTrn512_segmentations_extended_texture_regions_int8.735979.4325.mat']},...    
        {'stimTrn512_segs_extended_texture_regions_without_edges_int8',[G.Desktop kay sF 'stimTrn512_segs_extended_texture_regions_without_edges_int8.735979.5032.mat']},...
        {'segmentation_results',[G.Desktop kay sF 'segmentation_results.18Jan2015_Sunday_morning.735982.4036.mat']}
        %{'segmentation_results',[G.Desktop kay sF 'segmentation_results.735980.3452.mat']}
        };

    something_loaded = false;
    for i = 1:length( essential_data )
        var_str = essential_data{i}{1};
        file_path = essential_data{i}{2};
        if not(exist(var_str))
            something_loaded = true;
            fprintf(['\nLoading ' var_str '...']); 
            load(file_path);
        end
    end
    if something_loaded
        fprintf([' Done loading.\n']);
    end
    
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%




%%%%%%%%%%%%%%%%%% bar chart making, second pass %%%%%%%%%%%%%
if GO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 150; %% updated from cell 100.
%%%%%%%%%%%%%%%%%%%%% specify input below %%%%%%%%%%%%%%
%   
    
    for subj = 1:3%1%
        clear ms; clear ses;
        seg_ctr = 0;
        for data_version = [1 3]%1%
    for seg = [6 7];%[12 13];%[6 7 12 13]%;[2 3 10 11]%%1:13;%[1 2 3 4 5 6 7 8 9]
        
        seg_ctr = seg_ctr + 1; 
        for roi = [V1 V2]%V1%
               
            a=segmentation_results.s(subj).roi(roi).data_version(data_version).segmentation(seg).mean_vals;
            m = mean(a);
            se = std(a)/sqrt(length(a));
            ses(seg_ctr,roi) = se;
            ms(seg_ctr,roi) = m;

            fsp(2,[1,3,subj]);
            h = barwitherr(ses, ms);
            set(gca,'XTickLabel',{'heads (data)','torsos (data)','heads (model)','torsos (model)'})
            legend('V1','V2')
            %xlabel('mean P-image value in region')
            %set(gca,'XTickLabel',{'V1','V2'})
            ylabel('mean P-image value in region');
            set(h(1),'FaceColor','k');
            %axis([0 28 -1.3 1.3])
            %if subj==1
                xlabel(fix_(segmentation_results.s(subj).roi(V1).data_version(1).segmentation(seg).seg_str));
            %end
            title(d2s({'Subject ' subj}));
        end
    end
        end
    end
end  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%   y = randn(3,4);         % random y values (3 groups of 4 parameters) 
%   errY = 0.1.*y;          % 10% error
%   h = barwitherr(errY, y);% Plot with errorbars
% 
%   set(gca,'XTickLabel',{'Group A','Group B','Group C'})
%   legend('Parameter 1','Parameter 2','Parameter 3','Parameter 4')
%   ylabel('Y Value')
%   set(h(1),'FaceColor','k');





%%%%%%%%%%%%%%%%%% bar chart making %%%%%%%%%%%%%
if NO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 130; %% updated from cell 100.
%%%%%%%%%%%%%%%%%%%%% specify input below %%%%%%%%%%%%%%
%
%    close('all');
%     a=segmentation_results.s(subj).roi(V1).data_version(3).segmentation(9).mean_vals;
%     more_textured_animal_bodies_V1 = find(a>=0.40);
%     b=segmentation_results.s(subj).roi(V2).data_version(3).segmentation(9).mean_vals;
%     more_textured_animal_bodies_V2 = find(b>=0.40);
    % a segmentation # for a given roi should work for all the related
    % things (animal heads modified 2 and animal torsos modified 2.) If it
    % doesn't, it suggests a mistake.
    
    %[length(segmentation_results.s(subj).roi(V1).data_version(3).segmentation(9).mean_vals) length(more_textured_animal_bodies)]
    for seg = 1:13;%[1 2 3 4 5 6 7 8 9]
        for subj = 1:3

%                 a=segmentation_results.s(subj).roi(V1).data_version(1).segmentation(seg).mean_vals;
%                 b=segmentation_results.s(subj).roi(V1).data_version(1).segmentation(seg).mean_vals;
%                 m1 = [mean(a) mean(b)];
%                 se1 = [std(a)/sqrt(length(a)) std(b)/sqrt(length(b))];
%                 a=segmentation_results.s(subj).roi(V1).data_version(1).segmentation(seg).mean_vals;
%                 b=segmentation_results.s(subj).roi(V1).data_version(1).segmentation(seg).mean_vals;
%                 m2 = [mean(a) mean(b)];
%                 se2 = [std(a)/sqrt(length(a)) std(b)/sqrt(length(b))];
                
                a=segmentation_results.s(subj).roi(V1).data_version(1).segmentation(seg).mean_vals;
                b=segmentation_results.s(subj).roi(V1).data_version(3).segmentation(seg).mean_vals;
                m1 = [mean(a) mean(b)];
                se1 = [std(a)/sqrt(length(a)) std(b)/sqrt(length(b))];
                a=segmentation_results.s(subj).roi(V2).data_version(1).segmentation(seg).mean_vals;
                b=segmentation_results.s(subj).roi(V2).data_version(3).segmentation(seg).mean_vals;
                m2 = [mean(a) mean(b)];
                se2 = [std(a)/sqrt(length(a)) std(b)/sqrt(length(b))];


            ses = [se1;se2];
            ms = [m1;m2];

            fsp(seg+100,[1,3,subj]);barwitherr(ses, ms);
            set(gca,'XTickLabel',{'V1','V2'})
            %legend('data','model')
            xlabel('mean P-image value in region')
            set(gca,'XTickLabel',{'V1','V2'})
            ylabel('mean P-image value in region');
            axis([0 3 -1.3 1.3])
            if subj==1
                my_title(segmentation_results.s(subj).roi(V1).data_version(1).segmentation(seg).seg_str);
            end
        end
    end
end  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%









%%%%%%%%%%%%%%%%%% sorting images by predicted response in animal torso %%%%%%%%%%%%%
if NO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 140;
    a = segmentation_results.s(1).roi(V1V2).data_version(3).segmentation(2) % in this run, segmentation 2 is animal torsos.
    if not(strcmp('stimTrn512_segmentations_animal_torsos_int8',a.seg_str))
        error('incorrect segmentation');
    end
    fsp(100,[1,1,1]);hist(a.mean_vals);
    [V,I] = sort(a.mean_vals);
    hist(a.mean_vals(I(50:length(I))));
    low_texture_bodies = a.image_nums(I(1:200));
    a.mean_vals(I(1:10)) % these are images with low animal torso values.
    stimTrn512_segs_animal_heads_textured_bodies_int8 = stimTrn512_segmentations_animal_heads_int8;
    stimTrn512_segs_animal_torsos_textured_bodies_int8 = stimTrn512_segmentations_animal_torsos_int8;
    stimTrn512_segs_animal_heads_textured_bodies_modified2_int8 = stimTrn512_segmentations_animal_heads_modified2_int8;
    stimTrn512_segs_animal_torsos_textured_bodies_modified2_int8 = stimTrn512_segmentations_animal_torsos_modified2_int8;
    
    % zero-out the images with low texture in body.
    stimTrn512_segs_animal_heads_textured_bodies_int8(low_texture_bodies,:,:)=0*stimTrn512_segs_animal_heads_textured_bodies_int8(low_texture_bodies,:,:);
    stimTrn512_segs_animal_torsos_textured_bodies_int8(low_texture_bodies,:,:)=0*stimTrn512_segs_animal_torsos_textured_bodies_int8(low_texture_bodies,:,:);
    stimTrn512_segs_animal_heads_textured_bodies_modified2_int8(low_texture_bodies,:,:)=0*stimTrn512_segs_animal_heads_textured_bodies_modified2_int8(low_texture_bodies,:,:);
    stimTrn512_segs_animal_torsos_textured_bodies_modified2_int8(low_texture_bodies,:,:)=0*stimTrn512_segs_animal_torsos_textured_bodies_modified2_int8(low_texture_bodies,:,:);

%     my_save(stimTrn512_segs_animal_heads_textured_bodies_int8,'stimTrn512_segs_animal_heads_textured_bodies_int8');
%     my_save(stimTrn512_segs_animal_torsos_textured_bodies_int8,'stimTrn512_segs_animal_torsos_textured_bodies_int8');
%     my_save(stimTrn512_segs_animal_heads_textured_bodies_modified2_int8,'stimTrn512_segs_animal_heads_textured_bodies_modified2_int8');
%     my_save(stimTrn512_segs_animal_torsos_textured_bodies_modified2_int8,'stimTrn512_segs_animal_torsos_textured_bodies_modified2_int8');
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%








%%%%%%%%%%%%%%%%%% third pass at analysis %%%%%%%%%%%%%
if NO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 110; %% updated from cell 100.
%%%%%%%%%%%%%%%%%%%%% specify input below %%%%%%%%%%%%%%
%
if 1
    subjects = 1;%1:3
    rois = [V1];%[ V1 V2 V1V2 ];
    segmentation_strs = {...
        'stimTrn512_segs_extended_texture_regions_without_edges_int8' ...
        'stimTrn512_segmentations_human_heads_int8' ...
        'stimTrn512_segmentations_human_shirts_int8' ...
        'stimTrn512_segmentations_animal_heads_int8' ...
        'stimTrn512_segmentations_animal_torsos_int8' ...
        'stimTrn512_segmentations_human_heads_modified2_int8' ...
        'stimTrn512_segmentations_human_shirts_modified2_int8' ...
        'stimTrn512_segmentations_animal_heads_modified2_int8' ...
        'stimTrn512_segmentations_animal_torsos_modified2_int8' ...
        'stimTrn512_segs_animal_heads_textured_bodies_int8' ...
        'stimTrn512_segs_animal_torsos_textured_bodies_int8' ...
        'stimTrn512_segs_animal_heads_textured_bodies_modified2_int8' ...
        'stimTrn512_segs_animal_torsos_textured_bodies_modified2_int8' ...
    };
end
if 0
    subjects = 1
    rois = [ V1 V2 ];
    segmentation_strs = {...
        'stimTrn512_segs_animal_heads_textured_bodies_int8' ...
        'stimTrn512_segs_animal_torsos_textured_bodies_int8' ...
        'stimTrn512_segs_animal_heads_textured_bodies_modified2_int8' ...
        'stimTrn512_segs_animal_torsos_textured_bodies_modified2_int8' ...
    };
end
%%%%%%%%%%%%%%%%%%%%% end specify input %%%%%%%%%%%%%%%%
    
    clear segmentation_results;
    tic
    for subj = subjects
        Pimages = eval(d2s({'S' subj '_Pimages_15Oct2014'}));
        for r = 1:length(rois)
            roi = rois(r);
            pimage_roi_coverage = Pimages.roi(roi).coverage_mask;
            pimage_roi_coverage_512 = doubleMatrixSize(doubleMatrixSize( pimage_roi_coverage ));
            for data_version = 1%1:3

                if data_version == 1
                    data_version_str = 'average';
                    the_pimages = squeeze(Pimages.roi(roi).stim(TRN).average);
                elseif data_version == 2
                    data_version_str = 'predicted';
                    the_pimages = Pimages.roi(roi).stim(TRN).predicted;                  
                elseif data_version == 3
                    data_version_str = 'predicted-gamma';
                    the_pimages = Pimages.roi(roi).stim(TRN).predicted;
                else
                    error('');
                end
                
                for seg = 1:length(segmentation_strs)
                    seg_str = segmentation_strs{seg};
                    segmentation = eval(seg_str);
                    ctr = 0;
                    clear mean_vals; %this is important!!!!
                    clear image_nums;
                    clear pixel_count;
                    h = waitbar(0,d2sp({'Now processing:' fix_(seg_str) 'subj' subj 'roi' roi data_version_str})); movegui(h,'southeast');
                    i_shuffled = 1:1750;% randperm(1750); %NOTE shuffling option
                    for i = 1:1750
                        waitbar(i/1750);
                        mask = sqsing(segmentation(i,:,:));
                        mask = mask .* pimage_roi_coverage_512; % limit mask to valid parts of the p-image.
                        if length(find(mask>0))
                            ctr = ctr + 1;
                            pimg = squeeze(the_pimages(i_shuffled(i),:,:));  % NOTE shuffling option
                            if data_version == 3
                                %pimg_vals_temp = pimg(find(pimage_roi_coverage>0));
                                pimg = zeroToOneRange(pimg);
                                pimg = pimg.^0.5;
                                pimg_vals = pimg(find(pimage_roi_coverage>0));
                                pimg = pimg - mean(pimg_vals);
                                pimg = pimg / std(pimg_vals);
                                %pimg_vals_temp2 = pimg(find(pimage_roi_coverage>0))
                                %fsp(10,[1,2,1]);hist(pimg_vals_temp);fsp(10,[1,2,2]);hist(pimg_vals_temp2);pause
                            end
                            %%%%
                            pimg512 = squeeze(stimTrnHP_SD6(i,:,:));%%%doubleMatrixSize(doubleMatrixSize(pimg));%%
                            %%%%
                            masked_vals = pimg512(find(mask>0));
                            mean_vals(ctr) = mean(masked_vals);
                            image_nums(ctr) = i;
                            pixel_count(ctr) = length(find(mask>0));
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
                    segmentation_results.s(subj).roi(roi).data_version(data_version).data_version_str = data_version_str;
                    segmentation_results.s(subj).roi(roi).data_version(data_version).segmentation(seg).seg_str = seg_str;
                    segmentation_results.s(subj).roi(roi).data_version(data_version).segmentation(seg).mean_vals = mean_vals;
                    segmentation_results.s(subj).roi(roi).data_version(data_version).segmentation(seg).image_nums = image_nums;
                    segmentation_results.s(subj).roi(roi).data_version(data_version).segmentation(seg).pixel_count = pixel_count;
                end
            end
        end
    end
    toc
    
    my_save(segmentation_results, 'segmentation_results');
    
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%




%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% looking at distributions of heads across photos.
if NO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 2;
    f = 1;
    mi(sum(stimTrn512_segmentations_human_heads_modified2_int8,1),f, [1,3,1])
    mi(sum(stimTrn512_segmentations_animal_heads_modified2_int8,1),f, [1,3,2])
    f = 2;
    mi(sum(stimTrn512_segmentations_human_shirts_modified2_int8,1),f, [1,3,1])
    mi(sum(stimTrn512_segmentations_animal_torsos_modified2_int8,1),f, [1,3,2])
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%





%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% New function-based version of cell 40. Look at segmentations in color. Write results to pptx file...
if NO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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
%     the_slide = '~/Desktop/animals.pptx';
%     segmentation1_name = 'stimTrn512_segmentations_animal_heads_int8';
%     segmentation2_name = 'stimTrn512_segmentations_animal_torsos_int8';
%     segmentation3_name = 'stimTrn512_segmentations_animal_torsos_modified_int8';
%
%     the_slide = '~/Desktop/animals_modified2.pptx';
%     segmentation1_name = 'stimTrn512_segmentations_animal_heads_modified2_int8';
%     segmentation2_name = 'stimTrn512_segmentations_animal_torsos_int8';
%     segmentation3_name = 'stimTrn512_segmentations_animal_torsos_modified2_int8';
%
    the_slide = '~/Desktop/humans_modified2.pptx';
    segmentation1_name = 'stimTrn512_segmentations_human_heads_modified2_int8';
    segmentation2_name = 'stimTrn512_segmentations_human_shirts_int8';
    segmentation3_name = 'stimTrn512_segmentations_human_shirts_modified2_int8';

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
% Modify modified segmentations so that body has at least 80% num pixels as
% head, otherwise zero the segmentation.
if NO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 120;
GRAPHICS = 1;
%%%%%%%%%%%%%%%%%%%%% specify below %%%%%%%%%%%%%%
%
%     head_name = 'stimTrn512_segmentations_human_heads_int8';
%     body_name = 'stimTrn512_segmentations_human_shirts_modified_int8';
    head_name = 'stimTrn512_segmentations_animal_heads_int8';
    body_name = 'stimTrn512_segmentations_animal_torsos_modified_int8';
%
%%%%%%%%%%%%%%%%%%%%% end specify %%%%%%%%%%%%%%%%
    head_segmentations = eval(head_name);
    body_segmentations = eval(body_name);
    ctr1 = 0; ctr2 = 0;
    for i = 1:1750
        h = sqsing( head_segmentations(i,:,:) );
        summ_h = summ( h );
        if summ_h > 0
            ctr1 = ctr1 + 1;
            b = sqsing( body_segmentations(i,:,:) );
            summ_b = summ( b );
            if summ_b < 0.8 * summ_h
                head_segmentations(i,:,:) = 0 * h;
                body_segmentations(i,:,:) = 0 * b;
                ctr2 = ctr2 + 1;
            end
        end
    end
    [ctr1 ctr2]
%   Saving done manually since only two conditions.

%     stimTrn512_segmentations_human_heads_modified2_int8 = head_segmentations;
%     stimTrn512_segmentations_human_shirts_modified2_int8 = body_segmentations;
%     my_save(stimTrn512_segmentations_human_heads_modified2_int8,'stimTrn512_segmentations_human_heads_modified2_int8');
%     my_save(stimTrn512_segmentations_human_shirts_modified2_int8,'stimTrn512_segmentations_human_shirts_modified2_int8');

    stimTrn512_segmentations_animal_heads_modified2_int8 = head_segmentations;
    stimTrn512_segmentations_animal_torsos_modified2_int8 = body_segmentations;
    my_save(stimTrn512_segmentations_animal_heads_modified2_int8,'stimTrn512_segmentations_animal_heads_modified2_int8');
    my_save(stimTrn512_segmentations_animal_torsos_modified2_int8,'stimTrn512_segmentations_animal_torsos_modified2_int8');

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