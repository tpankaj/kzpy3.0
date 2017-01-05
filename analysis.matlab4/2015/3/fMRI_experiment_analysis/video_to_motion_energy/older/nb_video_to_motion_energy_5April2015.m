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
% Getting Barry Lyndon texture energy images 5 April 2015
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    if not(exist('frames'))
       frame_path = '~/Data/stimuli/2015/2/11Feb2015_Vermeer_reading_videos/vermeer1to10.avi_images';
%       frame_path = '~/Data/experiments/localizer2/eccentricity/movie_frames';
%       frame_path = '~/Data/experiments/localizer2/orientation/movie_frames';
%       frame_path = '~/Data/stimuli/2015/1/17Jan2015_BarryLyndon_material_for_scanning/BarryLyndon_16Jan2015_3.avi_images';
        fps(d2s({'*** Reading frames from ' frame_path}))
%        frame_path = '~/Desktop/Data/fmri_scanning_experiments/2015/2/5Feb2015_localizer2/localizer2_orientation_5Feb2015.736000.8698/localizer2_orientation_5Feb2015_frames';
%        frame_path = '~/Desktop/Data/fmri_scanning_experiments/2015/2/5Feb2015_localizer2/localizer2_eccentricity_5Feb2015.736000.8919/localizer2_eccentricity_5Feb2015_frames';
        N = length(dir([frame_path '/*.png']));
        f = imread(d2s({frame_path '/' 1 '.png'}));
        %f = imresize(f,[768/2,512]);
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
            %f = imresize(f,[768/2,512]);
            f_size = size(f);            
            frames(i,min_start:min_end,:,:) = f;
        end
        close(h);
    end
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 2;
    if not(exist('texture_energy_images'))
        grayscale_frames = sum(single(frames),4);
        texture_energy_images = make_high_pass_version_of_image_general(grayscale_frames,6,false);
    end
    texture_energy_images_uint8 = uint8(0*texture_energy_images);
    h=waitbar(0,'uint8ing frames...');movegui(h,'southeast');
    for i = 1:length(texture_energy_images)
        waitbar(i/N);
        texture_energy_images_uint8(i,:,:) = uint8range(squeeze(texture_energy_images(i,:,:)));
    end
    close(h);
    my_save(texture_energy_images_uint8,'texture_energy_images_uint8_Vm')
    %my_save(texture_energy_images,'texture_energy_images_BL2')
end

if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 3;
    size_frames = size(frames);
    for i = 1:(size_frames(1)-9)
        mi(frames(i,:,:,:),1,[1,3,1]);
        mi(grayscale_frames(i,:,:),1,[1,3,2]);
        mi(texture_energy_images_uint8(i,:,:),1,[1,3,3]);
%         mi(sum(texture_energy_images((i-4):(i+8),:,:),1) - 13*texture_energy_images(1,:,:),1,[1,3,3]);
        pause(1/25);
    end
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 4;
    size_frames = size(frames);
    N = size_frames(1);
    frame_rate = 5;
    frame_t = (0:(N-1))/5;
    tr=0.9;
    tr_t = 0:tr:max(frame_t);
    hrf = model_HRF( (0:149)/frame_rate );
%     x=randi(500)+6;y=randi(500)+6;
%     a=5;
%     te = squeeze(sum(sum(texture_energy_images(:,(x-a:x+a),(y-a:y+a)),2),3));

    size_texture_energy_images = size(texture_energy_images);
    texture_energy_images_HRF = zeros(length(tr_t),size_texture_energy_images(2),size_texture_energy_images(3));
    h=waitbar(0,'loading frames...');movegui(h,'southeast');
    for x = 1:size_texture_energy_images(2)
        waitbar(x/size_texture_energy_images(2));
        for y = 1:size_texture_energy_images(3)
        te = squeeze(texture_energy_images(:,x,y));
        %mp({frame_t,te,'o-'},1,[2,1,1]);
        at_frame_rate = conv(te,hrf,'full');
        at_tr_rate = 0*tr_t;
        for i = 1:length(tr_t)
            i2 = round(tr_t(i)*frame_rate);
            if i2 > 0
                if i2 <= length(at_frame_rate)
                    at_tr_rate(i) = at_frame_rate(i2);
                end
            end
        end
        texture_energy_images_HRF(:,x,y) = (at_tr_rate-mean(at_tr_rate))/std(at_tr_rate);
        end
    end
    close(h);
%     mp({frame_t,at_frame_rate(1:length(frame_t)),'o-'},1,[2,1,2]);
%     hold on;
%     mp({tr_t,at_tr_rate,'rx-'},1,[2,1,2]);
%     hold off;
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 5;
    size_frames = size(frames);
    mean_texture_energy = mean(texture_energy_images_HRF(i,:,:),1);
    mask = 0*zeros(512,512,'single'); mask(74:437,12:501)=1;
    for i = 1:length(tr_t)
        img = squeeze(texture_energy_images_HRF(i,:,:));%-mean_texture_energy;
        img=img.*mask;img(1,1)=7.3;img(1,2)=-7.3;
        img(find(not(isfinite(img))))=0;
        mi(img,1,[1,1,1],d2s({i}));
        pause(0.1);
    end
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 6; % 57,13,25;   63,13,23
    X = 161;Y=227;
    BZ=25;mi(zc_sum(:,:,BZ),20);
    [BY,BX]=ginput(1);
    BY=round(BY);BX=round(BX);
    %BX=X;BY=Y;
    hold on;plot(BY,BX,'ro');hold off;
        i=1;
        a=20;
        sample_time_course_ori = squeeze(sum(sum(ori_texture_energy_images_HRF(:,(X-a:X+a),(Y-a:Y+a)),2),3));
        sample_time_course_ecc = squeeze(sum(sum(ecc_texture_energy_images_HRF(:,(X-a:X+a),(Y-a:Y+a)),2),3));
        sample_time_course = [sample_time_course_ori;sample_time_course_ecc];
        sample_time_course = sample_time_course + 0*std(sample_time_course)*randn(size(sample_time_course));
        real_time_course_ori = squeeze(z_scored_filtered_func_data6.z_img(BX,BY,BZ,:));+squeeze(z_scored_filtered_func_data11.z_img(BX,BY,BZ,:));
        real_time_course_ecc = squeeze(z_scored_filtered_func_data8.z_img(BX,BY,BZ,:));+squeeze(z_scored_filtered_func_data13.z_img(BX,BY,BZ,:));
        real_time_course_ori = real_time_course_ori(1:334);
        real_time_course_ecc = real_time_course_ecc(1:334);
        real_time_course = [real_time_course_ori ; real_time_course_ecc];
        sample_time_course = real_time_course;
%         sample_time_course(1:667)=sample_time_course(2:668);sample_time_course(668:668)=0;
        mp({sample_time_course,'o-'},1,[2,1,1]);
        mp({abs(real(fft(sample_time_course))),'o-'},1,[2,1,2]);
        mask = 0*zeros(512,512,'single'); mask(74:437,12:501)=1;
        c_img(i).img = sqsing(512);
         h=waitbar(0,'processing...');movegui(h,'southeast');
        for x = 1:512
            waitbar(x/512);
            for y = 1:512
                local_timecourse = [squeeze(ori_texture_energy_images_HRF(:,x,y));squeeze(ecc_texture_energy_images_HRF(:,x,y))];
                %local_timecourse = local_timecourse(1:340);
                cc = corrcoef(sample_time_course,local_timecourse);
                c_img(i).img(x,y) = cc(1,2);
            end
        end;close(h);
        c_img(i).img(find(not(isfinite(c_img(i).img))))=0;
        mi(mask.*c_img(i).img,2,[1,2,1]);%hold on;plot(Y,X,'o');hold off;
        mi(mask.*c_img(i).img.^4,2,[1,2,2]);%hold on;plot(Y,X,'o');hold off;
    
end