


if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if not(exist('RF_mapping'))
        fps('*** loading ~/Desktop/Matlab_Desktop/HVO_RF_mapping.736252.5459.mat');
        load('~/2015/10/2015-10/HVO_RF_mapping.736252.5459.mat');
        RF_mapping = HVO_RF_mapping;
    end
end




if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if not(exist('the_frames'))
        for s = 1:6 % attending
            stimuli(s).on_frames = 30 + (1+(s-1)*30):(30*6*2):1470;
            stimuli(s).durations = 0*stimuli(s).on_frames + 19;
        end
        for s = 7:12 % reading
            stimuli(s).on_frames = 30 + 180 + (1+(s-1-6)*30):(30*6*2):1470;
            stimuli(s).durations = 0*stimuli(s).on_frames + 19;
        end
    end
end


tasks = {%'attend_face_or_read',
    %'attend_vase_or_read',
    %'attend_vase_or_face',
    %'attend_object_or_body',
    %'fixate_vase_or_face',
    %'saccade_from_vase_or_face',
    'attend_gnd_near_vase_or_face',
    'fixate_or_read',
    'attend_scene_or_face'}

e = 'vermeer_attention';
subject = 'HVO';
for t = 1:length(tasks)
    ee = tasks{t}
    mkdir(d2s({'~/Desktop/',ee}))
    if not(exist(ee))
        eval(d2s({ee ' = MB_get_MB_experiment(''' e ''', ''' ee ''', ''' subject ''');'}));
    end
    for RUN_NUM = 1:eval(d2s({'length(' ee '.runs)'}))

        eval(d2s({ee '_resampled_data = tseriesinterp_selected_voxels(' ee '.runs(' RUN_NUM ').z_scored_filtered_func_data.z_img, RF_mapping.selected_voxel_xyzs, ' ee '.runs(1).TR, 5 );'}));
%                eval(d2s({ee '_resampled_data = tseriesinterp_selected_voxels(' ee '.runs_avg, RF_mapping.selected_voxel_xyzs, ' ee '.runs(1).TR, 5 );'}));

        eval(d2s({'resampled_data  = ' ee '_resampled_data;'}));
        offset = 4 * 5;
        p_images.experiment = e;
        p_images.experiment_subtype = ee;
        p_images.imgs = [];
        for s = [1 7 2 8 3 9 4 10 5 11 6 12]
            data_frames = [];
            for p = 1:4 % p = 1:2 % TEMP!!!!, was p=1:4, change on 14June2015 for surface attention viewing. p=1:4 is for vermeer stuff
                data_frames = [data_frames (stimuli(s).on_frames(p)):(stimuli(s).on_frames(p)-1+stimuli(s).durations(p))];%!!!!!
            end

            data = resampled_data(:,(data_frames+offset));
            mean_data = mean(data,2); %- gray_data;%!!!!!!!!!!!!!!!!!!
            fig_num = p;

            if s > 6
                fig_num = p+100;
            end

            img = MB_display_resampled_data_and_frames(mean_data, 0, RF_mapping.pixel_to_voxel_assignment, fig_num );
            p_images.imgs(s).img = img;
            img = img - min(min(img))
            img = img / max(max(img))
            imwrite(img,d2s({'~/Desktop/',ee,'/',s,'.',RUN_NUM,'.png'}))
        end
    end
end

















