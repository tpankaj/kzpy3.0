function my_pause( input_arg )
%function my_pause( input_arg )
%   19 Aug. 2014
    if nargin < 1
      input_arg = 'Hit any key to continue . . .';
    end
    if isstr(input_arg)
        fprintf('%s\n', input_arg);
        pause
    else
        pause(input_arg);
    end
end

