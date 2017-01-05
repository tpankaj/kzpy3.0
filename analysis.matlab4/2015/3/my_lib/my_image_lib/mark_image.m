function [ Xs, Ys ] = mark_image( img, opt_title )
%function [ Xs, Ys ] = mark_image( img )
%   
    if nargin < 2
        opt_title = '';
    end
    
    mi(img,1,[1,1,1], d2s({opt_title}));

    Xs = [];
    Ys = [];
    
    disp('Click to mark, return to go on or end.');
    
    for clicks = 1:1000
        figure(1);
        [x,y] = ginput(1);
        if length(x)<1
            break;
        end

        hold on; plot(x,y,'ro'); hold off;

        Xs(clicks) = x;
        Ys(clicks) = y;
    end

end

