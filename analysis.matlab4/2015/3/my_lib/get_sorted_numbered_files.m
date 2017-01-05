function [sortedImageNames,imageNumbers] = get_sorted_numbered_files( image_path, file_extension )
% function [sortedImageNames,imageNumbers] = get_sorted_numbered_files( image_path, file_extension )
%
    imageNames = dir(fullfile(image_path,['*.',file_extension]));
    imageNames = {imageNames.name}';
    imageStrings = regexp([imageNames{:}],'(\d*)','match');
    imageNumbers = str2double(imageStrings);
    [~,sortedIndices] = sort(imageNumbers);
%     length(imageNumbers)
%     length(sortedIndices)
%     length(imageNames)
    sortedImageNames = imageNames(sortedIndices);
end