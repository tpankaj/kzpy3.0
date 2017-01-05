function pixel_to_voxel_assignment = assign_voxels_to_pixels( voxel_xys, img_width, max_num_voxels_per_pixel )
% function pixel_to_voxel_assignment = assign_voxels_to_pixels( voxel_xys, img_width, max_num_voxels_per_pixel )
%
	pixel_to_voxel_assignment = zeros(img_width,img_width,max_num_voxels_per_pixel);
	distances = zeros(length(voxel_xys),1,'single');
	h = waitbar(0,'processing');movegui('southeast');
	for x = 1:img_width
		waitbar(x/img_width);
		for y = 1:img_width
			distances = 0 * distances;
			for i = 1:length(voxel_xys)
				distances(i) =  distance( x, voxel_xys(i,1), y, voxel_xys(i,2) );
			end
			[~,voxel_indicies] = sort(distances);
			pixel_to_voxel_assignment(x,y,:) = voxel_indicies(1:max_num_voxels_per_pixel);
		end
	end
	close(h);
end