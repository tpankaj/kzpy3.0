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


if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    if not(exist('frames'))
        N = 500;
%        frame_path = '~/Desktop/Data/fmri_scanning_experiments/2015/2/5Feb2015_localizer2/localizer2_orientation_5Feb2015.736000.8698/localizer2_orientation_5Feb2015_frames';
        frame_path = '~/Desktop/Data/fmri_scanning_experiments/2015/2/5Feb2015_localizer2/localizer2_eccentricity_5Feb2015.736000.8919/localizer2_eccentricity_5Feb2015_frames';
        f = imread(d2s({frame_path '/' 1 '.png'}));
        f_size = size(f);
        min_dim = min(f_size(1:2));
        max_dim = max(f_size(1:2));
        frames = zeros(N,max_dim,max_dim,3,'uint8');
        min_start = (max_dim-min_dim)/2;
        min_end = max_dim - min_start - 1;
        [min_dim max_dim min_start min_end]
        
        for i = 1:N
            f = imread(d2s({frame_path '/' i '.png'}));
            f_size = size(f);            
            frames(i,min_start:min_end,:,:) = f;
        end
    end
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 2;
    if not(exist('texture_energy_images'))
        grayscale_frames = sum(single(frames),4);
        texture_energy_images = make_high_pass_version_of_image_general(grayscale_frames,6,false);
    end
end

if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 2;
    size_frames = size(frames);
    for i = 50:(size_frames(1)-9)
        mi(frames(i,:,:,:),1,[1,3,1]);
        mi(grayscale_frames(i,:,:),1,[1,3,2]);
        mi(texture_energy_images(i,:,:),1,[1,3,3]);
%         mi(sum(texture_energy_images((i-4):(i+8),:,:),1) - 13*texture_energy_images(1,:,:),1,[1,3,3]);
        pause(1/5);
    end
end

