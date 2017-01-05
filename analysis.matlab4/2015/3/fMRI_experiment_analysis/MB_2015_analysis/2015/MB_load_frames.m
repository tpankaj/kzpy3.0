function frames = MB_load_frames(experiment_folder, experiment_subfolder)
% function runs = MB_load_frames(experiment_folder, experiment_subfolder)
%
	experiment_subfolder_path = d2s({'~/Data/experiments/' experiment_folder '/' experiment_subfolder});
	load(d2s({experiment_subfolder_path '/frames.mat'}));

end

