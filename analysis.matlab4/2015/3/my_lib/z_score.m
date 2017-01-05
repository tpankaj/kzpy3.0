function z = z_score( d )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
    m = mean(d);
    sd = std(d);
    
    z = (d-m)/sd;

end

