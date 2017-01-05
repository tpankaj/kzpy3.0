function img = merge_images(img1,img2,img2_mask)
%function img = merge_images(img1,img2,img2_mask)
%
    
    size_img1 = size(img1);
    size_img2 = size(img2);
    if length(size_img1) < 3
        img1 = gray_image_to_color(img1);
    end
    if length(size_img2) < 3
        img2 = gray_image_to_color(img2);
    end

    
    img = img1*0;
%     mi(img1,1,[1,4,1]);
%     mi(img2,1,[1,4,2]);
%     mi(img2_mask,1,[1,4,3]);
    for c = 1:3
        img(:,:,c) = img1(:,:,c) .* img2_mask + img2(:,:,c) .* (1-img2_mask); % 26Oct2014 I am reversing the meaning of the mask.
        %img(:,:,c) = img1(:,:,c) .* (1-img2_mask) + img2(:,:,c) .* img2_mask; % 26Oct2014 I am reversing the meaning of the mask.
    end
    %mi(img,1,[1,4,4]);
end