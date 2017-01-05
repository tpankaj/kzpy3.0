function [indicies,names] = get_set_of_indicies2_2( total_path, extension_str )
%function set_of_indicies = get_set_of_indicies2_2( total_path, extension_str )
%   16 Feb. 2014

    %'get_set_of_indicies2_2'

    listing = dir( fullfile(total_path, ['*.', extension_str ]) );
    indicies = zeros(length(listing),1);
    names = {};
    for i = 1:length(listing)
        %listing(i).name
        indicies(i) = get_index_from_filename( listing( i ).name, extension_str );
        names{i} = listing(i).name;
    end
    set_of_indicies = unique(indicies);
    if length(set_of_indicies) ~= length(indicies)
        error('if length(set_of_indicies) ~= length(indicies)');
    end
end