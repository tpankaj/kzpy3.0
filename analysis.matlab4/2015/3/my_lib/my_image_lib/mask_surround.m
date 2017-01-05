function image_matrix = mask_surround( image_matrix, radius, value )
%image_matrix = mask_surround( image_matrix, radius, value )
%	19 Nov. 2013

    size_image_matrix = size(image_matrix);
    
    length_image_matrix = length(image_matrix);
    half_len = length_image_matrix / 2;
    
    if length(size_image_matrix) < 3
        for x = 1:length_image_matrix
            for y = 1:length_image_matrix
                if distance( x, half_len, y, half_len ) > radius
                    image_matrix(x, y) = value;
                end
            end
        end
    else
            for x = 1:length_image_matrix
                for y = 1:length_image_matrix
                    if distance( x, half_len, y, half_len ) > radius
                        image_matrix(x, y,:) = value;
                    end
                end
            end
    end
end

