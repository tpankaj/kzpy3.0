function p_image = voronoi_P_image( voxel_responses, pixel_to_voxel_assignment, num_voxels_per_pixel )
% function p_image = voronoi_P_image( voxel_responses, pixel_to_voxel_assignment, num_voxels_per_pixel )
%
	img_width = size(pixel_to_voxel_assignment,1);
	p_image = zeros(img_width,img_width,'single');
	
	%h = waitbar(0,'processing');movegui('southeast');
	for x = 1:img_width
		%waitbar(x/img_width);
		for y = 1:img_width
			for i = 1:num_voxels_per_pixel
				v = pixel_to_voxel_assignment(x,y,i);
				p_image(x,y) = p_image(x,y) + voxel_responses(v);
			end
			p_image(x,y) = p_image(x,y)/num_voxels_per_pixel;
		end
	end
	%close(h);
end