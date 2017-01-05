function texture_energy_images_HRF = get_texture_energy_images_HRF(texture_energy_images,TR_LENGTH_s,NUM_TRs,FRAME_RATE_Hz,SCREEN_MASK_X,SCREEN_MASK_Y)
    
    num_frames = ceil( NUM_TRs * TR_LENGTH_s * FRAME_RATE_Hz);
    frame_times_s = (0:(num_frames-1)) / FRAME_RATE_Hz;
	TR_times_s = 0:TR_LENGTH_s:max(frame_times_s);

    HRF_at_frame_rate = model_HRF( (0:149)/FRAME_RATE_Hz );

    size_texture_energy_images = size(texture_energy_images);
    texture_energy_images_HRF = zeros(NUM_TRs,size_texture_energy_images(2),size_texture_energy_images(3));
    h=waitbar(0,'process texture_energy_images_HRF...');movegui(h,'southeast');
    for x = 1:size_texture_energy_images(2)
        waitbar(x/size_texture_energy_images(2));
        for y = 1:size_texture_energy_images(3)
        te = squeeze(texture_energy_images(:,x,y));
        at_frame_rate = conv(te,HRF_at_frame_rate,'full');
        at_TR_rate = 0*TR_times_s;
        for i = 1:length(TR_times_s)
            i2 = round(TR_times_s(i)*FRAME_RATE_Hz);
            if i2 > 0
                if i2 <= length(at_frame_rate)
                    at_TR_rate(i) = at_frame_rate(i2);
                end
            end
        end
        texture_energy_images_HRF(:,x,y) = z_score(at_TR_rate);%(at_TR_rate-mean(at_TR_rate))/std(at_TR_rate);
        end
    end
    close(h);

    mask = 0*zeros(128,128,'single'); mask((1+SCREEN_MASK_X):(128-SCREEN_MASK_X),(1+SCREEN_MASK_Y):(128-SCREEN_MASK_Y))=1;
    for i = 1:NUM_TRs
        img = mask .* squeeze(texture_energy_images_HRF(i,:,:));
        img(find(not(isfinite(img))))=0;
        texture_energy_images_HRF(i,:,:) = img;
        mi(texture_energy_images_HRF(i,:,:),1,[1,1,1],d2s({i}));
        pause(0.1);
    end
end