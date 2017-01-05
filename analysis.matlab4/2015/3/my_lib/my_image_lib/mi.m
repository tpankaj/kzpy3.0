function mi( image_matrix, figure_num, subplot_array, img_title, img_xlabel, img_ylabel, cmap )
% Should be identical to my_imagesc2.
% my_imagesc2( image_matrix, <opt>figure_num, <opt>subplot_array )
%   27 Sep. 2013

    if nargin < 1
      error('my_imagesc2 :  image_matrix is a required input')
    end

    if nargin > 1
      figure( figure_num )
    else
        figure(gcf)
    end

    if nargin > 2
      subplot( subplot_array(1), subplot_array(2), subplot_array(3));
    end

    imagesc( squeeze(image_matrix) );


    image_matrix_size = size(squeeze(image_matrix));

    if image_matrix_size(1) == image_matrix_size(2)
        axis('square');
    end

    if nargin > 3
        my_title( img_title );
    end

    if nargin > 4
        xlabel( img_xlabel );
    end

    if nargin > 5
        ylabel( img_ylabel );
    end

    if nargin > 6
        colormap(cmap);
    else
        colormap gray(256);
    end
    
    axis('off');
    axis('equal');
end
