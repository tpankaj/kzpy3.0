function convert_frames_to_video_numbered( frame_folder, num_frames,img_extension, video_name, frame_rate, quality )
    
    if quality == 100
        outputVideo = VideoWriter(d2s({'~/Desktop/Video_Desktop/' video_name '.' num2str(now)}),'Uncompressed AVI');
    else
        outputVideo = VideoWriter(d2s({'~/Desktop/Video_Desktop/' video_name '.' num2str(now)}),'Motion JPEG AVI');
        outputVideo.Quality = quality;
    end
    outputVideo.FrameRate = frame_rate;
    open(outputVideo)
    h=waitbar(0,'processing...');movegui(h,'southeast');
    for ii = 0:(num_frames-1)
        waitbar(ii/num_frames);
        img = imread(fullfile(frame_folder,d2s({ii '.' img_extension})));
        %mi(img,1,[1,1,1],d2s({ii}));
        %pause(0.01)
        writeVideo(outputVideo,img)
    end
    close(outputVideo)
    close(h)
end

