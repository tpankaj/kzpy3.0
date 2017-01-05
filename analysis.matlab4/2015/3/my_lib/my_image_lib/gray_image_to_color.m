function color_img = gray_image_to_color(img)
%function color_img = gray_image_to_color(img)
%
    size_img = size(img);
    color_img = zeros(size_img(1),size_img(2),3);
    img = zeroToOneRange(img);
    color_img(:,:,1) = img;
    color_img(:,:,2) = img;
    color_img(:,:,3) = img;
end