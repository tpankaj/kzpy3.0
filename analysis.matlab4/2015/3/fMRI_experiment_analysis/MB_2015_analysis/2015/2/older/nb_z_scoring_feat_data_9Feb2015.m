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
year = 2015;
month = 2;
%%%%%%%%%%%%%%%%%%%%%
subject = 'HVO';
session = '18Feb2015_Zipser_Pilots_HVO';
fsl_subfolder = '18Feb2015_mc_to_006a_of_9Feb2015';
feat_folders = {... % do not use .feat extension
    '20150218_081721mbboldmb620mmAPPSNs004a001' ...
    '20150218_081721mbboldmb620mmAPPSNs006a001' ...
    '20150218_081721mbboldmb620mmAPPSNs008a001' ...
    '20150218_081721mbboldmb620mmAPPSNs010a001' ...
    '20150218_081721mbboldmb820mmAPPSNs012a001'};
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
    session_path = d2s({'~/Desktop/Data/subjects/' subject '/' year '/' month '/' session});
    feat_partial_path = d2s({session_path '/fsl/' fsl_subfolder '/' feat_folder});
    clear filtered_func_data;
    if not(exist('filtered_func_data'))
        nii_path = [feat_partial_path '.feat/filtered_func_data.nii.gz'];
        fps(['Loading ' nii_path]);
        filtered_func_data = load_untouch_nii(nii_path);
        z_scored_filtered_func_data = z_score_4D_nii(filtered_func_data);
        eval(['z_scored_' feat_folder ' = z_scored_filtered_func_data;']);
        save( [feat_partial_path '.z_scored_filtered_func_data.mat' ], 'z_scored_filtered_func_data');
    end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

