function [texture_energy_images, blurred_images, high_pass_images ] = ...
    make_high_pass_version_of_image_general( images, sd, do_graphics )
% function [texture_energy_images, blurred_images, high_pass_images ] = ...
%     make_high_pass_version_of_image_general( images, sd, do_graphics )
%
%   <images> can be either an array of images, or a single image.
%   The images must be square and have width in the set 2^n.
%   Example:
% [texture_energy_images, blurred_images, high_pass_images ] = make_high_pass_version_of_image_general((GD.stimTrn512_int8([17,1609,1665,1469],:,:)),6);
%
% [texture_energy_images, blurred_images, high_pass_images ] = make_high_pass_version_of_image_general(stimTrn512_int8([17,1609,1665,1469],:,:),6,false);

    if nargin < 3
        do_graphics = true;
    end

%%% If given a single 2d image, turn it into an array of images.

    if length(size(images)) == 2
        temp = images;
        size_images = size(images);
        images = zeros(1,size_images(1),size_images(2),'single');
        images(1,:,:) = temp;
    end
    
%%%  Test that images are valid  

    imageMatrix = squeeze(images(1,:,:));
    
    size_imageMatrix = size( squeeze(images(1,:,:)) );

    if length( size_imageMatrix ) > 2
        error('if length( size_imageMatrix ) > 2');
    end

    if length( size_imageMatrix(1) ) ~= length( size_imageMatrix(2) )
        error('if length( size_imageMatrix(1) ) ~= length( size_imageMatrix(2) )');
    end

    valid_widths = (zeros(1,20)+2).^(1:20);

    if not( ismember( size_imageMatrix(1), valid_widths) )
        error('if not( ismember( size_imageMatrix(1), valid_widths) ) )');
    end

%%% These are matricies used to analyze every image.
    
    g=gaussian_matrix2(8*sd,sd); 
    g_in_512 = zeros(size_imageMatrix(1)*2,size_imageMatrix(1)*2,'single');
    uuu = round(256-length(g)/2);
    g_in_512(uuu:(uuu+length(g)-1),uuu:(uuu+length(g)-1)) = g;
    
    imageMatrix_double_extent = zeros(size_imageMatrix(1)*2,size_imageMatrix(1)*2,'single');
    
    blurred_images = zeros(length(images(:,1,1)), size_imageMatrix(1), size_imageMatrix(1), 'single' );
    high_pass_images = blurred_images;
    texture_energy_images = blurred_images;
    
    A = size_imageMatrix(1)/2;
    B = 3*size_imageMatrix(1)/2-1;
    
    background_value = imageMatrix(1,1);%mean(mean(mean(images))) % this only works for Kay images
    
%%%
    h=waitbar(0,'processing images...');movegui(h,'southeast');
    len_images = length(images(:,1,1));
    for i = 1:len_images
        waitbar(i/len_images);
        imageMatrix = squeeze(images(i,:,:));

        imageMatrix = zeroToOneRange( single( imageMatrix ) );

        background_value = mean(mean(imageMatrix));
        imageMatrix_double_extent = 0 * imageMatrix_double_extent + background_value;
        imageMatrix_double_extent(A:B,A:B) = imageMatrix;

        c = conv2(imageMatrix_double_extent,g,'same');

        blurred_image = c(A:B,A:B);

        high_pass_image = imageMatrix - blurred_image;

        texture_energy_image = abs( high_pass_image );
        
        blurred_images(i,:,:) = blurred_image;
        high_pass_images(i,:,:) = high_pass_image;
        texture_energy_images(i,:,:) = texture_energy_image;

        if do_graphics
            mi(imageMatrix,1,[1,5,1]);
            mi(imageMatrix_double_extent,1,[1,5,2]);
            mi(blurred_image,1,[1,5,3]);
            mi(high_pass_image,1,[1,5,4]);
            mi(texture_energy_image,1,[1,5,5]);


            if i < length(images(:,1,1))
                my_pause
            else
                fprintf('Done.\n');
            end
        end
    end
    close(h);

%%%
end
