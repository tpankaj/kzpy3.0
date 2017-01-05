% local_startup.m for analysis.matlab4
% 10 December 2014
% Run this script manually at the beginning of the session.
% to run matlab from terminal: /Applications/MATLAB_R2014b.app/bin/matlab 


'%%%%%%%%%%%% local_startup.m %%%%%%%%%%%%'
pwd

addpath(genpath(pwd));

% addpath(pwd);

% addpath([pwd,'/my_lib']);
% addpath([pwd,'/my_lib/eval_struct']);
% addpath([pwd,'/my_lib/my_adjust_matrix_lib']); 
% addpath([pwd,'/my_lib/my_image_lib']); 
% addpath([pwd,'/my_lib/my_video_lib']); 
% addpath([pwd,'/my_lib/my_image_lib/image_figure']); 
% addpath([pwd,'/my_lib/my_shortcut_lib']); 
% addpath([pwd,'/my_lib/my_fMRI_lib']); 
% addpath([pwd,'/my_lib/gaussian']); 
% addpath([pwd,'/my_lib/3rd_party']);
% addpath([pwd,'/my_lib/3rd_party/stefslon-exportToPPTX-568f04f']);
% addpath([pwd,'/my_lib/3rd_party/NIfTI_20140122']);
% addpath([pwd,'/my_lib/3rd_party/GLMdenoise-1.4']);
% addpath([pwd,'/my_lib/3rd_party/GLMdenoise-1.4/utilities']);
% addpath([pwd,'/my_lib/3rd_party/analyzePRF-1.1']);
% addpath([pwd,'/my_lib/3rd_party/analyzePRF-1.1/utilities']);
% addpath(genpath([pwd,'/my_lib/3rd_party/knkutils']));
% addpath([pwd,'/my_lib/3rd_party/edfmex']);

% addpath([pwd,'/Kay_2008_analysis']);
% addpath([pwd,'/literature']);
% addpath([pwd,'/fMRI_experiment_analysis/MB_2015_analysis']);
% addpath([pwd,'/fMRI_experiment_analysis/MB_2015_analysis/2015/3']);
% addpath([pwd,'/functional_voxel_mapping']);
% addpath([pwd,'/grant_models']);


LOCAL_STARTUP = true;

run G_initalize;

