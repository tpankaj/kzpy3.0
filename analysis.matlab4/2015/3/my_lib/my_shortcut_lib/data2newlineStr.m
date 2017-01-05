function str = data2newlineStr( input_cell )
%function str = data2str( input_cell )
%   18 August 2014
%str = data2spacedStr( input_cell );
    str = '';
    for i = 1:length(input_cell)
        t = input_cell{i};
        if isnumeric(t)
            str = [str, sprintf('%s\n',num2str(t))];
        elseif isstr(t)
            str = [str, sprintf('%s\n',t)];
        else
            error('what is it?');
        end
    end
end

