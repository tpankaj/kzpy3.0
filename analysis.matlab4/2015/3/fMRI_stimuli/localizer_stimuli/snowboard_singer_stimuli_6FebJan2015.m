%
% first task: get filenames in one sequence
if 0
    clear frames;
    clear all_frames;
    
    i = 1
    frames(i).path = '~/Desktop/Video_Desktop/video_material_for_1Sept2014_scanning/BarryLyndonMaterial/Barry_Lyndon_1_to_1800s'
    frames(i).filenames = get_sorted_numbered_files(frames(i).path,'png');
    
    i = i + 1
    frames(i).path = '~/Desktop/Video_Desktop/video_material_for_1Sept2014_scanning/BarryLyndonMaterial/Barry_Lyndon_1800_to_3600s'
    frames(i).filenames = get_sorted_numbered_files(frames(i).path,'png');
    
    i = i + 1
    frames(i).path = '~/Desktop/Video_Desktop/video_material_for_1Sept2014_scanning/BarryLyndonMaterial/Barry_Lyndon_3600_to_4318s'
    frames(i).filenames = get_sorted_numbered_files(frames(i).path,'png');
    
    i = i + 1
    frames(i).path = '~/Desktop/Video_Desktop/video_material_for_1Sept2014_scanning/BarryLyndonMaterial/Barry_Lyndon2_1_to_3600s_a'
    frames(i).filenames = get_sorted_numbered_files(frames(i).path,'png');
    
    i = i + 1
    frames(i).path = '~/Desktop/Video_Desktop/video_material_for_1Sept2014_scanning/BarryLyndonMaterial/Barry_Lyndon2_1_to_3600s_b'
    frames(i).filenames = get_sorted_numbered_files(frames(i).path,'png');
    
    i = i + 1
    frames(i).path = '~/Desktop/Video_Desktop/video_material_for_1Sept2014_scanning/BarryLyndonMaterial/Barry_Lyndon2_1_to_3600s_c'
    frames(i).filenames = get_sorted_numbered_files(frames(i).path,'png');
    
    i = i + 1
    frames(i).path = '~/Desktop/Video_Desktop/video_material_for_1Sept2014_scanning/BarryLyndonMaterial/Barry_Lyndon2_3600_to_4600s'
    frames(i).filenames = get_sorted_numbered_files(frames(i).path,'png');
    
    i = i + 1
    frames(i).path = '~/Desktop/Video_Desktop/video_material_for_1Sept2014_scanning/BarryLyndonMaterial/Barry_Lyndon2_4600_to_5100s'
    frames(i).filenames = get_sorted_numbered_files(frames(i).path,'png');
    
    i = i + 1
    frames(i).path = '~/Desktop/Video_Desktop/video_material_for_1Sept2014_scanning/BarryLyndonMaterial/Barry_Lyndon2_5100_to_5800s'
    frames(i).filenames = get_sorted_numbered_files(frames(i).path,'png');
    
    i = i + 1
    frames(i).path = '~/Desktop/Video_Desktop/video_material_for_1Sept2014_scanning/BarryLyndonMaterial/Barry_Lyndon2_5800_to_6320s'
    frames(i).filenames = get_sorted_numbered_files(frames(i).path,'png');
    
    ctr = 0;
    for j = 1:i
        j
        for k = 1:length(frames(j).filenames)
            ctr = ctr + 1;
            all_frames(ctr).path = frames(j).path;
            all_frames(ctr).filename = frames(j).filenames(k);
        end
    end
end

if 0
    save('~/Desktop/Matlab_Desktop/BarryLyndon_all_frames.mat','all_frames');
end

if 0
    ctr = 0;
    ctr2 = 0;
    ctr3 = 0;
    clear dir_str;
    for i = 1:length(all_frames)
        if ctr == 0
            ctr2 = ctr2 + 1;
            dir_str = d2s({'~/Desktop/Video_Desktop/video_material_for_1Sept2014_scanning/BarryLyndonMaterial/Barry_Lyndon_1000_frame_sets/',ctr2})
            mkdir(dir_str);
        end
        ctr = ctr + 1;
        ctr3 = ctr3 + 1;
        sys_str = d2s({'cp ', all_frames(i).path, '/', all_frames(i).filename{1}, ' ', dir_str, '/', ctr3, '.png' });
        system( sys_str );
        if ctr == 1000
            ctr = 0;
        end
    end
end

if 0
   for i = 1:205
       dir_str = d2s({'~/Desktop/Video_Desktop/video_material_for_1Sept2014_scanning/BarryLyndonMaterial/Barry_Lyndon_1000_frame_sets/',i})
       ctr = 0;
       for j = 1:28:1000
           ctr = ctr + 1;
           k = j+(i-1)*1000;
           mi(imread(d2s({dir_str,'/',k,'.png'})),1,[6,6,ctr],d2s({k}));
       end
       pause;
   end  
end

if 0
    ctr = 0;
    ctr2 = 0
   for i = 1:200
       dir_str = d2s({'~/Desktop/Video_Desktop/video_material_for_1Sept2014_scanning/BarryLyndonMaterial/Barry_Lyndon_1000_frame_sets/',i})
       ctr = ctr + 1;
       ctr2 = ctr2 + 1;
       mi(imread(d2s({dir_str,'/',1+(i-1)*1000,'.png'})),1,[6,6,ctr],d2c({ctr2,1+(i-1)*1000}));
%       f=round(rand(1)*20000)+1;mi(imread(d2s({dir_str,'/',f,'.png'})),1,[6,6,ctr],d2c({ctr2,f}));
%        ctr = ctr + 1;
%        ctr2 = ctr2 + 1;
%        mi(imread(d2s({dir_str,'/',501+(i-1)*1000,'.png'})),1,[6,6,ctr],d2c({ctr2,501+(i-1)*1000}));
       if ctr == 36
           pause;
           ctr = 0;
       end
       
       
   end  
end

if 0
    clc
    ft = 195000
    rmax = 3;
    smax = 5;
    ctr = 0;
    
    fs = [];
    for r = 1:rmax
        outputVideo = VideoWriter(d2s({'~/Desktop/BarryLyndonRun_',r,'.avi'}),'Motion JPEG AVI');
        outputVideo.FrameRate = 25;
        open(outputVideo);

        r
        ctr2 = 0;
        for o = 1:20
            o
            for s = 1:smax
                s
                ctr2 = ctr2 + 1;
                f = 1 + (s-1)*ft/(smax) + (o-1) * ft/3/5/20 + ft*(r-1)/15;
                mi(imread(d2s({'~/Desktop/Video_Desktop/video_material_for_1Sept2014_scanning/BarryLyndonMaterial/Barry_Lyndon_1000_frame_sets/',uint32(1+floor((f-1)/1000)),'/',f,'.png'})),2,[10,10,ctr2],d2c({f}));
                ctr = ctr + 1;
                fs(ctr) = f;
                for ff = 1:6*25
                    fff = f + (ff-1);
                    fimg = imread(d2s({'~/Desktop/Video_Desktop/video_material_for_1Sept2014_scanning/BarryLyndonMaterial/Barry_Lyndon_1000_frame_sets/',uint32(1+floor((fff-1)/1000)),'/',fff,'.png'}));
                    writeVideo(outputVideo,fimg);
                end
            end
        end
        close(outputVideo);
    end
    figure(12);
    plot(1:ctr,fs,'go');
end

if 0
    for i = 1:211
        my_makethumbdir('1.png',d2s({'~/Desktop/Video_Desktop/video_material_for_1Sept2014_scanning/BarryLyndonMaterial/Barry_Lyndon_1000_frame_sets/', i}) );
    end
end

if 0
    clear contact_sheet;
    for i = 1:211
        thumb_path = d2s({'~/Desktop/Video_Desktop/video_material_for_1Sept2014_scanning/BarryLyndonMaterial/Barry_Lyndon_1000_frame_sets/', i, '/_pngThumbnails'});
        d=dir(thumb_path);
        [sortedImageNames,imageNumbers] = get_sorted_numbered_files( thumb_path, 'png' );
        length(sortedImageNames)
        contact_sheet_specs = {};
        ctr = 0;
        x = 1;
        y = 1;
        for j = 1:10:1000
            ctr = ctr + 1;
            img = imread(d2s({thumb_path,'/',sortedImageNames{j}}));
            img_size= size(img);
            contact_sheet_specs{ctr} = {{single(img)/255.0},{x,y}};
            x = x + img_size(1);

            if x > 10*img_size(1)
                x = 1;
                y = y + img_size(2);
            end
        end
        contact_sheet(i).img = compose_image(contact_sheet_specs);
        mi(contact_sheet(i).img,1,[1,1,1],d2s({i}));
        pause(0.1);
        imwrite(contact_sheet(i).img,d2s({'~/Desktop/Video_Desktop/video_material_for_1Sept2014_scanning/BarryLyndonMaterial/Barry_Lyndon_1000_frame_sets/',i,'/_contact_sheet.png'}));
    end
end

if 0
    ctr = 0;
    clear big_contact_sheet;
    for i = 1:210
        if mod(i,10) == 0
            ctr = ctr + 10;
        end
        %big_contact_sheet((1+(i-1)*img_size(1)):(i*img_size(1)),1:10*img_size(2),:) = contact_sheet(i).img((1+(i-1)*img_size(1)):(i*img_size(1)),1:10*img_size(2),:);
        big_contact_sheet((ctr + 1+(i-1)*img_size(1)):(ctr + i*img_size(1)),1:10*img_size(2),:) = contact_sheet(i).img((1+(1-1)*img_size(1)):(1*img_size(1)),1:10*img_size(2),:);
    end
    mi(big_contact_sheet,10);
end

if 0 % using this on 16 Jan 2015 to make 5 minute movies:
    % BarryLyndon_16Jan2015_1.avi, BarryLyndon_16Jan2015_2.avi,
    % BarryLyndon_16Jan2015_3.avi, BarryLyndon_16Jan2015_4.avi, BarryLyndon_16Jan2015_5.avi
    clc
    ft = 195000
    rmax = 4;
    smax = 5;
    ctr = 0;
    USE_ON_OFF_FIXSPOT = false;
    
    fff=1;
    fimg = imread(d2s({'~/Desktop/Video_Desktop/video_material_for_1Sept2014_scanning/BarryLyndonMaterial/Barry_Lyndon_1000_frame_sets/',uint32(1+floor((fff-1)/1000)),'/',fff,'.png'}));
    gray = single(0.5+0*fimg);
    
    fs = [];
    for r = 1:rmax
        outputVideo = VideoWriter(d2s({'~/Desktop/BarryLyndon_16Jan2015_',r,'.avi'}),'Motion JPEG AVI');%'Uncompressed AVI');%
        outputVideo.FrameRate = 25;
        open(outputVideo);

        r
        ctr2 = 0;
        for o = 1:10 %for o = 1:20 originally in 24Sept2014 file.
            o
            for s = 1:smax
                s
                ctr2 = ctr2 + 1;
                f = 1 + (s-1)*ft/(smax) + (o-1) * ft/3/5/20 + ft*(r-1)/15;

                mi(imread(d2s({'~/Desktop/Video_Desktop/video_material_for_1Sept2014_scanning/BarryLyndonMaterial/Barry_Lyndon_1000_frame_sets/',uint32(1+floor((f-1)/1000)),'/',f,'.png'})),2,[10,10,ctr2],d2c({f}));
                ctr = ctr + 1;
                fs(ctr) = f;
                mask = sqsing(fimg(:,:,1));
                mask = 0*mask;
                fimg_size = size(fimg);
                occluder_width = 30;
                for q = 1:50
                    mx = round(rand(1)*fimg_size(1)-occluder_width/2);
                    my = round(rand(1)*fimg_size(2)-occluder_width/2);
                    x1 = mx;y1=my;
                    if x1<1, x1 = 1; end
                    if y1<1, y1 = 1; end
                    x2 = mx+occluder_width;y2=my+occluder_width;
                    if x2>fimg_size(1), x2=fimg_size(1); end
                    if y2>fimg_size(2), y2=fimg_size(2); end
                    mask(x1:x2,y1:y2)=1;
                end
                    
                for ff = 1:6*25 % is this 25 the framerate?
                    fff = f + (ff-1);
                    fimg = imread(d2s({'~/Desktop/Video_Desktop/video_material_for_1Sept2014_scanning/BarryLyndonMaterial/Barry_Lyndon_1000_frame_sets/',uint32(1+floor((fff-1)/1000)),'/',fff,'.png'}));
                    fimg = single(fimg)/255;
                    fimg_size = size(fimg);
                    fx = round(fimg_size(1)/2);
                    fy = round(fimg_size(2)/2);
                  
%                     if ff > 4*25
%                         fimg = merge_images(fimg,gray,mask);
%                     end
                    if USE_ON_OFF_FIXSPOT
                        if mod(o,2)==0
                            if ff < 8
                                if s == 1
                                    fimg = 0 * fimg + 0.5;
                                end
                            end
                            fimg((fx-1):(fx+1),(fy-1):(fy+1),:)=0;
                            fimg(fx:fx,fy:fy,:)=1;
                        end
                    end
                    writeVideo(outputVideo,fimg);
                end
            end
        end
        close(outputVideo);
    end
    figure(12);
    plot(1:ctr,fs,'go');
end


% 6Feb2015 Jan. convert frames to video
if 0

    h = waitbar(0,'Now processing'); movegui(h,'southeast');
    videos(1).frames = zeros(150*30,384,512,3,'single')+0.5;
    videos(2).frames = zeros(150*30,384,512,3,'single')+0.5;
    videos(2).path = '~/Desktop/LakeStreetDive_IWantYouBack.mp4_images/';
    videos(1).path = '~/Desktop/Snowboard_GoPro_BackCountry.mp4_images/';
    videos(1).start = 60*30
    videos(2).start = 30*30;
    blank_384_512 = zeros(384,512,'single')+0.5;
    for v = 1:2
        ctr = 0;
        for i = videos(v).start:(videos(v).start-1+150*30)
            ctr = ctr + 1;
            waitbar(ctr/(150*30));
            fimg = imread(d2s({videos(v).path i '.png'}));
            r = reduceMatrixByHalf(sqsing(fimg(:,:,1))/255);
            g = reduceMatrixByHalf(sqsing(fimg(:,:,2))/255);
            b = reduceMatrixByHalf(sqsing(fimg(:,:,3))/255);
            videos(v).frames(ctr,12:371,:,1) = r(:,64:(640-65));
            videos(v).frames(ctr,12:371,:,2) = g(:,64:(640-65));
            videos(v).frames(ctr,12:371,:,3) = b(:,64:(640-65));
            if mod(ctr,100)==0
                mi(videos(v).frames(ctr,:,:,:),1,[1,1,1],d2s({ctr}));
            end
        end
    end
    close(h);
end

if 1
    outputVideo = VideoWriter(d2s({'~/Desktop/CW_snowboard_singer_fixspot_6Feb2015.avi'}),'Motion JPEG AVI');%'Uncompressed AVI');%
    outputVideo.FrameRate = 30;
    open(outputVideo);

    f_ctr=[0,0];
    for a = 1:25
        for v = 1:2
            for f = 1:(6*30)
                f_ctr(v)=f_ctr(v)+1;
                fimg = squeeze(videos(v).frames(f_ctr(v),:,:,:));
                fimg(189:195,253:259,:)=0;
                fimg(191:193,255:257,:)=1;
                writeVideo(outputVideo,fimg);
                mi(fimg,1,[1,1,1],d2s({f_ctr(v)}));
                %pause(1/30);
            end
        end
    end
	close(outputVideo);
end
