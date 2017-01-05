%system('rsync -rav ~/Desktop/Data/subjects/ ~/Google\ Drive/Data_Google_Drive/subjects');
%system('rsync -rav ~/Desktop/Data/fmri_scanning_experiments/ ~/Google\ Drive/Data_Google_Drive/fmri_scanning_experiments');


rsync -P -rav --exclude 'Icon*' --exclude 'analysis' --exclude 'experiments' --exclude 'freesurfer' --exclude 'osx' --exclude 'stimuli' --exclude '_blank_scan' --exclude 'AK' --exclude 'AV' --exclude 'CW' --exclude 'DR' --exclude 'KW' --exclude 'KZ' --exclude 'Phantom' --exclude 'SK' --exclude 'TN' --exclude 'dcm' --exclude 'edf' --exclude 'fsl' --exclude 'info' --exclude 'log' --exclude 'mat' --exclude '*.nii.gz' --exclude 'runs' ~/Data/ ~/Desktop/karlzipser/