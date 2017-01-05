function m = gaussian_matrix2( the_width, the_std, opt_x, opt_y )
%function m = gaussian_matrix2( the_width, the_std )
%   19 Nov. 2013
    m = zeros( the_width );

    if nargin < 3
        opt_x = 0;
        opt_y = 0;
    end
    for x = 1:the_width
        for y = 1:the_width
            m( x, y ) = gaussian_2d( x, y, the_width/2+opt_x, the_width/2+opt_y, the_std, the_std );
        end
    end

end

