function [xdeg, ydeg, orientation, eccentricity] = visual_coordinates_from_512px_vim1_fixated_image( x, y, xcen, ycen, pix_per_deg )

x = x - xcen;
y = y - ycen;

ydeg = -y / pix_per_deg;
xdeg = x / pix_per_deg;

orientation = atan(ydeg/xdeg)/2/pi*360;

if true
if and(xdeg < 0, ydeg >= 0)
    orientation = 180 + orientation;
elseif and(xdeg < 0, ydeg < 0)
    orientation = 180 + orientation;
elseif and(xdeg >= 0, ydeg >= 0)
    orientation = orientation;
elseif and(xdeg >= 0, ydeg < 0)
    orientation = 360 + orientation;
end
end
eccentricity = sqrt( xdeg^2 + ydeg^2 );

