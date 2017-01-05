%%%%%%%%%%% Standard Notebook Beginning %%%%%%%%%%%%
%
clc; fprintf('%s\n',[mfilename ' (' mfilename('fullpath') '.m)']);
this_filename = mfilename('fullpath');
this_file_text = fileread([this_filename,'.m']);
if not(exist('G'))
    error('NOTE: run local_startup.m manually at the beginning of the Matlab session.');
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This script coordinates calls to z_score_4D_nii
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% what to do %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
year = 2015;
month = 6;
subject = 'HVO';
session = 15;
fsl_subfolder = 'mc_to_006a_of_9Feb2015';
feat_folders = {... % do not use .feat extension
    '20150614_164413mbboldmb620mmAPPSNs006a001' ...
    '20150614_164413mbboldmb620mmAPPSNs008a001' ...
    '20150614_164413mbboldmb620mmAPPSNs010a001' ...
    '20150614_164413mbboldmb620mmAPPSNs012a001' ...
    '20150614_164413mbboldmb620mmAPPSNs014a001' ...
    '20150614_164413mbboldmb620mmAPPSNs016a001' ...
    '20150614_164413mbboldmb620mmAPPSNs018a001' ...
    '20150614_164413mbboldmb620mmAPPSNs020a001' ...
};
% session = 14;
% fsl_subfolder = 'mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%    '20150614_093445mbboldmb620mmAPPSNs004a001' ...
%    '20150614_093445mbboldmb620mmAPPSNs006a001' ...
%    '20150614_093445mbboldmb620mmAPPSNs008a001' ...
%    '20150614_093445mbboldmb620mmAPPSNs010a001' ...
%    '20150614_093445mbboldmb620mmAPPSNs012a001' ...
%    '20150614_093445mbboldmb620mmAPPSNs014a001' ...
%    '20150614_093445mbboldmb620mmAPPSNs016a001' ...
%    '20150614_093445mbboldmb620mmAPPSNs018a001' ...
%     '20150614_093445mbboldmb620mmAPPSNs020a001' ...
% };

% month = 4;
% subject = 'HVO';
% session = 7;
% fsl_subfolder = 'mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     '20150407_081930mbboldmb620mmAPPSNs004a001' ...
%     '20150407_081930mbboldmb620mmAPPSNs006a001' ...
%     '20150407_081930mbboldmb620mmAPPSNs008a001' ...
%     '20150407_081930mbboldmb620mmAPPSNs014a001' ...
%     '20150407_081930mbboldmb620mmAPPSNs016a001' ...
%     '20150407_081930mbboldmb620mmAPPSNs018a001' ...
% };
% session = 3;
% fsl_subfolder = 'mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     '20150403_081859mbboldmb620mmAPPSNs016a001' ...
%     '20150403_081859mbboldmb620mmAPPSNs018a001' ...
%     '20150403_081859mbboldmb620mmAPPSNs020a001' ...
%     '20150403_081859mbboldmb620mmAPPSNs022a001' ...
%     '20150403_081859mbboldmb620mmAPPSNs030a001' ...
%     '20150403_081859mbboldmb620mmAPPSNs032a001' ...
%     '20150403_081859mbboldmb620mmAPPSNs034a001' ...
% };
% session = 2;
% fsl_subfolder = 'mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     '20150402_082238mbboldmb620mmAPPSNs006a001' ...
%     '20150402_082238mbboldmb620mmAPPSNs008a001' ...
%     '20150402_082238mbboldmb620mmAPPSNs010a001' ...
%     '20150402_082238mbboldmb620mmAPPSNs012a001' ...
%     '20150402_082238mbboldmb620mmAPPSNs014a001' ...
% };
% month = 3;
% subject = 'HVO';
% session = 30;
% fsl_subfolder = 'mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     '20150330_082317mbboldmb620mmAPPSNs004a001' ...
%     '20150330_082317mbboldmb620mmAPPSNs006a001' ...
%     '20150330_082317mbboldmb620mmAPPSNs010a001' ...
%     '20150330_082317mbboldmb620mmAPPSNs012a001' ...
%     '20150330_082317mbboldmb620mmAPPSNs018a001' ...
%     '20150330_082317mbboldmb620mmAPPSNs020a001' ...
%     '20150330_082317mbboldmb620mmAPPSNs022a001' ...
%     '20150330_082317mbboldmb620mmAPPSNs024a001' ...
% };
% session = 29;
% fsl_subfolder = 'mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     '20150329_102756mbboldmb620mmAPPSNs004a001' ...
%     '20150329_102756mbboldmb620mmAPPSNs006a001' ...
%     '20150329_102756mbboldmb620mmAPPSNs008a001' ...
%     '20150329_102756mbboldmb620mmAPPSNs010a001' ...
%     '20150329_102756mbboldmb620mmAPPSNs016a001' ...
%     '20150329_102756mbboldmb620mmAPPSNs020a001' ...
%     '20150329_102756mbboldmb620mmAPPSNs022a001' ...
%     '20150329_102756mbboldmb620mmAPPSNs026a001' ...
% };
% session = 27;
% fsl_subfolder = 'mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     '20150327_080630mbboldmb620mmAPPSNs004a001' ...
%     '20150327_080630mbboldmb620mmAPPSNs006a001' ...
%     '20150327_080630mbboldmb620mmAPPSNs008a001' ...
%     '20150327_080630mbboldmb620mmAPPSNs010a001' ...
%     '20150327_080630mbboldmb620mmAPPSNs016a001' ...
%     '20150327_080630mbboldmb620mmAPPSNs018a001' ...
%     '20150327_080630mbboldmb620mmAPPSNs020a001' ...
%     '20150327_080630mbboldmb620mmAPPSNs022a001' ...
% };
% session = 26;
% fsl_subfolder = 'mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     '20150326_082236mbboldmb620mmAPPSNs006a001' ...
%     '20150326_082236mbboldmb620mmAPPSNs008a001' ...
%     '20150326_082236mbboldmb620mmAPPSNs010a001' ...
%     '20150326_082236mbboldmb620mmAPPSNs012a001' ...
%     '20150326_082236mbboldmb620mmAPPSNs018a001' ...
%     '20150326_082236mbboldmb620mmAPPSNs020a001' ...
%     '20150326_082236mbboldmb620mmAPPSNs022a001' ...
% };
% session = 24;
% fsl_subfolder = 'mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     '20150324_081252mbboldmb620mmAPPSNs004a001' ...
%     '20150324_081252mbboldmb620mmAPPSNs006a001' ...
%     '20150324_081252mbboldmb620mmAPPSNs008a001' ...
%     '20150324_081252mbboldmb620mmAPPSNs010a001' ...
%     '20150324_081252mbboldmb620mmAPPSNs016a001' ...
%     '20150324_081252mbboldmb620mmAPPSNs018a001' ...
%     '20150324_081252mbboldmb620mmAPPSNs020a001' ...
%     '20150324_081252mbboldmb620mmAPPSNs022a001' ...
% };
% session = 23;
% fsl_subfolder = 'mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     '20150323_081841mbboldmb620mmAPPSNs004a001' ...
%     '20150323_081841mbboldmb620mmAPPSNs006a001' ...
%     '20150323_081841mbboldmb620mmAPPSNs008a001' ...
%     '20150323_081841mbboldmb620mmAPPSNs010a001' ...
% };
% subject = 'AA';
% session = 22;
% fsl_subfolder = 'mc_to_016a_of_22Mar2015';
% feat_folders = {... % do not use .feat extension
%     '20150322_165752mbboldmb620mmAPPSNs004a001' ...
%     '20150322_165752mbboldmb620mmAPPSNs006a001' ...
%     '20150322_165752mbboldmb620mmAPPSNs008a001' ...
%     '20150322_165752mbboldmb620mmAPPSNs010a001' ...
%     '20150322_165752mbboldmb620mmAPPSNs012a001' ...
%     '20150322_165752mbboldmb620mmAPPSNs014a001' ...
%     '20150322_165752mbboldmb620mmAPPSNs016a001' ...
% };
% subject = 'HVO';
% session = 21;
% fsl_subfolder = 'mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     '20150321_165030mbboldmb620mmAPPSNs004a001' ...
%     '20150321_165030mbboldmb620mmAPPSNs006a001' ...
%     '20150321_165030mbboldmb620mmAPPSNs008a001' ...
%     '20150321_165030mbboldmb620mmAPPSNs010a001' ...
%     '20150321_165030mbboldmb620mmAPPSNs016a001' ...
%     '20150321_165030mbboldmb620mmAPPSNs018a001' ...
%     '20150321_165030mbboldmb620mmAPPSNs020a001' ...
%     '20150321_165030mbboldmb620mmAPPSNs022a001' ...
% };
% session = 20;
% fsl_subfolder = 'mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     % '20150319_143524mbboldmb620mmAPPSNs004a001' ...
%     % '20150319_143524mbboldmb620mmAPPSNs006a001' ...
%     % '20150319_143524mbboldmb620mmAPPSNs008a001' ...
%     % '20150319_143524mbboldmb620mmAPPSNs010a001' ...
%     '20150319_143524mbboldmb620mmAPPSNs016a001' ...
%     '20150319_143524mbboldmb620mmAPPSNs018a001' ...
%     '20150319_143524mbboldmb620mmAPPSNs020a001' ...
%     '20150319_143524mbboldmb620mmAPPSNs022a001' ...
% };
% session = 19;
% fsl_subfolder = 'mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     '20150319_082633mbboldmb620mmAPPSNs004a001' ...
%     '20150319_082633mbboldmb620mmAPPSNs006a001' ...
%     '20150319_082633mbboldmb620mmAPPSNs008a001' ...
%     %'20150319_082633mbboldmb620mmAPPSNs010a001' ...
% };
% session = 18;
% fsl_subfolder = 'mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     '20150318_082104mbboldmb620mmAPPSNs004a001' ...
%     '20150318_082104mbboldmb620mmAPPSNs006a001' ...
%     '20150318_082104mbboldmb620mmAPPSNs008a001' ...
%     '20150318_082104mbboldmb620mmAPPSNs010a001' ...
% };
% session = 16;
% fsl_subfolder = 'mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     %'20150316_081001mbboldmb620mmAPPSNs004a001' ...
%     %'20150316_081001mbboldmb620mmAPPSNs008a001' ...
%     '20150316_081001mbboldmb620mmAPPSNs010a001' ...
%     %'task_failure_20150316_081001mbboldmb620mmAPPSNs006a001' ...
% };
% subject = 'HVO';
% session = 14;
% fsl_subfolder = 'mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     '20150314_133430mbboldmb620mmAPPSNs004a001' ...
%     '20150314_133430mbboldmb620mmAPPSNs006a001' ...
%     '20150314_133430mbboldmb620mmAPPSNs008a001' ...
%     '20150314_133430mbboldmb620mmAPPSNs010a001'};
%%%%%%%%%%%%%%%%%%%%
% subject = 'AV';
% session = 12;
% fsl_subfolder = 'mc_to_004a_of_12Mar2015';
% feat_folders = {... % do not use .feat extension
%     '20150312_173814mbboldmb620mmAPPSNs004a001' ...
%      '20150312_173814mbboldmb620mmAPPSNs006a001' ...
%      '20150312_173814mbboldmb620mmAPPSNs008a001' ...
%      '20150312_173814mbboldmb620mmAPPSNs012a001' ...
%      '20150312_173814mbboldmb620mmAPPSNs014a001' ...
%     };
%%%%%%%%%%%%%%%%%%%%
% subject = 'HVO';
% session = 9;
% fsl_subfolder = 'mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     '20150309_081313mbboldmb620mmAPPSNs006a001' ...
%      '20150309_081313mbboldmb620mmAPPSNs008a001' ...
%      '20150309_081313mbboldmb620mmAPPSNs010a001' ...
%      '20150309_081313mbboldmb620mmAPPSNs012a001'};
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% year = 2015;
% month = 2;
% %%%%%%%%%%%%%%%%%%%%
% subject = 'HVO';
% session = 20;
% fsl_subfolder = 'mc_to_004a_of_20Feb2015';
% feat_folders = {... % do not use .feat extension
%     '20150220_082727mbboldmb820mmAPPSNs004a001' ...
%      '20150220_082727mbboldmb820mmAPPSNs006a001' ...
%      '20150220_082727mbboldmb820mmAPPSNs008a001'};
%%%%%%%%%%%%%%%%%%%%
% subject = 'HVO';
% session = 26;
% fsl_subfolder = 'mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     '20150226_082625mbboldmb820mmAPPSNs004a001' ...
%     '20150226_082625mbboldmb820mmAPPSNs006a001' ...
%     '20150226_082625mbboldmb820mmAPPSNs008a001' ...
%     '20150226_082625mbboldmb820mmAPPSNs010a001'};
%%%%%%%%%%%%%%%%%%%%
% subject = 'HVO';
% session = '20Feb2015_Zipser_Pilots_HVO';
% fsl_subfolder = '20Feb2015_mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     '20150220_082727mbboldmb820mmAPPSNs004a001' ...
%     '20150220_082727mbboldmb820mmAPPSNs006a001' ...
%     '20150220_082727mbboldmb820mmAPPSNs008a001'};
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% year = 2015;
% month = 2;
% subject = 'DR';
% session = '19Feb2015_Zipser_Pilots_DR_testing_32ch_for_TMS_use';
% fsl_subfolder = '19Feb2015_4mm_smoothing';
% feat_folders = {... % do not use .feat extension
%     '20150219_173025mbboldmb620mmAPPSNs004a001' ...
%     '20150219_173025mbboldmb620mmAPPSNs006a001'};
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% year = 2015;
% month = 1;
% subject = 'HVO';
% session = '18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO';
% fsl_subfolder = '18Feb2015_mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     '20150118_164630mbboldmb615mmAPPSNs003a001' ...
%     '20150118_164630mbboldmb615mmAPPSNs005a001' ...
%     '20150118_164630mbboldmb615mmAPPSNs007a001'};
% session = '22Jan2015_MB_Zipser_Pilot_13Nov2014_HVO';
% fsl_subfolder = '18Feb2015_mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     '20150122_144129mbboldmb615mmAPPSNs003a001' ...
%     '20150122_144129mbboldmb615mmAPPSNs005a001' ...
%     '20150122_144129mbboldmb615mmAPPSNs007a001'};
% session = '25Jan2015_MB_Zipser_Pilot_13Nov2014_HVO';
% fsl_subfolder = '18Feb2015_mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     '20150125_124420mbboldmb615mmAPPSNs005a001' ...
%     '20150125_124420mbboldmb615mmAPPSNs007a001' ...
%     '20150125_124420mbboldmb615mmAPPSNs009a001'};
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% year = 2015;
% month = 2;
%%%%%%%%%%%%%%%%%%%%%
% subject = 'HVO';
% session = '18Feb2015_Zipser_Pilots_HVO';
% fsl_subfolder = '18Feb2015_mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     '20150218_081721mbboldmb620mmAPPSNs004a001' ...
%     '20150218_081721mbboldmb620mmAPPSNs006a001' ...
%     '20150218_081721mbboldmb620mmAPPSNs008a001' ...
%     '20150218_081721mbboldmb620mmAPPSNs010a001' ...
%     '20150218_081721mbboldmb820mmAPPSNs012a001'};
%%%%%%%%%%%%%%%%%%%%%
% subject = 'HVO';
% session = '12Feb2015_Zipser_Pilots_HVO';
% fsl_subfolder = '16Feb2015_mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     '20150212_081609mbboldmb620mmAPPSNs006a001' ...
%     '20150212_081609mbboldmb620mmAPPSNs008a001' ...
%     '20150212_081609mbboldmb620mmAPPSNs010a001'};
% session = '14Feb2015_Zipser_Pilots_HVO';
% fsl_subfolder = '16Feb2015_mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     '20150214_082112mbboldmb620mmAPPSNs006a001' ...
%     '20150214_082112mbboldmb620mmAPPSNs008a001' ...
%     '20150214_082112mbboldmb620mmAPPSNs010a001'};
%%%%%%%%%%%%%%%%%%%%%
% subject = 'HVO';
% session = '16Feb2015_Zipser_Pilots_HVO';
% fsl_subfolder = '16Feb2015_mc_to_006a_of_9Feb2015';
% feat_folders = {... % do not use .feat extension
%     '20150216_082043mbboldmb620mmAPPSNs005a001' ...
%     '20150216_082043mbboldmb620mmAPPSNs009a001' ...
%     '20150216_082043mbboldmb620mmAPPSNs011a001' ...
%     '20150216_082043mbboldmb620mmAPPSNs013a001' ...
%     '20150216_082043mbboldmb620mmAPPSNs019a001' ...
%     '20150216_082043mbboldmb620mmAPPSNs021a001' ...
%     '20150216_082043mbboldmb620mmAPPSNs025a001'};
%%%%%%%%%%%%%%%%%%%%%
% subject = 'HVO';
% session = '14Feb2015_Zipser_Pilots_HVO';
% fsl_subfolder = '14Feb2015';
% %feat_folders = {'20150214_082112mbboldmb620mmAPPSNs006a001' '20150214_082112mbboldmb620mmAPPSNs008a001' '20150214_082112mbboldmb620mmAPPSNs010a001 20150214_082112mbboldmb620mmAPPSNs012a001'}; % don not use .feat extension
% feat_folders = {'20150214_082112mbboldmb620mmAPPSNs012a001'}; % do not use .feat extension
%%%%%%%%%%%%%%%%%%%%%
%subject = 'HVO';
%session = '12Feb2015_Zipser_Pilots_HVO';
%fsl_subfolder = '12Feb2015';
%%feat_folders = {'20150212_081609mbboldmb620mmAPPSNs010a001'}; % don not use .feat extension
%feat_folders = {'20150212_081609mbboldmb620mmAPPSNs006a001' '20150212_081609mbboldmb620mmAPPSNs008a001' '20150212_081609mbboldmb620mmAPPSNs010a001.feat'}; % don not use .feat extension
%%%%%%%%%%%%%%%%%%%%%
% subject = 'HVO';
% session = '9Feb2015_Zipser_Pilots_HVO';
% fsl_subfolder = '9Feb2015';
% feat_folders = {'20150209_081421mbboldmb620mmAPPSNs013a001'}; % do not use .feat extension
%%%%%%%%%%%%%%%%%%%%%
% subject = 'CW';
% session = '7Feb2015_Zipser_Pilots_CW';
% fsl_subfolder = '7Feb2015';
% feat_folder = '20150207_091449mbboldmb620mmAPPSNs014a001';
%%%%%%%%%%%%%%%%%%%%%
% subject = 'HVO';
% session = '6Feb2015_Zipser_Pilots_HVO';
% fsl_subfolder = '6Feb2015';
% feat_folder = '20150206_081657mbboldmb615mmPSNs010a001';
%%%%%%%%%%%%%%%%%%%%
% session = '3Feb2015_Zipser_Pilots_HVO';
% fsl_subfolder = '3Feb2015_Partial_brain_motion_corrected_to_run_006a';
% feat_folder = '20150203_082706mbboldmb615mmPartialPSNs008a001';
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% action %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for i = 1:length(feat_folders)
    feat_folder = feat_folders{i};
    session_path = d2s({'~/Data/subjects/' subject '/' year '/' month '/' session});
    feat_partial_path = d2s({session_path '/fsl/' fsl_subfolder '/' feat_folder});
    clear filtered_func_data;
    if not(exist('filtered_func_data'))
        nii_path = [feat_partial_path '.feat/filtered_func_data.nii.gz'];
        fps(['Loading ' nii_path]);
        filtered_func_data = load_untouch_nii(nii_path);
        z_scored_filtered_func_data = z_score_4D_nii(filtered_func_data);
        eval(['z_scored_' feat_folder ' = z_scored_filtered_func_data;']);
        save( [feat_partial_path '.z_scored_filtered_func_data.mat' ], ['z_scored_' feat_folder]);
        %save( [feat_partial_path '.z_scored_filtered_func_data.mat' ], 'z_scored_filtered_func_data');
        % prior to 19 Feb 2015
    end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

