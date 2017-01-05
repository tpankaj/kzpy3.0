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
% Taking localizer2 of 5 February and using it to find HVO receptive fields
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% this loads the frame png images and puts them into a frame array. I
%%% saved these as .mat files for the orientation and eccentricity
%%% localizers, so this cell is not needed immeidately. 15Feb2015
CELL_NUM = 1;
    if not(exist('frames'))
        frame_path = '~/Desktop/Data/fmri_scanning_experiments/2015/2/5Feb2015_localizer2/localizer2_orientation_5Feb2015.736000.8698/localizer2_orientation_5Feb2015_frames';
%        frame_path = '~/Desktop/Data/fmri_scanning_experiments/2015/2/5Feb2015_localizer2/localizer2_eccentricity_5Feb2015.736000.8919/localizer2_eccentricity_5Feb2015_frames';
        N = length(dir([frame_path '/*.png']));
        f = imread(d2s({frame_path '/' 1 '.png'}));
        f_size = size(f);
        min_dim = min(f_size(1:2));
        max_dim = max(f_size(1:2));
        frames = zeros(N,max_dim,max_dim,3,'uint8');
        min_start = (max_dim-min_dim)/2;
        min_end = max_dim - min_start - 1;
        [min_dim max_dim min_start min_end]
        h=waitbar(0,'loading frames...');movegui(h,'southeast');
        for i = 1:N
            waitbar(i/N);
            f = imread(d2s({frame_path '/' i '.png'}));
            f_size = size(f);            
            frames(i,min_start:min_end,:,:) = f;
        end
        close(h);
    end
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% These were also saved as .mat files, separately for orientation and
% eccentricity.
CELL_NUM = 2;
    if not(exist('texture_energy_images'))
        grayscale_frames = sum(single(frames),4);
        texture_energy_images = make_high_pass_version_of_image_general(grayscale_frames,6,false);
    end
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This is for display only, comparing the various versions of frames.
CELL_NUM = 3;
    size_frames = size(frames);
    for i = 50:(size_frames(1)-9)
        mi(frames(i,:,:,:),1,[1,3,1]);
        mi(grayscale_frames(i,:,:),1,[1,3,2]);
        mi(texture_energy_images(i,:,:),1,[1,3,3]);
%         mi(sum(texture_energy_images((i-4):(i+8),:,:),1) - 13*texture_energy_images(1,:,:),1,[1,3,3]);
        pause(1/5);
    end
end

if 0 %%%%%%%%%%% reduce size of texture energy images %%%%%%%%%%
CELL_NUM = 3.5;
    texture_energy_images = ecc_texture_energy_images;
    size_frames = size(frames);
    texture_energy_images_128 = zeros(size_frames(1),128,128,'single');
    for i = 1:size_frames(1)
        texture_energy_images_128(i,:,:) = reduceMatrixByHalf(reduceMatrixByHalf( squeeze(texture_energy_images(i,:,:)) ));
    end
    my_save(texture_energy_images_128,'texture_energy_images_128');
end
    

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Used this to save 128x128 texture_energy_images_HRF for orientation and
% ecc., 15Feb2015
CELL_NUM = 4;
    texture_energy_images = texture_energy_images_128;
    TR_LENGTH_s = 0.9;
    NUM_TRs = 340;
    FRAME_RATE_Hz = 5;
    SCREEN_MASK_X = 19;
    SCREEN_MASK_Y = 2;
    texture_energy_images_HRF = get_texture_energy_images_HRF(texture_energy_images,TR_LENGTH_s,NUM_TRs,FRAME_RATE_Hz,SCREEN_MASK_X,SCREEN_MASK_Y);
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Make list of [1508] gaussians.
CELL_NUM = 8;
    gaussians = []
    X = -63;Y=-63;
    ctr = 0;
    for y = -63:(distance( 0, X, 0, Y )/24):64
        for x = -63:(distance( 0, X, 0, Y )/24):64
            X=x;Y=y;ctr=ctr+1;
            sd = (2+distance( 0, x, 0, y )/12);
            gaussians(ctr).x = x;
            gaussians(ctr).y = y;
            gaussians(ctr).sd = sd;
            mi(gaussian_matrix2(128,sd,x,y),70);
            pause(0.03);
        end
    end
    fps(d2s({ctr}));
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% assign timecourses to gaussians
    for n = 1:length(gaussians)
        g = gaussian_matrix2(128,gaussians(n).sd,gaussians(n).x,gaussians(n).y);
        mi(g,70,[2,1,1],d2s({n}));
        timecourse = zeros(NUM_TRs,1,'single');
        HRF_timecourse = [ori_texture_energy_images_HRF ; ecc_texture_energy_images_HRF];
        for i = 1:2*NUM_TRs
            timecourse(i) = summ(g.*squeeze(HRF_timecourse(i,:,:)));
        end
        gaussians(n).timecourse = timecourse;
        gaussians(n).img = g;
        mp({gaussians(n).timecourse,'o-'},70,[2,1,2],d2s({n}));
        pause(0.01);
    end
end
if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% assign images to gaussians
    for n = 1:length(gaussians)
        g = gaussian_matrix2(128,gaussians(n).sd,gaussians(n).x,gaussians(n).y);
        mi(g,70,[2,1,1],d2s({n}));
        gaussians(n).img = g;
        mp({gaussians(n).timecourse,'o-'},70,[2,1,2],d2s({n}));
        pause(0.01);
    end
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% make zc_sum
%     zc = z_scored_20150218_081721mbboldmb620mmAPPSNs004a001.z_img .* z_scored_20150218_081721mbboldmb620mmAPPSNs008a001.z_img + ...
%         z_scored_20150218_081721mbboldmb620mmAPPSNs006a001.z_img .* z_scored_20150218_081721mbboldmb620mmAPPSNs010a001.z_img;
    
%     zc = z_scored_20150216_082043mbboldmb620mmAPPSNs005a001.z_img .* z_scored_20150216_082043mbboldmb620mmAPPSNs011a001.z_img + ...
%         z_scored_20150216_082043mbboldmb620mmAPPSNs009a001.z_img .* z_scored_20150216_082043mbboldmb620mmAPPSNs013a001.z_img;

% % HVO
%     zc = z_scored_20150218_081721mbboldmb620mmAPPSNs004a001.z_img .* z_scored_20150218_081721mbboldmb620mmAPPSNs008a001.z_img + ...
%         z_scored_20150218_081721mbboldmb620mmAPPSNs006a001.z_img .* z_scored_20150218_081721mbboldmb620mmAPPSNs010a001.z_img + ...
%         z_scored_20150216_082043mbboldmb620mmAPPSNs005a001.z_img .* z_scored_20150216_082043mbboldmb620mmAPPSNs011a001.z_img + ...
%         z_scored_20150216_082043mbboldmb620mmAPPSNs009a001.z_img .* z_scored_20150216_082043mbboldmb620mmAPPSNs013a001.z_img;

    %CW
    zc = z_scored_20150207_091449mbboldmb620mmAPPSNs004a001.z_img .* z_scored_20150207_091449mbboldmb620mmAPPSNs008a001.z_img + ...
        z_scored_20150207_091449mbboldmb620mmAPPSNs006a001.z_img .* z_scored_20150207_091449mbboldmb620mmAPPSNs010a001.z_img;
    
    
    zc_sum = squeeze(sum(zc,4));
    size(zc_sum)
% 
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% sort voxels into analysis order
    size_zc_sum = size(zc_sum);
    ctr = 0;
    zc_ordering = zeros(size_zc_sum(1)*size_zc_sum(2)*size_zc_sum(3),4,'single');
    h=waitbar(0,'processing...');movegui(h,'southeast');
    for x = 1:size_zc_sum(1)
        waitbar(x/size_zc_sum(1));
    for y = 1:size_zc_sum(2)
    for z = 1:size_zc_sum(3)
        ctr = ctr + 1;
        zc_ordering(ctr,:) = [zc_sum(x,y,z) x y z];
    end
    end
    end;close(h);
    zc_ordering = -1 * sortrows( -1*zc_ordering, 1 );
    hist(zc_ordering(1:100));
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% process voxels
    %NUM_TRs = 340;
    
    NUM_TRs = 240; %for CW
    fps(d2s({'Note, num TRs = ' NUM_TRs}));
    my_pause
    size_zc_sum = size(zc_sum);
    ctr = 0;
    gaussian_r_volume = zeros(size_zc_sum(1),size_zc_sum(2),size_zc_sum(3),length(gaussians),'single');
    for i = 1:length(zc_ordering)
        x = zc_ordering(i,2);
        y = zc_ordering(i,3);
        z = zc_ordering(i,4);
        if z > 7
        if z < 51
        if y < 40
                mi_nii(zc_sum,x,y,z,1,false);
                %pause(0.1)
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            BX = x;BY=y;BZ=z;
        %     real_time_course_ori = squeeze(z_scored_filtered_func_data6.z_img(BX,BY,BZ,:))+squeeze(z_scored_filtered_func_data11.z_img(BX,BY,BZ,:));
        %     real_time_course_ecc = squeeze(z_scored_filtered_func_data8.z_img(BX,BY,BZ,:))+squeeze(z_scored_filtered_func_data13.z_img(BX,BY,BZ,:));
        
%             real_time_course_ori = squeeze(z_scored_20150216_082043mbboldmb620mmAPPSNs005a001.z_img(BX,BY,BZ,:))+squeeze(z_scored_20150216_082043mbboldmb620mmAPPSNs011a001.z_img(BX,BY,BZ,:));
%             real_time_course_ecc = squeeze(z_scored_20150216_082043mbboldmb620mmAPPSNs009a001.z_img(BX,BY,BZ,:))+squeeze(z_scored_20150216_082043mbboldmb620mmAPPSNs013a001.z_img(BX,BY,BZ,:));

%             real_time_course_ori = squeeze(z_scored_20150218_081721mbboldmb620mmAPPSNs004a001.z_img(BX,BY,BZ,:))+squeeze(z_scored_20150218_081721mbboldmb620mmAPPSNs008a001.z_img(BX,BY,BZ,:));
%             real_time_course_ecc = squeeze(z_scored_20150218_081721mbboldmb620mmAPPSNs006a001.z_img(BX,BY,BZ,:))+squeeze(z_scored_20150218_081721mbboldmb620mmAPPSNs010a001.z_img(BX,BY,BZ,:));

%                %HVO
%             real_time_course_ori = squeeze(z_scored_20150216_082043mbboldmb620mmAPPSNs005a001.z_img(BX,BY,BZ,:))+...
%                 squeeze(z_scored_20150216_082043mbboldmb620mmAPPSNs011a001.z_img(BX,BY,BZ,:))+...
%                 squeeze(z_scored_20150218_081721mbboldmb620mmAPPSNs004a001.z_img(BX,BY,BZ,:))+...
%                 squeeze(z_scored_20150218_081721mbboldmb620mmAPPSNs008a001.z_img(BX,BY,BZ,:));
%             real_time_course_ecc = squeeze(z_scored_20150216_082043mbboldmb620mmAPPSNs009a001.z_img(BX,BY,BZ,:))+...
%                 squeeze(z_scored_20150216_082043mbboldmb620mmAPPSNs013a001.z_img(BX,BY,BZ,:))+...
%                 squeeze(z_scored_20150218_081721mbboldmb620mmAPPSNs006a001.z_img(BX,BY,BZ,:))+...
%                 squeeze(z_scored_20150218_081721mbboldmb620mmAPPSNs010a001.z_img(BX,BY,BZ,:));
% 

            %CW
            real_time_course_ori = squeeze(z_scored_20150207_091449mbboldmb620mmAPPSNs004a001.z_img(BX,BY,BZ,:))+...
                squeeze(z_scored_20150207_091449mbboldmb620mmAPPSNs008a001.z_img(BX,BY,BZ,:));
            real_time_course_ecc = squeeze(z_scored_20150207_091449mbboldmb620mmAPPSNs006a001.z_img(BX,BY,BZ,:))+...
                squeeze(z_scored_20150207_091449mbboldmb620mmAPPSNs010a001.z_img(BX,BY,BZ,:));


            real_time_course = [real_time_course_ori ; real_time_course_ecc];
            
            if std(real_time_course)>0
                data = zscore(real_time_course);
                d_range = [15:NUM_TRs (NUM_TRs+12):(2*NUM_TRs-6)];
                data = data(d_range);
                r_max = -90;
                for n=1:length(gaussians)

                    model = zscore(gaussians(n).timecourse);
                    model = model(d_range+1);

                    cc = corrcoef(data,model);
                     c = cc(1,2);
                    gaussians(n).cc = c;
%                     temp = gaussians(n).img;
%                     temp = zeroToOneRange(temp);
%                     temp = temp * c;
%                     temp(1,1)=1;

                    if false
                        if c > r_max
                            r_max = c;
                            mp({model,'b-'},70,[2,1,2]);
                            hold on;
                            mp({data,'ro-'},70,[2,1,2],d2c({r_max n}));    
                            hold off;
                            mi(temp,70,[2,2,2]);
                            mp({data,model,'o'},70,[2,2,1]);axis([-3,3,-3,3]);axis('square');title(gaussians(n).cc);
                            pause(0.1);
                        end
                    end
                    gaussian_r_volume(BX,BY,BZ,n) = gaussians(n).cc;    
                end
                [i max(squeeze(gaussian_r_volume(BX,BY,BZ,:)))]
            %%%%%
            end
        end
        end
        end
    end
end



if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% looking at RFs, select RFs
    ctr = 0;
    coverage_img = zeros(128,128,'single');
    selected_voxel_xyzs = [];
    for i = 1:length(zc_ordering)
        x = zc_ordering(i,2);
        y = zc_ordering(i,3);
        z = zc_ordering(i,4);
        if z > 7
        if z < 51
        if y < 40
            mi(zc_sum(:,:,z,1),1,[1,3,1]);
            hold on; plot(y,x,'o');hold off;
            %gaussian_r_volume(x,y,z,:);
            g_num = find(gaussian_r_volume(x,y,z,:)==max(gaussian_r_volume(x,y,z,:)));
            r = gaussian_r_volume(x,y,z,g_num);
            if r > 0.10
                ctr = ctr + 1;
                hold on; plot(y,x,'ro');hold off;pause(0.1);
                selected_voxel_xyzs(ctr,:) = [x y z];
                mi(gaussians(g_num).img,1,[1,3,2],d2s({r}));
                coverage_img = coverage_img + gaussians(g_num).img;
                mi(log(coverage_img+0.01),1,[1,3,3],d2s({ctr}));
                pause(0.01);
            end
        end
        end
        end
    end
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% load and rename data

% % 18Feb2015_Zipser_Pilots_HVO localizer2 ori, ecc
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/2/18Feb2015_Zipser_Pilots_HVO/fsl/18Feb2015_mc_to_006a_of_9Feb2015/20150218_081721mbboldmb620mmAPPSNs004a001.z_scored_filtered_func_data.mat')
% z_scored_20150218_081721mbboldmb620mmAPPSNs004a001 = z_scored_filtered_func_data;
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/2/18Feb2015_Zipser_Pilots_HVO/fsl/18Feb2015_mc_to_006a_of_9Feb2015/20150218_081721mbboldmb620mmAPPSNs006a001.z_scored_filtered_func_data.mat')
% z_scored_20150218_081721mbboldmb620mmAPPSNs006a001 = z_scored_filtered_func_data;
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/2/18Feb2015_Zipser_Pilots_HVO/fsl/18Feb2015_mc_to_006a_of_9Feb2015/20150218_081721mbboldmb620mmAPPSNs008a001.z_scored_filtered_func_data.mat')
% z_scored_20150218_081721mbboldmb620mmAPPSNs008a001 = z_scored_filtered_func_data;
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/2/18Feb2015_Zipser_Pilots_HVO/fsl/18Feb2015_mc_to_006a_of_9Feb2015/20150218_081721mbboldmb620mmAPPSNs010a001.z_scored_filtered_func_data.mat')
% z_scored_20150218_081721mbboldmb620mmAPPSNs010a001 = z_scored_filtered_func_data;
% 
% % 16Feb2015_Zipser_Pilots_HVO localizer2 ori, ecc
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/2/16Feb2015_Zipser_Pilots_HVO/fsl/16Feb2015_mc_to_006a_of_9Feb2015/20150216_082043mbboldmb620mmAPPSNs005a001.z_scored_filtered_func_data.mat')
% z_scored_20150216_082043mbboldmb620mmAPPSNs005a001 = z_scored_filtered_func_data;
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/2/16Feb2015_Zipser_Pilots_HVO/fsl/16Feb2015_mc_to_006a_of_9Feb2015/20150216_082043mbboldmb620mmAPPSNs009a001.z_scored_filtered_func_data.mat')
% z_scored_20150216_082043mbboldmb620mmAPPSNs009a001 = z_scored_filtered_func_data;
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/2/16Feb2015_Zipser_Pilots_HVO/fsl/16Feb2015_mc_to_006a_of_9Feb2015/20150216_082043mbboldmb620mmAPPSNs011a001.z_scored_filtered_func_data.mat')
% z_scored_20150216_082043mbboldmb620mmAPPSNs011a001 = z_scored_filtered_func_data;
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/2/16Feb2015_Zipser_Pilots_HVO/fsl/16Feb2015_mc_to_006a_of_9Feb2015/20150216_082043mbboldmb620mmAPPSNs013a001.z_scored_filtered_func_data.mat')
% z_scored_20150216_082043mbboldmb620mmAPPSNs013a001 = z_scored_filtered_func_data;

% % 
% load('')
% z_scored_ = z_scored_filtered_func_data;
% load('')
% z_scored_ = z_scored_filtered_func_data;
% load('')
% z_scored_ = z_scored_filtered_func_data;
% load('')
% z_scored_ = z_scored_filtered_func_data;

% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/2/12Feb2015_Zipser_Pilots_HVO/fsl/16Feb2015_mc_to_006a_of_9Feb2015/20150212_081609mbboldmb620mmAPPSNs006a001.z_scored_filtered_func_data.mat')
% z_scored_20150212_081609mbboldmb620mmAPPSNs006a001 = z_scored_filtered_func_data;
% 
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/2/12Feb2015_Zipser_Pilots_HVO/fsl/16Feb2015_mc_to_006a_of_9Feb2015/20150212_081609mbboldmb620mmAPPSNs008a001.z_scored_filtered_func_data.mat')
% z_scored_20150212_081609mbboldmb620mmAPPSNs008a001 = z_scored_filtered_func_data;
% 
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/2/12Feb2015_Zipser_Pilots_HVO/fsl/16Feb2015_mc_to_006a_of_9Feb2015/20150212_081609mbboldmb620mmAPPSNs010a001.z_scored_filtered_func_data.mat')
% z_scored_20150212_081609mbboldmb620mmAPPSNs010a001 = z_scored_filtered_func_data;
% 
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/2/14Feb2015_Zipser_Pilots_HVO/fsl/16Feb2015_mc_to_006a_of_9Feb2015/20150214_082112mbboldmb620mmAPPSNs006a001.z_scored_filtered_func_data.mat')
% z_scored_20150214_082112mbboldmb620mmAPPSNs006a001 = z_scored_filtered_func_data;
% 
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/2/14Feb2015_Zipser_Pilots_HVO/fsl/16Feb2015_mc_to_006a_of_9Feb2015/20150214_082112mbboldmb620mmAPPSNs008a001.z_scored_filtered_func_data.mat')
% z_scored_20150214_082112mbboldmb620mmAPPSNs008a001 = z_scored_filtered_func_data;
% 
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/2/14Feb2015_Zipser_Pilots_HVO/fsl/16Feb2015_mc_to_006a_of_9Feb2015/20150214_082112mbboldmb620mmAPPSNs010a001.z_scored_filtered_func_data.mat')
% z_scored_20150214_082112mbboldmb620mmAPPSNs010a001 = z_scored_filtered_func_data;

% 16Feb2015_Zipser_Pilots_HVO Vermeer
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/2/16Feb2015_Zipser_Pilots_HVO/fsl/16Feb2015_mc_to_006a_of_9Feb2015/20150216_082043mbboldmb620mmAPPSNs019a001.z_scored_filtered_func_data.mat')
% z_scored_20150216_082043mbboldmb620mmAPPSNs019a001 = z_scored_filtered_func_data;
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/2/16Feb2015_Zipser_Pilots_HVO/fsl/16Feb2015_mc_to_006a_of_9Feb2015/20150216_082043mbboldmb620mmAPPSNs021a001.z_scored_filtered_func_data.mat')
% z_scored_20150216_082043mbboldmb620mmAPPSNs021a001 = z_scored_filtered_func_data;
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/2/16Feb2015_Zipser_Pilots_HVO/fsl/16Feb2015_mc_to_006a_of_9Feb2015/20150216_082043mbboldmb620mmAPPSNs025a001.z_scored_filtered_func_data.mat')
% z_scored_20150216_082043mbboldmb620mmAPPSNs025a001 = z_scored_filtered_func_data;

% 18, 22 & 25 January Barry Lyndon redspot
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/1/25Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/18Feb2015_mc_to_006a_of_9Feb2015/20150125_124420mbboldmb615mmAPPSNs009a001.z_scored_filtered_func_data.mat')
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/1/25Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/18Feb2015_mc_to_006a_of_9Feb2015/20150125_124420mbboldmb615mmAPPSNs007a001.z_scored_filtered_func_data.mat')
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/1/25Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/18Feb2015_mc_to_006a_of_9Feb2015/20150125_124420mbboldmb615mmAPPSNs005a001.z_scored_filtered_func_data.mat')
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/1/22Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/18Feb2015_mc_to_006a_of_9Feb2015/20150122_144129mbboldmb615mmAPPSNs007a001.z_scored_filtered_func_data.mat')
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/1/22Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/18Feb2015_mc_to_006a_of_9Feb2015/20150122_144129mbboldmb615mmAPPSNs005a001.z_scored_filtered_func_data.mat')
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/1/22Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/18Feb2015_mc_to_006a_of_9Feb2015/20150122_144129mbboldmb615mmAPPSNs003a001.z_scored_filtered_func_data.mat')
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/18Feb2015_mc_to_006a_of_9Feb2015/20150118_164630mbboldmb615mmAPPSNs007a001.z_scored_filtered_func_data.mat')
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/18Feb2015_mc_to_006a_of_9Feb2015/20150118_164630mbboldmb615mmAPPSNs005a001.z_scored_filtered_func_data.mat')
% load('/Users/davidzipser/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/18Feb2015_mc_to_006a_of_9Feb2015/20150118_164630mbboldmb615mmAPPSNs003a001.z_scored_filtered_func_data.mat')

% % CW data
% load('/Users/davidzipser/Desktop/Data/subjects/CW/2015/2/7Feb2015_Zipser_Pilots_CW/fsl/7Feb2015/20150207_091449mbboldmb620mmAPPSNs014a001.z_scored_filtered_func_data.mat')
% z_scored_20150207_091449mbboldmb620mmAPPSNs014a001 = z_scored_filtered_func_data;
% load('/Users/davidzipser/Desktop/Data/subjects/CW/2015/2/7Feb2015_Zipser_Pilots_CW/fsl/7Feb2015/20150207_091449mbboldmb620mmAPPSNs010a001.z_scored_filtered_func_data.mat')
% z_scored_20150207_091449mbboldmb620mmAPPSNs010a001 = z_scored_filtered_func_data;
% load('/Users/davidzipser/Desktop/Data/subjects/CW/2015/2/7Feb2015_Zipser_Pilots_CW/fsl/7Feb2015/20150207_091449mbboldmb620mmAPPSNs008a001.z_scored_filtered_func_data.mat')
% z_scored_20150207_091449mbboldmb620mmAPPSNs008a001 = z_scored_filtered_func_data;
% load('/Users/davidzipser/Desktop/Data/subjects/CW/2015/2/7Feb2015_Zipser_Pilots_CW/fsl/7Feb2015/20150207_091449mbboldmb620mmAPPSNs006a001.z_scored_filtered_func_data.mat')
% z_scored_20150207_091449mbboldmb620mmAPPSNs006a001 = z_scored_filtered_func_data;
% load('/Users/davidzipser/Desktop/Data/subjects/CW/2015/2/7Feb2015_Zipser_Pilots_CW/fsl/7Feb2015/20150207_091449mbboldmb620mmAPPSNs004a001.z_scored_filtered_func_data.mat')
% z_scored_20150207_091449mbboldmb620mmAPPSNs004a001 = z_scored_filtered_func_data;

end



if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% looking at P-images
    p_image = zeros(NUM_TRs,128,128,'single');
    SCREEN_MASK_X = 19;
    SCREEN_MASK_Y = 2;
    mask = 0*zeros(128,128,'single'); mask((1+SCREEN_MASK_X):(128-SCREEN_MASK_X),(1+SCREEN_MASK_Y):(128-SCREEN_MASK_Y))=1;
    coverage_mask = coverage_img;coverage_mask(find(coverage_mask>=0.01))=1;coverage_mask(find(coverage_mask<0.01))=0;
    for tr = 1:NUM_TRs
        tic
        resp_img = 0*coverage_img;
        for i = 1:length(selected_voxel_xyzs)
            x = selected_voxel_xyzs(i,1);
            y = selected_voxel_xyzs(i,2);
            z = selected_voxel_xyzs(i,3);
            resp = 0;
            for j = 0%0:3
                a = 80*j;
                for k = 0%-1:1
                    if tr == 1
                        if k == -1
                            k = 0;
                        end
                    end
%                     %localizer2, ori/ecc, 18Feb
%                     resp = resp + z_scored_20150218_081721mbboldmb620mmAPPSNs006a001.z_img(x,y,z,tr+a+k)+...
%                         z_scored_20150218_081721mbboldmb620mmAPPSNs010a001.z_img(x,y,z,tr+a+k);
%                     %localizer2, ori/ecc, 16Feb
%                     resp = resp + z_scored_20150216_082043mbboldmb620mmAPPSNs009a001.z_img(x,y,z,tr+a+k)+...
%                         z_scored_20150216_082043mbboldmb620mmAPPSNs013a001.z_img(x,y,z,tr+a+k);
                    
%                     %localizer2, ecc, 16Feb & 18Feb
%                     resp = resp + z_scored_20150218_081721mbboldmb620mmAPPSNs006a001.z_img(x,y,z,tr+a+k)+...
%                         z_scored_20150218_081721mbboldmb620mmAPPSNs010a001.z_img(x,y,z,tr+a+k)+...
%                         z_scored_20150216_082043mbboldmb620mmAPPSNs009a001.z_img(x,y,z,tr+a+k)+...
%                         z_scored_20150216_082043mbboldmb620mmAPPSNs013a001.z_img(x,y,z,tr+a+k);

%                     %localizer2, ori, 16Feb & 18Feb
%                     resp = resp + z_scored_20150218_081721mbboldmb620mmAPPSNs004a001.z_img(x,y,z,tr+a+k)+...
%                         z_scored_20150218_081721mbboldmb620mmAPPSNs008a001.z_img(x,y,z,tr+a+k)+...
%                         z_scored_20150216_082043mbboldmb620mmAPPSNs005a001.z_img(x,y,z,tr+a+k)+...
%                         z_scored_20150216_082043mbboldmb620mmAPPSNs011a001.z_img(x,y,z,tr+a+k);
% 
                                                           
%                     %Vermeer, 3 days
%                     resp = resp + z_scored_20150216_082043mbboldmb620mmAPPSNs019a001.z_img(x,y,z,tr+a+k)+...
%                         z_scored_20150216_082043mbboldmb620mmAPPSNs021a001.z_img(x,y,z,tr+a+k)+...
%                         z_scored_20150216_082043mbboldmb620mmAPPSNs025a001.z_img(x,y,z,tr+a+k);%+...
%                     resp = resp + z_scored_20150212_081609mbboldmb620mmAPPSNs006a001.z_img(x,y,z,tr+a+k)+...
%                         z_scored_20150212_081609mbboldmb620mmAPPSNs008a001.z_img(x,y,z,tr+a+k)+...
%                         z_scored_20150212_081609mbboldmb620mmAPPSNs010a001.z_img(x,y,z,tr+a+k);%+...
%                     resp = resp + z_scored_20150214_082112mbboldmb620mmAPPSNs006a001.z_img(x,y,z,tr+a+k)+...
%                         z_scored_20150214_082112mbboldmb620mmAPPSNs008a001.z_img(x,y,z,tr+a+k)+...
%                         z_scored_20150214_082112mbboldmb620mmAPPSNs010a001.z_img(x,y,z,tr+a+k);%+...
 
                    
%                     %Barry Lyndon, 3 days
%                     resp = resp + z_scored_20150118_164630mbboldmb615mmAPPSNs003a001.z_img(x,y,z,tr+a+k)+...
%                         z_scored_20150118_164630mbboldmb615mmAPPSNs005a001.z_img(x,y,z,tr+a+k)+...
%                         z_scored_20150118_164630mbboldmb615mmAPPSNs007a001.z_img(x,y,z,tr+a+k);%+...
%                     resp = resp + z_scored_20150122_144129mbboldmb615mmAPPSNs003a001.z_img(x,y,z,tr+a+k)+...
%                         z_scored_20150122_144129mbboldmb615mmAPPSNs005a001.z_img(x,y,z,tr+a+k)+...
%                         z_scored_20150122_144129mbboldmb615mmAPPSNs007a001.z_img(x,y,z,tr+a+k);%+...
%                     resp = resp + z_scored_20150125_124420mbboldmb615mmAPPSNs005a001.z_img(x,y,z,tr+a+k)+...
%                         z_scored_20150125_124420mbboldmb615mmAPPSNs007a001.z_img(x,y,z,tr+a+k)+...
%                         z_scored_20150125_124420mbboldmb615mmAPPSNs009a001.z_img(x,y,z,tr+a+k);%+...
                    
%                     %CW localizer2, ecc
                    resp = resp + z_scored_20150207_091449mbboldmb620mmAPPSNs006a001.z_img(x,y,z,tr+a+k)+...
                        z_scored_20150207_091449mbboldmb620mmAPPSNs010a001.z_img(x,y,z,tr+a+k);
                    
                    
                    
                end
%                 b = 40*j;
%                 for k = -1:1
%                     resp = resp - z_scored_20150216_082043mbboldmb620mmAPPSNs019a001.z_img(x,y,z,tr+b+k)-...
%                         z_scored_20150216_082043mbboldmb620mmAPPSNs021a001.z_img(x,y,z,tr+b+k)-...
%                         z_scored_20150216_082043mbboldmb620mmAPPSNs025a001.z_img(x,y,z,tr+b+k);%+...
%                 end
            end
%             resp = z_scored_20150209_081421mbboldmb620mmAPPSNs008a001.z_img(x,y,z,tr)+...
%                 z_scored_20150209_081421mbboldmb620mmAPPSNs013a001.z_img(x,y,z,tr);%+...
%                 z_scored_20150216_082043mbboldmb620mmAPPSNs005a001.z_img(x,y,z,tr)+...
%                 z_scored_20150216_082043mbboldmb620mmAPPSNs011a001.z_img(x,y,z,tr);

            resp = resp / 2;
            
%             resp = z_scored_20150216_082043mbboldmb620mmAPPSNs009a001.z_img(x,y,z,tr)+...
%                 z_scored_20150216_082043mbboldmb620mmAPPSNs013a001.z_img(x,y,z,tr);
%             resp = z_scored_20150216_082043mbboldmb620mmAPPSNs005a001.z_img(x,y,z,tr)+...
%                 z_scored_20150216_082043mbboldmb620mmAPPSNs011a001.z_img(x,y,z,tr);
%             if resp > 3
%                 resp = 3;
%             end
%             if resp < -3
%                 resp = -3;
%             end
            g_num = find(gaussian_r_volume(x,y,z,:)==max(gaussian_r_volume(x,y,z,:)));
            resp_img = resp_img + resp * gaussians(g_num).img;
        end
        mi(mask.*coverage_mask.*resp_img,2,[1,3,1]);
        mi(mask.*coverage_mask.*coverage_img,2,[1,3,2]);
        temp = mask.*coverage_mask.*resp_img./coverage_img;
        temp = zeroToOneRange(temp);temp=temp-mean(mean(temp));
        temp(1,1)=0.6;temp(1,2)=-0.6;
        mi(temp,2,[1,3,3],d2c({tr tr*0.9-5}));
        p_image(tr,:,:)=temp;
        pause(1.85);
        toc
    end
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% looking at P-images
    p_image(:,1,1)=0;p_image(:,1,2)=0;
    for tr = 2:NUM_TRs
        a=p_image(tr,:,:)+p_image(tr+1,:,:)+p_image(tr-1,:,:);
        a=a+p_image(tr+80,:,:)+p_image(tr+81,:,:)+p_image(tr+79,:,:);
        a=a+p_image(tr+2*80,:,:)+p_image(tr+2*80+1,:,:)+p_image(tr+2*80-1,:,:);
        b=p_image(tr+39,:,:)+p_image(tr+40,:,:)+p_image(tr+41,:,:);
        b=b+p_image(tr+80+39,:,:)+p_image(tr+80+40,:,:)+p_image(tr+80+41,:,:);
        b=b+p_image(tr+2*80+39,:,:)+p_image(tr+2*80+40,:,:)+p_image(tr+2*80+41,:,:);
%          a=zeroToOneRange(a).^2;
%          b=zeroToOneRange(b).^2;
        mi(a,3,[1,2,1]);
        mi(b,3,[1,2,2],d2s({tr*0.9-5}));
%         mi(a-b,3,[1,3,3]);
%         plot(a(find(a~=0)),b(find(a~=0)),'.');axis([-8,8,-8,8]);axis('square');
        pause%(0.9);
    end
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% look at gaussian results
    max_gaussian_r_volume = squeeze(max(gaussian_r_volume,[],4));
    for i = 1:60
        mi_nii(max_gaussian_r_volume,50,50,i,1,false);
        pause(0.2);
    end
    hist(reshape(max_gaussian_r_volume,size_zc_sum(1)*size_zc_sum(2)*size_zc_sum(3),1),100);axis([-0.1,0.7,0,300])
end




if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 
    BZ=26;mi(zc_sum(:,:,BZ),20);
    [BY,BX]=ginput(1);
    BY=round(BY);BX=round(BX);
    real_time_course_ori = squeeze(z_scored_filtered_func_data6.z_img(BX,BY,BZ,:))+squeeze(z_scored_filtered_func_data11.z_img(BX,BY,BZ,:));
    real_time_course_ecc = squeeze(z_scored_filtered_func_data8.z_img(BX,BY,BZ,:))+squeeze(z_scored_filtered_func_data13.z_img(BX,BY,BZ,:));
    real_time_course = [real_time_course_ori ; real_time_course_ecc];
    data = zscore(real_time_course);
    d_range = [15:NUM_TRs (NUM_TRs+12):(2*NUM_TRs-6)];
    data = data(d_range);
    r_max = -90;
    for n=1:length(gaussians)
        
        model = zscore(gaussians(n).timecourse);
        model = model(d_range+1);
     
        cc = corrcoef(data,model);
         c = cc(1,2);
        gaussians(n).cc = c;
        temp = gaussians(n).img;
        temp = zeroToOneRange(temp);
        temp = temp * c;
        temp(1,1)=1;
               
        if c > r_max
            r_max = c;
            mp({model,'b-'},70,[2,1,2]);
            hold on;
            mp({data,'ro-'},70,[2,1,2],d2c({r_max n}));    
            hold off;
        	mi(temp,70,[2,2,2]);
            mp({data,model,'o'},70,[2,2,1]);axis([-3,3,-3,3]);axis('square');title(gaussians(n).cc);
            pause(0.1);
        end
        
    end
end


if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 6; % 57,13,25;   63,13,23
    X = 40;Y=40;
    BZ=36;mi(zc_sum(:,:,BZ),20);
    [BY,BX]=ginput(1);
    BY=round(BY);BX=round(BX);
    %BX=X;BY=Y;
    hold on;plot(BY,BX,'ro');hold off;
        i=1;
        a=0;
        sample_time_course_ori = squeeze(sum(sum(ori_texture_energy_images_HRF(:,(X-a:X+a),(Y-a:Y+a)),2),3));
        sample_time_course_ecc = squeeze(sum(sum(ecc_texture_energy_images_HRF(:,(X-a:X+a),(Y-a:Y+a)),2),3));
        sample_time_course = [sample_time_course_ori;sample_time_course_ecc];

        real_time_course_ori = squeeze(z_scored_filtered_func_data6.z_img(BX,BY,BZ,:))+squeeze(z_scored_filtered_func_data11.z_img(BX,BY,BZ,:));
        real_time_course_ecc = squeeze(z_scored_filtered_func_data8.z_img(BX,BY,BZ,:))+squeeze(z_scored_filtered_func_data13.z_img(BX,BY,BZ,:));
        real_time_course = [real_time_course_ori ; real_time_course_ecc];
        
        %sample_time_course = real_time_course;
        mp({sample_time_course,'o-'},1,[2,1,1]);
        mp({abs(real(fft(sample_time_course))),'o-'},1,[2,1,2]);
        SCREEN_MASK_X = 19;
        SCREEN_MASK_Y = 2;
        mask = 0*zeros(128,128,'single'); mask((1+SCREEN_MASK_X):(128-SCREEN_MASK_X),(1+SCREEN_MASK_Y):(128-SCREEN_MASK_Y))=1;
        
        c_img(i).img = sqsing(512);
         h=waitbar(0,'processing...');movegui(h,'southeast');
        for x = 1:128
            waitbar(x/128);
            for y = 1:128
                local_timecourse = [squeeze(ori_texture_energy_images_HRF(:,x,y));squeeze(ecc_texture_energy_images_HRF(:,x,y))];
                cc = corrcoef(sample_time_course,local_timecourse);
                c_img(i).img(x,y) = cc(1,2);
            end
        end;close(h);
        c_img(i).img(find(not(isfinite(c_img(i).img))))=0;
        mi(mask.*c_img(i).img,2,[1,2,1]);
        mi(mask.*c_img(i).img.^4,2,[1,2,2]);
end