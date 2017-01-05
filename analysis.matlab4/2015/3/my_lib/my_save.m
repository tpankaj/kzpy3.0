function my_save(data, data_name, opt_filename_no_extension,opt_folder)
%function my_save(data, data_name, opt_filename_no_extension,opt_folder)
% 11 Sept. 2014

    eval(d2s({data_name,' = data;'}));
    
    if nargin < 4
        folder = '~/Desktop/Matlab_Desktop';
    else
        folder = fullfile('~/Desktop/Matlab_Desktop',opt_folder);
    end
    
    if nargin < 3
        filename = d2s({data_name, '.', num2str(now), '.mat'});
    else
        filename = d2s({opt_filename_no_extension,'.mat'});
    end
    
    l = dir(folder);
    if length(l) == 0
        system(d2s({'mkdir ',folder}));
    end
    
    S = whos(data_name);
    if S.bytes > 2000000000
        disp(d2s({'Saving ' filename ' with -v7.3 switch'}));
        save(fullfile(folder, filename), data_name, '-v7.3');
    else
        save(fullfile(folder, filename), data_name);
    end

end
