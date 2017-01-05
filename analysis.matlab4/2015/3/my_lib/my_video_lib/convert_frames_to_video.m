function convert_frames_to_video( frame_folder, img_extension, video_name, frame_rate, quality, scale_factor )
    [imageNames,imageNumbers] = get_sorted_numbered_files( frame_folder, img_extension );

    if quality == 100
        outputVideo = VideoWriter(d2s({'~/Desktop/Video_Desktop/' video_name '.' num2str(now)}),'Uncompressed AVI');
    else
        outputVideo = VideoWriter(d2s({'~/Desktop/Video_Desktop/' video_name '.' num2str(now)}),'Motion JPEG AVI');
        outputVideo.Quality = quality;
    end
    outputVideo.FrameRate = frame_rate;
    open(outputVideo)
    h=waitbar(0,'processing...');movegui(h,'southeast');
    for ii = 1:length(imageNames)
        waitbar(ii/length(imageNames));
        img = imread(fullfile(frame_folder,imageNames{ii}));
        %mi(img,1,[1,1,1],d2s({ii}));
        %pause(0.01)
        img = imresize(img,scale_factor,'nearest');
        writeVideo(outputVideo,img)
    end
    close(outputVideo)
    close(h)
end

% convert_frames_to_video('.','png','ip2_dots_0',15,90,4.0)