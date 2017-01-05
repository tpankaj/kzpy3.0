function img_B = place_img_A_in_img_B( img_A, img_B, x_center_offset, y_center_offset )
%function img_B = place_img_A_in_img_B( img_A, img_B, x_center_offset, y_center_offset )
%

    
    size_img_A = size(img_A);
    size_img_B = size(img_B);
    
    if length(size_img_B) == 3
        img_B( (x_center_offset+size_img_B(1)/2 - size_img_A(1)/2):(x_center_offset+size_img_B(1)/2 + size_img_A(1)/2-1), (y_center_offset+size_img_B(2)/2 - size_img_A(2)/2):(y_center_offset+size_img_B(2)/2 + size_img_A(2)/2-1),: ) = img_A;
    else
        img_B( (x_center_offset+size_img_B(1)/2 - size_img_A(1)/2):(x_center_offset+size_img_B(1)/2 + size_img_A(1)/2-1), (y_center_offset+size_img_B(2)/2 - size_img_A(2)/2):(y_center_offset+size_img_B(2)/2 + size_img_A(2)/2-1) ) = img_A;
    end
end
    

