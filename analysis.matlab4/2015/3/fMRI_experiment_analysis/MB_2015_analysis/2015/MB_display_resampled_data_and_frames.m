function img = MB_display_resampled_data_and_frames(the_data, the_frames, pixel_to_voxel_assignment, fig_num )
%
%

    T=1;%0.25;
    SCREEN_MASK_X = 19;
    SCREEN_MASK_Y = 2;
    % SCREEN_MASK_X = 30;
 %    SCREEN_MASK_Y = 30;
    mask = 0*zeros(128,128,'single'); mask((1+SCREEN_MASK_X):(128-SCREEN_MASK_X),(1+SCREEN_MASK_Y):(128-SCREEN_MASK_Y))=1;
    blank = square_single_zeros(512);

    offset = 0;%4 * 5;
    for i = 1:1:(size(the_data,2)-offset);
        voxel_responses = sum(the_data(:,(i+offset):(i+offset)),2);
        img = mask .* voronoi_P_image( voxel_responses, pixel_to_voxel_assignment, 25);
        % img(1,1)=T;
        % img(1,2)=-T;
        mi( img,fig_num,[1,2,1],d2s({floor((i-1)/5)}));
        drawnow;
        if 0
            % simg = squeeze(sum(single(the_frames(i,:,:,:)),1));
            % simg = simg/ max(max(max(simg)));
            simg = squeeze(the_frames(i,:,:,:));
            mi( simg,fig_num,[1,2,2],d2s({floor((i-1)/5)}));
            drawnow;
        end
        pause(1/5);
    end
end