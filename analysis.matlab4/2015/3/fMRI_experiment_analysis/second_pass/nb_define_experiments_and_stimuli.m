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
%cd ~/Google' Drive'/analysis.matlab4/2015/2/fMRI_experiment_analysis/second_pass/

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;

	%experiment(LOCALIZER2).runs(1).z_scored_datafile_name = '';
	%HVO = G.constants.HVO;

	path_Data = '~/Desktop/Data';
	z_path = d2s({path_Data '/' 'subjects' '/' 'HVO' '/'  2015 '/'  2 '/' '9Feb2015_Zipser_Pilots_HVO' '/' 'fsl' '/' '9Feb2015'});
	d = dir([z_path '/' '*.z_scored_filtered_func_data.mat']);
	for i = 1:length(d)
		f = strrep(d(i).name, '.z_scored_filtered_func_data.mat', '');
		clear('z_scored_filtered_func_data');
		clear(['z_scored_' f]);
		load([z_path '/' d(i).name]);
		if exist('z_scored_filtered_func_data')
			%'z_scored_filtered_func_data exists'
			eval(['z_scored_' f ' = z_scored_filtered_func_data;']);
			clear('z_scored_filtered_func_data');
		else
			if not(exist(['z_scored_' f]))
				error('');
			end
		end
		%fps(f);
	end
end


if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
	clear session;
	session.subject = 'HVO';
	session.subject_code = 'S1_2015';
	session.year = 2015;
	session.month = 2;
	session.day = 20;
	session.time_slot = [7 9]
	session.folder = '20Feb2015_Zipser_Pilots_HVO';
	session.log_folder = '20Feb2015 scanning HVO (S1_2015)';
	session.log_file = '20Feb2015 BIC HVO (S1_2015) scanning.trf'
	session.room_lights_left_on = true;
	session.RF_32ch_coil_front_and_back = true;
	session.back_of_32ch_coil_mirror_stand_to_screen_inches = 12.75;
	session.distance_from_bottom_of_screen_inches = 2.75;
	session.screen_width_inches = 8.75;
	session.EyeLinkUsed = true;
	session.AAHScout = true;
	session.comments = 'Hanneke was supposed to attend to the faces, but she told me that she was paying attention to what seemed salient.';

	clear runn;
	runn.number = 2;
	runn.approximate_time = [8 29];
	runn.protocol = 'mb_bold_mb8_20mm_AP_PSN';
	runn.video = 'vermeer1to10.avi';
	runn.script = 'movie_fMRI_et_14Feb2015_Vermeer1_EL.m';
	runn.EyeLink_file = 'et_data.20150220_0833.edf';
	runn.nifti_file = '20150220_082727mbboldmb820mmAPPSNs004a001.nii.gz';
	runn.fsl.feat_folder = '20150220_082727mbboldmb820mmAPPSNs004a001.feat';
	runn.fsl.high_frequency_cutoff_Hz = 50;
	runn.fsl.analysis_folder = '20Feb2015_mc_to_006a_of_9Feb2015';
	runn.fsl.z_scored_filtered_func_data = ...
		 '20150220_082727mbboldmb820mmAPPSNs004a001.z_scored_filtered_func_data.mat';
	runn.comments = '';
	session.runs(runn.number) = runn;

	clear runn;
	runn.number = 3;
	runn.approximate_time = [8 34];
	runn.protocol = 'mb_bold_mb8_20mm_AP_PSN';
	runn.video = 'vermeer1to10.avi';
	runn.script = 'movie_fMRI_et_14Feb2015_Vermeer1_EL.m';
	runn.EyeLink_file = 'et_data.20150220_0840.edf';
	runn.nifti_file = '20150220_082727mbboldmb820mmAPPSNs006a001.nii.gz';
	runn.fsl.analysis_folder = '20Feb2015_mc_to_006a_of_9Feb2015';
	runn.fsl.feat_folder = '20150220_082727mbboldmb820mmAPPSNs006a001.feat';
	runn.fsl.high_frequency_cutoff_Hz = 50;
	runn.fsl.z_scored_filtered_func_data = ...
		 '20150220_082727mbboldmb820mmAPPSNs006a001.z_scored_filtered_func_data.mat';
	runn.comments = '';
	session.runs(runn.number) = runn;

	clear runn;
	runn.number = 4;
	runn.approximate_time = [8 40];
	runn.protocol = 'mb_bold_mb8_20mm_AP_PSN';
	runn.video = 'vermeer1to10.avi';
	runn.script = 'movie_fMRI_et_14Feb2015_Vermeer1_EL.m';
	runn.EyeLink_file = 'et_data.20150220_0846.edf';
	runn.nifti_file = '20150220_082727mbboldmb820mmAPPSNs008a001.nii.gz';
	runn.fsl.analysis_folder = '20Feb2015_mc_to_006a_of_9Feb2015';
	runn.fsl.feat_folder = '20150220_082727mbboldmb820mmAPPSNs008a001.feat';
	runn.fsl.high_frequency_cutoff_Hz = 50;
	runn.fsl.z_scored_filtered_func_data = ...
		 '20150220_082727mbboldmb820mmAPPSNs008a001.z_scored_filtered_func_data.mat';
	runn.comments = '';
	session.runs(runn.number) = runn;

	clear runn;
end
