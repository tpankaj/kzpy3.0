function full_filename = my_imwrite(data,opt_filename_no_extension,opt_folder)
%function my_imwrite(data,opt_filename_no_extension,opt_folder)
% 11 Sept. 2014
    if nargin < 3
        folder = '~/Desktop/Pictures_Desktop';
    else
        folder = fullfile('~/Desktop/Pictures_Desktop',opt_folder);
    end
    
    if nargin < 2
        filename = d2s({num2str(now),'.png'});
    else
        filename = d2s({opt_filename_no_extension,'.png'});
    end
    
    l = dir(folder);
    if length(l) == 0
        system(d2s({'mkdir ',folder}));
    end
    
    full_filename = fullfile(folder, filename);
    
    if length(size(squeeze(data))) == 2
        imwrite(uint8range(squeeze(data)), full_filename);
    else
        imwrite(squeeze(data), full_filename);
    end
end
