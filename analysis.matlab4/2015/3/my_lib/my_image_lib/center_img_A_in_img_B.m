function img_B = center_img_A_in_img_B( img_A, img_B )
%img_B = center_img_A_in_img_B( img_A, img_B )
%   Detailed explanation goes here
    
    size_img_A = size(img_A);
    size_img_B = size(img_B);
%     [size_img_A size_img_B]
%     [(size_img_B(1)/2 - size_img_A(1)/2) (size_img_B(1)/2 + size_img_A(1)/2-1)]
%     [(size_img_B(2)/2 - size_img_A(2)/2) (size_img_B(2)/2 + size_img_A(2)/2-1)]
    if length(size_img_B) == 3
        img_B( (size_img_B(1)/2 - size_img_A(1)/2):(size_img_B(1)/2 + size_img_A(1)/2-1), (size_img_B(2)/2 - size_img_A(2)/2):(size_img_B(2)/2 + size_img_A(2)/2-1),: ) = img_A;
    else
        img_B( (size_img_B(1)/2 - size_img_A(1)/2):(size_img_B(1)/2 + size_img_A(1)/2-1), (size_img_B(2)/2 - size_img_A(2)/2):(size_img_B(2)/2 + size_img_A(2)/2-1) ) = img_A;
    end
end
    

