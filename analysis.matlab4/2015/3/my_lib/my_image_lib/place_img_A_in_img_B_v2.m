function img_B = place_img_A_in_img_B_v2( img_A, img_B, x_center_offset, y_center_offset )
%function img_B = place_img_A_in_img_B_v2( img_A, img_B, x_center_offset, y_center_offset )
% 5 March 2015

    img.A.dim.x = size(img_A,1);
    img.A.dim.y = size(img_A,2);
    img.B.dim.x = size(img_B,1);
    img.B.dim.y = size(img_B,2);

    img.B.start.x = round(x_center_offset+img.B.dim.x/2 - img.A.dim.x(1)/2) ;
    img.B.finish.x = 	img.B.start.x + img.A.dim.x(1) - 1;
	

    img.B.start.y = round(y_center_offset+img.B.dim.y/2 - img.A.dim.y(1)/2 );
    img.B. finish.y = 	img.B.start.y + img.A.dim.y(1) - 1;

     [img.A.dim.x img.A.dim.y]
     [img.B.start.x img.B.finish.x img.B.start.y img.B.finish.y]

    img_B( img.B.start.x:img.B.finish.x, img.B.start.y:img.B.finish.y ) = img_A;

 end

    

