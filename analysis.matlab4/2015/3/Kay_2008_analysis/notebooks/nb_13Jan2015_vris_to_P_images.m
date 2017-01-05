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
% 13 January 2015
% P-image is the name Kendrick came up with in November 2014.
% It replaces voxel response image (vri) which I had used previous.
% I previously saved vri data for the three subjects in the
% 15Oct2014_vri_datasets folder. These are complex structures. The goal of
% this notebook is to translate the vri_dataset structures into
% image-indexed arrays of images. Eventually I would like to use folders
% to organize the data.
% This should make it easy to see what is there, to load subsets of the
% data quickly, and to facilitate the addition of new versions of the data
% produced by new analyses.
% For the moment, I will use a more minor rearrangement of the vri
% structures.
%
% I save these in after_January_2015 as:
%
%   S1_Pimages_15Oct2014.735977.3739.mat
%   S2_Pimages_15Oct2014.735977.3775.mat
%
%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    if not(exist('S1_vri_dataset'))
        load('~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/after_January_2014/15Oct2014_vri_datasets/S1_vri_dataset.735887.8626.mat')
    end
    vri_dataset = S1_vri_dataset;
end
if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 2;
    if not(exist('S2_vri_dataset'))
        load('~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/after_January_2014/15Oct2014_vri_datasets/S2_vri_dataset.735887.8643.mat')
    end
    vri_dataset = S2_vri_dataset;
end
if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 3;
    if not(exist('S3_vri_dataset'))
        load('~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/after_January_2014/15Oct2014_vri_datasets/S3_vri_dataset.735887.866.mat')
    end
    vri_dataset = S3_vri_dataset;
end

if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 10;

    roi_strs = {'V1' 'V2' 'V1V2'};
    roi_nums = [V1 V2 V1V2];
    stim_strs = {'Trn' 'Val'};
    stim_nums = [TRN VAL];
    stim_lens = [1750 120];
    num_presentations = [2 13];
    v = 1; subj = 2; % subject number doesn't matter here because I save the subjects separately.

    for r = 1:length(roi_strs)
        r
        roi_str = roi_strs{r};
        roi = roi_nums(r);
        for s = 1:length(stim_strs)
            stim_str = stim_strs{s};
            stim = stim_nums(s);
            stim_len = stim_lens(s);
            num_pres = num_presentations(s);
            
            Pimage_dataset.v(v).s(subj).roi(roi).stim(stim).average = zeros(stim_len,128,128,'single');
            Pimage_dataset.v(v).s(subj).roi(roi).stim(stim).predicted = zeros(stim_len,128,128,'single');
            Pimage_dataset.v(v).s(subj).roi(roi).stim(stim).presentations = zeros(stim_len,num_pres,128,128,'single');
            Pimage_dataset.v(v).s(subj).roi(roi).sum_of_contiguous_RFs = eas(vri_dataset,{roi_str 'sum_of_contiguous_RFs'});
            Pimage_dataset.v(v).s(subj).roi(roi).coverage_mask = eas(vri_dataset,{roi_str 'coverage_mask'});
            Pimage_dataset.v(v).s(subj).roi(roi).min_overlapping_voxels = eas(vri_dataset,{roi_str 'min_overlapping_voxels'});

            cm = Pimage_dataset.v(v).s(subj).roi(roi).coverage_mask;
            
            for i = 1:stim_len
                Pimage_dataset.v(v).s(subj).roi(roi).stim(stim).average(i,:,:) = eas(vri_dataset,{roi_str stim_str i 'average' 'z_img'});
                Pimage_dataset.v(v).s(subj).roi(roi).stim(stim).predicted(i,:,:) = eas(vri_dataset,{roi_str stim_str i 'predicted' 'z_img'});
                for j = 1:num_pres
                    Pimage_dataset.v(v).s(subj).roi(roi).stim(stim).presentations(i,j,:,:) = eas(vri_dataset,{roi_str stim_str i 'presentation' j 'z_img'});
                    %mi(Pimage_dataset.v(v).s(subj).roi(roi).stim(stim).presentations(i,j,:,:),1,[4,4,j]);
                end
                %mi(squeeze(Pimage_dataset.v(v).s(subj).roi(roi).stim(stim).average(i,:,:)),1,[4,4,16]);
                %mi(Pimage_dataset.v(v).s(subj).roi(roi).stim(stim).predicted(i,:,:),2,[1,2,2]);
                %pause
            end
        end
    end
    %S1_Pimages_15Oct2014 = Pimage_dataset.v(v).s(subj);
    %my_save(S1_Pimages_15Oct2014, 'S1_Pimages_15Oct2014');
    %S2_Pimages_15Oct2014 = Pimage_dataset.v(v).s(subj);
    %my_save(S2_Pimages_15Oct2014, 'S2_Pimages_15Oct2014');
    %S3_Pimages_15Oct2014 = Pimage_dataset.v(v).s(subj);
    %my_save(S3_Pimages_15Oct2014, 'S3_Pimages_15Oct2014');
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 20;

    roi = V1V2;
    stim = VAL;

    v = 1;
    for i = 1:1750
        mi(squeeze(Pimage_dataset.v(v).s(subj).roi(roi).stim(stim).average(i,:,:)),1,[1 2 1]);
        mi(Pimage_dataset.v(v).s(subj).roi(roi).stim(stim).predicted(i,:,:),1,[1,2,2]);
        pause
    end

end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

