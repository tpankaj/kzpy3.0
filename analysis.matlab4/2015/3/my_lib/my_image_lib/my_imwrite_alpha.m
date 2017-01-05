function full_filename = my_imwrite_alpha(data, mask, opt_filename_no_extension,opt_folder)
%function my_imwrite(data,opt_filename_no_extension,opt_folder)
% 11 Sept. 2014

    
    
    if nargin < 4
        folder = '~/Desktop/Pictures_Desktop';
    else
        folder = fullfile('~/Desktop/Pictures_Desktop',opt_folder);
    end
    
    if nargin < 3
        filename = d2s({num2str(now),'.png'});
    else
        filename = d2s({opt_filename_no_extension,'.png'});
    end
    

   mask = uint8range(mask);


    l = dir(folder);
    if length(l) == 0
        system(d2s({'mkdir ',folder}));
    end
    
    full_filename = fullfile(folder, filename);
    
    if length(mask) == 0
        if length(size(squeeze(data))) == 2
            imwrite(uint8range(squeeze(data)), full_filename );
        else
            imwrite(squeeze(data), full_filename );
        end
    else
        if length(size(squeeze(data))) == 2
            imwrite(uint8range(squeeze(data)), full_filename, 'Alpha', mask);
        else
            imwrite(squeeze(data), full_filename, 'Alpha', mask);
        end
    end
        
end
