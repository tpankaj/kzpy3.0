function [xdeg, ydeg, orientation, eccentricity] = visual_coordinates_from_512px_vim1_fixated_image( x, y )

x = x - 256;
y = y - 256;

ydeg = -y * 10 / 250; %circle radius 250 pixels, 10 degrees in visual angle
xdeg = x * 10 / 250;

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

