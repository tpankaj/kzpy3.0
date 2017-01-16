function frames = convert_video_to_frames( video_name )
%convert_video_to_frames( video_name )
%   First step in the video to motion-energy workflow. Give the name of a
%   video, a director with '_images' appended to this name is created and
%   the individual frames saved into it.

    inputVideo = VideoReader(video_name);    
    mkdir([video_name,'_images'])
    h = waitbar(0,video_name);
    for ii = 1:inputVideo.NumberOfFrames
        waitbar(ii/inputVideo.NumberOfFrames);
        img = read(inputVideo,ii);
        if ii == 1
        	frames = zeros(inputVideo.NumberOfFrames,size(img,1),size(img,2),size(img,3),'uint8');
        end
        frames(ii,:,:,:) = img;
        imwrite(img,fullfile([video_name,'_images'],sprintf('%d.png',ii)));
    end 
    close(h);
    fps('*** Saving frames...')
    save([video_name,'.frames.mat'],'frames', '-v7.3');
end
