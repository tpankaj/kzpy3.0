clc
clear folders_to_rsync;
clear folders_to_backup;
clear dest_Volume;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%% SPECIFIY WHAT TO DO %%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%folders_to_rsync = {'~/Google\ Drive/analysis.matlab4'};
folders_to_rsync = {'~/Desktop/fMRI_top_node', '~/Google\ Drive', '~/Desktop/Data'};
%folders_to_rsync = {'/Volumes/Karl\ Zipser\ fMRI2/External_Desktop/fMRI_top_node', '/Volumes/Karl\ Zipser\ fMRI2/External_Desktop/Google\ Drive', '/Volumes/Karl\ Zipser\ fMRI2/External_Desktop/Data'};
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
folders_to_backup = {'~/Google\ Drive/analysis.matlab4'};
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%dest_Volume = '/Volumes/Karl\ Zipser\ fMRI2/External_Desktop';
%dest_Volume = '/Volumes/25Oct2014_BKP1/External_Desktop';
%dest_Volume = '/Volumes/Time\ Machine\ Backups/External_Desktop';
%dest_Volume = '/Volumes/25Oct2014_BKP2/External_Desktop';
dest_Volume = '/Volumes/26Oct2014/External_Desktop';
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%% END SPECIFIY WHAT TO DO %%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%% DO IT %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for i = 1:length(folders_to_rsync)
    system(['rsync -rav --exclude Data_Google_Drive/ ' folders_to_rsync{i} ' ' dest_Volume])
end

dt = datestr(now,'dd_mmmm_yyyy_HH_MM_AM');
for i = 1:length(folders_to_backup)
    system(['rsync -rav ' folders_to_backup{i} ' ' dest_Volume '/dated_backups/' num2str(now) ])
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% rsync -rav ~/Desktop/Data/subjects/ ~/Google\ Drive/Data_Google_Drive/subjects
% rsync -rav ~/Desktop/Data/fmri_scanning_experiments/ ~/Google\ Drive/Data_Google_Drive/fmri_scanning_experiments