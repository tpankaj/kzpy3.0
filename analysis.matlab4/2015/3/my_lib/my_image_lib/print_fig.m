function print_fig(opt_fig_num,opt_filename_no_extension,opt_folder)

	if nargin < 1
        fig_num = gcf;
    else
        fig_num = opt_fig_num;
    end
    
    if nargin < 2
        filename = d2s({'matlab_figure.' fig_num '.' num2str(now), '.pdf'});%'.eps'});
    else
        filename = d2s({opt_filename_no_extension,'.pdf'});%'.eps'});
    end
    
    if nargin < 3
        folder = '~/Desktop/Pictures_Desktop';
    else
        folder = fullfile('~/Desktop/Pictures_Desktop',opt_folder);
    end
    

    
    l = dir(folder);
    if length(l) == 0
        system(d2s({'mkdir ',folder}));
    end
    
    full_filename = fullfile(folder, filename);
    
    %print( fig_num, '-depsc2', full_filename );
    print( fig_num, '-dpdf', full_filename );
end