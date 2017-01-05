function str = data2spacedStr( input_cell )
%function str = data2spacedStr( input_cell )
% 18 Aug. 2014
    str = '';
    for i = 1:length(input_cell)
        t = input_cell{i};
        if isnumeric(t)
            str = [str, num2str(t)];
        elseif isstr(t)
            str = [str, t];
        else
            error('what is it?');
        end
        if i < length(input_cell)
            str = [str, ' '];
        end
    end
end

