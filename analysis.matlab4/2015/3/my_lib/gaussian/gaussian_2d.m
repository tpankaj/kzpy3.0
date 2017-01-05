function z = gaussian_2d( x, y, xm, ym, xsd, ysd )
%function z = gaussian_2d( x, y, xm, ym, xsd, ysd )
%      19 Nov. 2013
    xt = (x-xm)^2 / (2*xsd^2);
    yt = (y-ym)^2 / (2*ysd^2);
    z = exp( -xt -yt ) / (ysd*xsd*2*pi);
end

