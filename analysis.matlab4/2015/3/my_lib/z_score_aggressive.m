function z = z_score_aggressive( d )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
    z = z_score(d);
    N = 10;
    for i = 1:N
        z(find(z>3.1))=3.1;
        z(find(z<-3.1))=-3.1;
        if i > N
            z = z_score(z);
        end
    end
    z = z - median(z);
    z(find(z>3.0))=3.0;
    z(find(z<-3.0))=-3.0;
    
end

