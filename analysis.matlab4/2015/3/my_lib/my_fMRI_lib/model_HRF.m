function responses_s = model_HRF( timepoints_s )
%function r = model_HRF( t )
%
    responses_s = 0*timepoints_s;
    for i = 1:length(timepoints_s)
        t = timepoints_s(i);
            z = gaussian(0,4.25,1.3) + gaussian(0,5.6,1.3) + 0.5*gaussian(0,8,2) - 0.2*gaussian(0,17,4);
            r = gaussian(t,4.25,1.3) + gaussian(t,5.6,1.3) + 0.5*gaussian(t,8,2) - 0.2*gaussian(t,17,4) - z;
            responses_s(i) = r;
    end
% r = 0*t;
% r(5*15) = 1;
%r(1) = 1;
end
