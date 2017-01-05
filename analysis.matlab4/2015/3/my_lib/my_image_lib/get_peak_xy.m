function [x,y] = get_peak_xy( M )
%function [x,y] = get_peak_xy( M )
%   24 August 2014
    [C,I] = max(M(:));
    [x,y] = ind2sub(size(M),I);
end

