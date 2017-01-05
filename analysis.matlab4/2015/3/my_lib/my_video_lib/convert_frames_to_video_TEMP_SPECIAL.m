function frames = convert_video_to_frames( frame_folder, img_extension, video_name, frame_rate, patterns, specialoverlay )
    [imageNames,imageNumbers] = get_sorted_numbered_files( frame_folder, img_extension );
    outputVideo = VideoWriter(d2s({'~/Desktop/Video_Desktop/' video_name '.' num2str(now)}),'Motion JPEG AVI');%'Uncompressed AVI');%
    outputVideo.FrameRate = frame_rate;
    outputVideo.Quality = 95;
    open(outputVideo)

    gray = zeros(768,1024,3,'single')+0.5;
    o=zeroToOneRange(sqsing(specialoverlay(:,:,4)))/20.0;
    o(1:767,:)=o(2:768,:);
    gray(:,128:(1024-129),1)=gray(:,128:(1024-129),1)+o;
    gray(:,128:(1024-129),2)=gray(:,128:(1024-129),2)+o;
    gray(:,128:(1024-129),3)=gray(:,128:(1024-129),3)+o;
    pat = 0 * gray;
    h=waitbar(0,'processing...');movegui(h,'southeast');
    for ii = 1:8*15
        writeVideo(outputVideo,gray);
    end
    for ii = 1:660%length(imageNames)
        waitbar(ii/length(imageNames));
        img = zeroToOneRange(imread(fullfile(frame_folder,imageNames{ii})));
        for jj = 1:3
            pat(1:768,1:768,:) = zeroToOneRange(single(patterns(:,:,:,randi(100))));
            pat1 = zeroToOneRange(patterns(:,:,:,randi(100)));
            offset = randi(512);
            pat(1:768,(1+offset+256):1024,:) = pat1(1:768,1:(768-offset),:);
            pat = pat .* img + gray .* (1-img);
            pat(384,512,:)=0;
            %mi(pat,1,[1,1,1],d2s({ii}));
            %pause(0.01)
            writeVideo(outputVideo,pat)
        end
    end
    for ii = 1:8*15
        writeVideo(outputVideo,gray);
    end
    close(outputVideo)
    close(h)
end

