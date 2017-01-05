function masked_img = select_positive_pixel_count_nearest_specified_center( img, num_pixels, xy_center )
% img = zeros(128,128,'single');
% num_pixels = 200;
% xy_center = [70 70];

    img_size = size(img);
    
    dist_img = 0 * img;
    masked_img = 0 * img;
    
    for x = 1:img_size(1)
        for y = 1:img_size(2)
            dist_img(x,y) = distance_vec(xy_center, [x y]);
        end
    end
    
    [~,I] = sort(reshape(dist_img, img_size(1) * img_size(2), 1 ));

    ctr = 0;
    for i = 1:(img_size(1) * img_size(2))
        if img(I(i)) > 0
            masked_img(I(i)) = 1;
            ctr = ctr + 1;
        end
        if ctr >= num_pixels
            break;
        end
    end

end