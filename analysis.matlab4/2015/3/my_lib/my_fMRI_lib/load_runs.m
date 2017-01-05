function runs = load_runs(experiment_folder, experiment_subfolder, subject)

	clc
	run_num = 0;
	subject_folder = d2s({'~/Data/experiments/' experiment_folder '/' experiment_subfolder '/subjects/' subject});
	year_dirs = ddir(subject_folder);% '/' year '/' month '/' day '/runs/'});
	for i = 1:length(year_dirs)
		year = str2num(year_dirs(i).name)
		month_dirs = ddir(d2s({subject_folder '/' year}));
		for j = 1:length(month_dirs)
			month = str2num(month_dirs(j).name)
			day_dirs = ddir(d2s({subject_folder '/' year '/' month}));
			for k = 1:length(day_dirs)
				day = str2num(day_dirs(k).name)
				run_dirs = ddir(d2s({subject_folder '/' year '/' month '/' day '/runs'}));
				for l = 1:length(run_dirs)
					runn = str2num(run_dirs(l).name);
					z_temp = ddir(d2s({subject_folder '/' year '/' month '/' day '/runs/' runn '/*.z_scored_filtered_func_data.mat'}));
					if length(z_temp) ~= 1
						error('if length(z_temp) ~= 1');
					end
					nii_root_name = z_temp.name;
					nii_root_name = strsplit(nii_root_name,'.');
					nii_root_name = nii_root_name{1};
					clear('z_scored_filtered_func_data');
					z_scored_filename = d2s({subject_folder '/' year '/' month '/' day '/runs/' runn '/' nii_root_name '.z_scored_filtered_func_data.mat'});
					fps(['*** Loading ' z_scored_filename]);
					load(d2s({z_scored_filename}));
					if not(exist('z_scored_filtered_func_data'))
						% In some files, that data is stored as z_scored_filtered_func_data, in others as z_scored_ + nii_root_name.
						eval(['z_scored_filtered_func_data  = z_scored_' nii_root_name ';']);
					end

					dirstr_of_mat = d2s({subject_folder '/' year '/' month '/' day '/runs/' runn '/movie_run*.mat'});
					m_temp = ddir(dirstr_of_mat);
					if length(m_temp) < 1
						fps(['*** Warning, move_run...mat not found for ' dirstr_of_mat]);
						moviename = [];
						my_pause;
					elseif length(m_temp) == 1
						mat_name = m_temp.name;
						mat_name = d2s({subject_folder '/' year '/' month '/' day '/runs/' runn '/' mat_name});
						clear('moviename');
						fps(['*** Loading ' mat_name]);
						load(mat_name);
						moviename = strsplit(moviename,'/');
						moviename = moviename{length(moviename)};
					else
						error('if length(m_temp) ~= 1');
					end

					fps(moviename)

					run_num = run_num + 1;
					runs(run_num).nii_root_name = nii_root_name;
					runs(run_num).moviename = moviename;
					runs(run_num).z_scored_filtered_func_data = z_scored_filtered_func_data;
				end
			end
		end
	end
end

