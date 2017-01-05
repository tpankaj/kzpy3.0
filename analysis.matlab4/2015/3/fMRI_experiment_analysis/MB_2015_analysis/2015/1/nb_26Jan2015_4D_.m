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


if 1 %%%%%%% high pass 50s motion corrected to 22 Jan %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CELL_NUM = 0;
    if not(exist('nii1','var'))
        nii1 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/28Jan2015_50s_HP_motion_corrected_to_22Jan2015/20150118_164630mbboldmb615mmAPPSNs003a001.feat/filtered_func_data.nii.gz');
    end
    if not(exist('nii2','var'))
         nii2 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/28Jan2015_50s_HP_motion_corrected_to_22Jan2015/20150118_164630mbboldmb615mmAPPSNs005a001.feat/filtered_func_data.nii.gz');
    end
    if not(exist('nii3','var'))
         nii3 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/28Jan2015_50s_HP_motion_corrected_to_22Jan2015/20150118_164630mbboldmb615mmAPPSNs007a001.feat/filtered_func_data.nii.gz');
    end
    if not(exist('nii4','var'))
        nii4 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/22Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/26Jan2015_50s_HP_same_day_motion_corrected/20150122_144129mbboldmb615mmAPPSNs003a001.feat/filtered_func_data.nii.gz');
    end
    if not(exist('nii5','var'))
         nii5 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/22Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/26Jan2015_50s_HP_same_day_motion_corrected/20150122_144129mbboldmb615mmAPPSNs005a001.feat/filtered_func_data.nii.gz');
    end
    if not(exist('nii6','var'))
         nii6 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/22Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/26Jan2015_50s_HP_same_day_motion_corrected/20150122_144129mbboldmb615mmAPPSNs007a001.feat/filtered_func_data.nii.gz');
    end
    if not(exist('nii7','var'))
        nii7 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/25Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/28Jan2015_50s_HP_motion_corrected_to_22Jan2015/20150125_124420mbboldmb615mmAPPSNs005a001.feat/filtered_func_data.nii.gz');
    end
    if not(exist('nii8','var'))
         nii8 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/25Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/28Jan2015_50s_HP_motion_corrected_to_22Jan2015/20150125_124420mbboldmb615mmAPPSNs007a001.feat/filtered_func_data.nii.gz');
    end
    if not(exist('nii9','var'))
         nii9 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/25Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/28Jan2015_50s_HP_motion_corrected_to_22Jan2015/20150125_124420mbboldmb615mmAPPSNs009a001.feat/filtered_func_data.nii.gz');
    end
end

if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 10;
    for i = 7:9
        eval_str = d2s({'[z_img, mean_img, std_img] = z_score_4D_nii(nii' i ');'});
        eval(eval_str);
        eval_str = d2s({'runs(' i ').z_img = z_img; runs(' i ').mean_img = mean_img; runs(' i ').std_img = std_img;'});
        eval(eval_str);
    end
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    
CELL_NUM = 20;
    if not(exist('mean_func','var'))
        mean_func = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/25Jan2015_50s_HP/20150118_164630mbboldmb615mmAPPSNs003a001.feat/mean_func.nii.gz');
    end
    for r = 1:9
    for x = 60%138:-1:1
        %mi_nii(sum(runs(1).z_img(:,:,:,105:109),4),138/2,x,30,1);
        mi_nii(runs(r).std_img(:,:,:),50,x,50,1);title(r);
        pause;
    end
    end
end

if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    
    CELL_NUM = 20;
    X=50;
    for r = 1:9
        mi(rot90(squeeze(runs(r).std_img(X,:,:))),CELL_NUM,[3,3,r],d2s({'run ' r}));
    end
end