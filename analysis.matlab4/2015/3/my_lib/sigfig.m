function y = sigfig( x, n )
%function y = sigfig( x, n )
%   e.g., sigfig(pi,2)

    y = 10^(-n) * round( 10^n * x );

end

