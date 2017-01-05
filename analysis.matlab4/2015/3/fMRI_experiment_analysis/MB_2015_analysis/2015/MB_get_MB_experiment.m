function MB_experiment = MB_get_MB_experiment(experiment_folder, experiment_subfolder, subject, runs_to_average, runs)
% function MB_experiment = MB_get_runs_average(experiment_folder, experiment_subfolder, subject, runs_to_average, runs)
%       
    if nargin < 5
        runs = MB_load_runs(experiment_folder,experiment_subfolder,subject);
    end
    if nargin < 4
        runs_to_average = 1:length(runs);
    end
    runs_avg = 0 * runs(runs_to_average(1)).z_scored_filtered_func_data.z_img;
    runs_even = 0 * runs(runs_to_average(1)).z_scored_filtered_func_data.z_img;
    runs_odd = 0 * runs(runs_to_average(1)).z_scored_filtered_func_data.z_img;
    num_even_runs = 0;
    num_odd_runs = 0;
    for i = 1:length(runs_to_average)
        r = runs_to_average(i);
        size(runs(r).z_scored_filtered_func_data.z_img)
        runs_avg = runs_avg + runs(r).z_scored_filtered_func_data.z_img;
        if iseven(r)
            num_even_runs = num_even_runs + 1;
            runs_even = runs_even + runs(r).z_scored_filtered_func_data.z_img;
        else
            num_odd_runs = num_odd_runs + 1;
            runs_odd = runs_odd + runs(r).z_scored_filtered_func_data.z_img;
        end
    end
    runs_avg = runs_avg / length(runs_to_average);
    runs_averaged = runs_to_average;
    runs_even = runs_even / num_even_runs;
    runs_odd = runs_odd / num_odd_runs;
    zc_sum = squeeze(sum(runs_even.*runs_odd,4));

    MB_experiment.runs = runs;
    MB_experiment.experiment_folder = experiment_folder;
    MB_experiment.experiment_subfolder = experiment_subfolder;
    MB_experiment.subject = subject;
    MB_experiment.runs_to_average = runs_to_average;
    MB_experiment.runs_avg = runs_avg;
    MB_experiment.zc_sum = zc_sum;

end