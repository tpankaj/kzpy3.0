
if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if not(exist('RF_mapping'))
        fps('*** loading /Users/davidzipser/Desktop/Matlab_Desktop/HVO_RF_mapping.736027.5901.mat');
        load('/Users/davidzipser/Desktop/Matlab_Desktop/HVO_RF_mapping.736027.5901.mat');
        RF_mapping = HVO_RF_mapping;
    end
end
% if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%     %ori_MB_experiment = MB_get_MB_experiment('localizer2', 'orientation', 'HVO', 1:6);
%     %ecc_MB_experiment = MB_get_MB_experiment('localizer2', 'eccentricity', 'HVO', 1:6);
%     %ver_MB_experiment = MB_get_MB_experiment('vermeer_attend_face_or_read_letters', 'vermeer1to10', 'HVO', [21:23]);%, ver_MB_experiment.runs);%1:9
%     attend_face_or_read = MB_get_MB_experiment('vermeer_attention', 'attend_face_or_read', 'HVO', [1:9]);
%     %mi_nii(ori_MB_experiment.zc_sum,50,50,20,101,false)
%     %mi_nii(ecc_MB_experiment.zc_sum,50,50,20,102,false)
%     %mi_nii(ori_MB_experiment.zc_sum,50,50,20,103,false)
%     %mi_nii(ori_MB_experiment.zc_sum+ecc_MB_experiment.zc_sum+ver_MB_experiment.zc_sum,50,50,20,104,false)
% end
% if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%     %attend_face_or_read = MB_get_MB_experiment('vermeer_attention', 'attend_face_or_read', 'HVO', [1:9]);
%     %attend_vase_or_read = MB_get_MB_experiment('vermeer_attention', 'attend_vase_or_read', 'HVO', [1:4]);
%     %attend_vase_or_face = MB_get_MB_experiment('vermeer_attention', 'attend_vase_or_face', 'HVO', [1:7]);
%     attend_object_or_body = MB_get_MB_experiment('vermeer_attention', 'attend_object_or_body', 'HVO', [1:3]);
% end

% if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%     %attend_face_or_read_resampled_data = tseriesinterp_selected_voxels(attend_face_or_read.runs_avg, RF_mapping.selected_voxel_xyzs, attend_face_or_read.runs(1).TR, 5 );
%     %attend_vase_or_read_resampled_data = tseriesinterp_selected_voxels(attend_vase_or_read.runs_avg, RF_mapping.selected_voxel_xyzs, attend_vase_or_read.runs(1).TR, 5 );
%     attend_vase_or_face_resampled_data = tseriesinterp_selected_voxels(attend_vase_or_face.runs_avg, RF_mapping.selected_voxel_xyzs, attend_vase_or_face.runs(1).TR, 5 );
%     attend_object_or_body_resampled_data = tseriesinterp_selected_voxels(attend_object_or_body.runs_avg, RF_mapping.selected_voxel_xyzs, attend_object_or_body.runs(1).TR, 5 );

%     %ori_resampled_data = tseriesinterp_selected_voxels(ori_MB_experiment.runs_avg, RF_mapping.selected_voxel_xyzs, ori_MB_experiment.runs(1).TR, 5 );
%     %ecc_resampled_data = tseriesinterp_selected_voxels(ecc_MB_experiment.runs_avg, RF_mapping.selected_voxel_xyzs, ecc_MB_experiment.runs(1).TR, 5 );
% end




if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    s = 'HVO';
    if 0
        e = 'vermeer_attention';
        if 0
            ee = 'attend_face_or_read';
            if not(exist(ee))
                eval(d2s({ee ' = MB_get_MB_experiment(''' e ''', ''' ee ''', ''' s ''');'}));
                eval(d2s({ee '_resampled_data = tseriesinterp_selected_voxels(' ee '.runs_avg, RF_mapping.selected_voxel_xyzs, ' ee '.runs(1).TR, 5 );'}));
            end
        end
        if 0
            ee = 'attend_vase_or_read';
            if not(exist(ee))
                eval(d2s({ee ' = MB_get_MB_experiment(''' e ''', ''' ee ''', ''' s ''');'}));
                eval(d2s({ee '_resampled_data = tseriesinterp_selected_voxels(' ee '.runs_avg, RF_mapping.selected_voxel_xyzs, ' ee '.runs(1).TR, 5 );'}));
            end
        end
        if 0
            ee = 'attend_vase_or_face';
            if not(exist(ee))
                eval(d2s({ee ' = MB_get_MB_experiment(''' e ''', ''' ee ''', ''' s ''');'}));
                eval(d2s({ee '_resampled_data = tseriesinterp_selected_voxels(' ee '.runs_avg, RF_mapping.selected_voxel_xyzs, ' ee '.runs(1).TR, 5 );'}));
            end
        end
        if 0
            ee = 'attend_object_or_body';
            if not(exist(ee))
                eval(d2s({ee ' = MB_get_MB_experiment(''' e ''', ''' ee ''', ''' s ''');'}));
                eval(d2s({ee '_resampled_data = tseriesinterp_selected_voxels(' ee '.runs_avg, RF_mapping.selected_voxel_xyzs, ' ee '.runs(1).TR, 5 );'}));
            end
        end
        if 0
            ee = 'fixate_vase_or_face';
            if not(exist(ee))
                eval(d2s({ee ' = MB_get_MB_experiment(''' e ''', ''' ee ''', ''' s ''');'}));
                eval(d2s({ee '_resampled_data = tseriesinterp_selected_voxels(' ee '.runs_avg, RF_mapping.selected_voxel_xyzs, ' ee '.runs(1).TR, 5 );'}));
            end
        end
        if 0
            ee = 'saccade_from_vase_or_face';
            if not(exist(ee))
                eval(d2s({ee ' = MB_get_MB_experiment(''' e ''', ''' ee ''', ''' s ''');'}));
                eval(d2s({ee '_resampled_data = tseriesinterp_selected_voxels(' ee '.runs_avg, RF_mapping.selected_voxel_xyzs, ' ee '.runs(1).TR, 5 );'}));
            end
        end
        if 0
            ee = 'attend_gnd_near_vase_or_face';
            if not(exist(ee))
                eval(d2s({ee ' = MB_get_MB_experiment(''' e ''', ''' ee ''', ''' s ''');'}));
                eval(d2s({ee '_resampled_data = tseriesinterp_selected_voxels(' ee '.runs_avg, RF_mapping.selected_voxel_xyzs, ' ee '.runs(1).TR, 5 );'}));
            end
        end
        if 0
            ee = 'fixate_or_read';
            if not(exist(ee))
                eval(d2s({ee ' = MB_get_MB_experiment(''' e ''', ''' ee ''', ''' s ''');'}));
                eval(d2s({ee '_resampled_data = tseriesinterp_selected_voxels(' ee '.runs_avg, RF_mapping.selected_voxel_xyzs, ' ee '.runs(1).TR, 5 );'}));
            end
        end
        if 0
            ee = 'attend_scene_or_face';
            if not(exist(ee))
                eval(d2s({ee ' = MB_get_MB_experiment(''' e ''', ''' ee ''', ''' s ''');'}));
                eval(d2s({ee '_resampled_data = tseriesinterp_selected_voxels(' ee '.runs_avg, RF_mapping.selected_voxel_xyzs, ' ee '.runs(1).TR, 5 );'}));
            end
        end
    end
    if 0
        e = 'BarryLyndon';
        ee = 'attend_person_not_BL_BarryLyndon_16Jan2015_1';
        if not(exist(ee))
            eval(d2s({ee ' = MB_get_MB_experiment(''' e ''', ''' ee ''', ''' s ''');'}));
            eval(d2s({ee '_resampled_data = tseriesinterp_selected_voxels(' ee '.runs_avg, RF_mapping.selected_voxel_xyzs, ' ee '.runs(1).TR, 5 );'}));
        end

            % ee = 'fixate_BarryLyndon_16Jan2015_1';
            % if not(exist(ee))
            %     eval(d2s({ee ' = MB_get_MB_experiment(''' e ''', ''' ee ''', ''' s ''');'}));
            %     eval(d2s({ee '_resampled_data = tseriesinterp_selected_voxels(' ee '.runs_avg, RF_mapping.selected_voxel_xyzs, ' ee '.runs(1).TR, 5 );'}));
            % end
            % ee = 'fixate_BarryLyndon_16Jan2015_2';
            % if not(exist(ee))
            %     eval(d2s({ee ' = MB_get_MB_experiment(''' e ''', ''' ee ''', ''' s ''');'}));
            %     eval(d2s({ee '_resampled_data = tseriesinterp_selected_voxels(' ee '.runs_avg, RF_mapping.selected_voxel_xyzs, ' ee '.runs(1).TR, 5 );'}));
            % end
            % ee = 'fixate_BarryLyndon_16Jan2015_3';
            % if not(exist(ee))
            %     eval(d2s({ee ' = MB_get_MB_experiment(''' e ''', ''' ee ''', ''' s ''');'}));
            %     eval(d2s({ee '_resampled_data = tseriesinterp_selected_voxels(' ee '.runs_avg, RF_mapping.selected_voxel_xyzs, ' ee '.runs(1).TR, 5 );'}));
            % end
    end
    if 0
        e = 'BarryLyndon';
        ee = 'attend_scene_BarryLyndon_16Jan2015_1';
        if not(exist(ee))
            eval(d2s({ee ' = MB_get_MB_experiment(''' e ''', ''' ee ''', ''' s ''');'}));
            eval(d2s({ee '_resampled_data = tseriesinterp_selected_voxels(' ee '.runs_avg, RF_mapping.selected_voxel_xyzs, ' ee '.runs(1).TR, 5 );'}));
        end
    end
    if 0
        e = 'surface_attention_13June2015';
        ee = 'attend_x';
        if not(exist(ee))
            eval(d2s({ee ' = MB_get_MB_experiment(''' e ''', ''' ee ''', ''' s ''');'}));
            eval(d2s({ee '_resampled_data = tseriesinterp_selected_voxels(' ee '.runs_avg, RF_mapping.selected_voxel_xyzs, ' ee '.runs(1).TR, 5 );'}));
        end
    end
    if 1
        e = 'surface_attention_13June2015';
        ee = 'attend_opposite_x';
        if not(exist(ee))
            eval(d2s({ee ' = MB_get_MB_experiment(''' e ''', ''' ee ''', ''' s ''');'}));
            eval(d2s({ee '_resampled_data = tseriesinterp_selected_voxels(' ee '.runs_avg, RF_mapping.selected_voxel_xyzs, ' ee '.runs(1).TR, 5 );'}));
        end
    end
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%








if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if not(exist('ver_frames'))
        % ori_frames = MB_load_frames('localizer2','orientation');
        % ecc_frames = MB_load_frames('localizer2','eccentricity');
        ver_frames = MB_load_frames('vermeer_attention','attend_face_or_read');
    end
end

if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if not(exist('the_frames'))
        the_frames = ver_frames;

        for s = 1:6 % attending
            stimuli(s).on_frames = 30 + (1+(s-1)*30):(30*6*2):1470;
            stimuli(s).durations = 0*stimuli(s).on_frames + 19;
        end
        for s = 7:12 % reading
            stimuli(s).on_frames = 30 + 180 + (1+(s-1-6)*30):(30*6*2):1470;
            stimuli(s).durations = 0*stimuli(s).on_frames + 19;
        end
        for i = 1:length(stimuli)
            for j = 1:length(stimuli(i).on_frames)
                on_frame = stimuli(i).on_frames(j);
                duration = stimuli(i).durations(j);
                 mi(the_frames(on_frame-1,:,:,:),2,[2,3,1],'on-1');
                 mi(the_frames(on_frame,:,:,:),2,[2,3,2],d2s({'stimulus ' i '(' j ') ' 'on ' on_frame}));
                 mi(the_frames(on_frame+1,:,:,:),2,[2,3,3],'on+1');
                  mi(the_frames(on_frame-1+duration-1,:,:,:),2,[2,3,4],'last-1');
                mi(the_frames(on_frame-1+duration,:,:,:),2,[2,3,5],'last');
                 mi(the_frames(on_frame-1+duration+1,:,:,:),2,[2,3,6],'last+1');
                 my_pause(0.2);
            end
        end
    end
end


if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %attend_face_or_read_resampled_data
    %attend_object_or_body_resampled_data
    %attend_vase_or_face_resampled_data;
    %attend_object_or_body_resampled_data;
%    resampled_data = attend_gnd_near_vase_or_face_resampled_data;%saccade_from_vase_or_face_resampled_data;% attend_object_or_body_resampled_data;%attend_vase_or_face_resampled_data;%fixate_vase_or_face_resampled_data;
    %e = 'vermeer_attention';
    %ee = 'attend_gnd_near_vase_or_face';
    eval(d2s({'resampled_data  = ' ee '_resampled_data;'}));

    offset = 4 * 5;
    %gray_data = mean(resampled_data(:,(1:30)+offset),2);
    %MB_display_resampled_data_and_frames(gray_data, ver_frames(data_frames(1),:,:,:), RF_mapping.pixel_to_voxel_assignment, 100 );
    p_images.experiment = e;
    p_images.experiment_subtype = ee;
    p_images.imgs = [];
    for s = [1 7 2 8 3 9 4 10 5 11 6 12]
        data_frames = [];
        for p = 1:4 % p = 1:2 % TEMP!!!!, was p=1:4, change on 14June2015 for surface attention viewing. p=1:4 is for vermeer stuff
            data_frames = [data_frames (stimuli(s).on_frames(p)):(stimuli(s).on_frames(p)-1+stimuli(s).durations(p))];%!!!!!
        end
            if 0
                for i = 1:length(data_frames)
                    mi(the_frames(data_frames(i),:,:,:),9,[1,1,1],d2c({s p i data_frames(i)}));
                    my_pause;
                end
            end

            
            data = resampled_data(:,(data_frames+offset));
            mean_data = mean(data,2); %- gray_data;%!!!!!!!!!!!!!!!!!!
            fig_num = p;
            if s > 6
                fig_num = p+100;
            end
            img = MB_display_resampled_data_and_frames(mean_data, ver_frames(data_frames(1),:,:,:), RF_mapping.pixel_to_voxel_assignment, fig_num );
            p_images.imgs(s).img = img;
        %my_pause
    end
    my_save(p_images,'p_images',d2s({'p_images.' ee }));
end

% if 0
%     if not(exist('BL_frames_1'))
%             'load Barry Lyndon frames'
%             BL_frames_1 = zeros(7500,320,512,3,'uint8');
%             for i = 1:7500
%                 BL_frames_1(i,:,:,:)=imread(d2s({'~/Data/experiments/BarryLyndon/BarryLyndon_redspot_17Jan2015/movie_frames/' i '.png'}));
%             end
%             my_save(frames,'frames');
%     end
% end

if 0
    if not(exist('BL_frames_1'))
        fps('*** load BL_frames_1');
        load('/Users/davidzipser/Google_Drive/Data/stimuli/2015/1/17Jan2015_BarryLyndon_material_for_scanning/BarryLyndon_16Jan2015_1.avi.frames.mat');
        BL_frames_1 = frames;
    end
    % if not(exist('BL_frames_2'))
    %     fps('*** load BL_frames_2');
    %     load('/Users/davidzipser/Google_Drive/Data/stimuli/2015/1/17Jan2015_BarryLyndon_material_for_scanning/BarryLyndon_16Jan2015_2.avi.frames.mat');
    %     BL_frames_2 = frames;
    % end
    % if not(exist('BL_frames_3'))
    %     fps('*** load BL_frames_3');
    %     load('/Users/davidzipser/Google_Drive/Data/stimuli/2015/1/17Jan2015_BarryLyndon_material_for_scanning/BarryLyndon_16Jan2015_3.avi.frames.mat');
    %     BL_frames_3 = frames;
    % end
end


if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    SCREEN_MASK_X = 19;
    SCREEN_MASK_Y = 2;
    offset = 4 * 5;
    mask = 0*zeros(128,128,'single'); mask((1+SCREEN_MASK_X):(128-SCREEN_MASK_X),(1+SCREEN_MASK_Y):(128-SCREEN_MASK_Y))=1;
    blank = square_single_zeros(512);

    resampled_data = attend_person_not_BL_BarryLyndon_16Jan2015_1_resampled_data;%fixate_BarryLyndon_16Jan2015_1_resampled_data;%
    frames = BL_frames_1;


    h = figure(1);
    p_image_frames = zeros(1530,128,128,'single');
    video_name = 'p_image_video';
    mkdir(d2s({'~/Desktop/' video_name '.' now}));
    outputVideo = VideoWriter(d2s({'~/Desktop/' video_name '.' now '/' video_name '.' now '.avi'}),'Motion JPEG AVI');%'Uncompressed AVI');%
    outputVideo.FrameRate = 5;
    outputVideo.Quality = 75;
    open(outputVideo);
    integration_window = 2*5;
    for i = 1:(1530)
        j= 1+round((i-1)*5);
        if j > 7500
            break;
        end
        img = voronoi_P_image( mean(resampled_data(:,(i+offset):(i+offset+integration_window)),2), RF_mapping.pixel_to_voxel_assignment, 30);
        img=img.*mask;
        img = zeroToOneRange(img);
        p_image_frames(i,:,:) = img;
        %img(1,1)=1;img(1,2)=-1;
        mi(img,1,[1,2,1],d2sp({round(i/5)-6}));%,d2sp({one_TRs(round(1+i/5/0.9)) two_TRs(round(1+i/5/0.9)) round(i/5)}));
        mi(frames(j,:,:,:),1,[1,2,2],d2s({j/25}));
        F=getframe(h);
        writeVideo(outputVideo,F.cdata);
        drawnow;%pause(1/5);%
    end
    my_save(p_image_frames,'p_image_frames');
    close(outputVideo);
end