
for x = 2:511
    for y = 2:511
        d1 = pixel_to_voxel_distance_matrix(x,y,1);
        d2 = pixel_to_voxel_distance_matrix(x,y,2);
        if abs(d1-d2)<0.5
            rf_mesh(x,y)=1;
        end
        if or(pixel_to_voxel_index_matrix(x+1,y+1) ~= pixel_to_voxel_index_matrix(x,y), pixel_to_voxel_index_matrix(x+1,y-1) ~= pixel_to_voxel_index_matrix(x,y))
            rf_mesh2(x,y) = 0;
        end
    end
end

mi(rf_mesh2,2,[1,1,1])

a = imread('~/DATA_REPRESENTATIONS/date_labeled_data_KZLAPTOP/21Nov2013/21Nov2013_DZ_NEW_IMAC/rf_neighbor_images/1/107.png');
a = single(a);
b = imread('~/DATA_REPRESENTATIONS/date_labeled_data_KZLAPTOP/21Nov2013/21Nov2013_DZ_NEW_IMAC/rf_neighbor_images/1/168.png');
b = single(b);

c=single(a).*rf_mesh2';
mi(mask_surround(c,210,128),1,[1,2,1]);
axis('off'); title('image 107');

d=single(b).*rf_mesh2';
mi(mask_surround(d,210,128),1,[1,2,2]);
axis('off'); title('image 168');
