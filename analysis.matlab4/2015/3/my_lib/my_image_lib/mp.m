function mp( plot_args, figure_num, subplot_array, img_title, img_xlabel, img_ylabel, img_axis )
%function mp( plot_args, figure_num, subplot_array, img_title, img_xlabel, img_ylabel )
%   16 Feb. 2014

    if nargin > 1
      figure( figure_num )
    else
        figure(gcf)
    end

    if nargin > 2
      subplot( subplot_array(1), subplot_array(2), subplot_array(3));
    end

    eval_str = 'plot(';
    for i = 1:length(plot_args)
        eval_str = [eval_str d2s({'plot_args{' i '}' })];
        if i < length(plot_args)
            eval_str = [eval_str ','];
        else
            eval_str = [eval_str ');'];
        end
    end
    eval(eval_str);
    % if length(plot_args) == 1
    %     plot( plot_args{1} );
    % elseif length(plot_args) == 2
    %     plot( plot_args{1}, plot_args{2} );
    % elseif length(plot_args) == 3
    %     plot( plot_args{1}, plot_args{2}, plot_args{3} );
    % elseif length(plot_args) == 4
    %     plot( plot_args{1}, plot_args{2}, plot_args{3} );
    % else
    %     error( 'length(plot_args) > 3' );
    % end

    if nargin > 3
        my_title( strrep(img_title, '_', '\_') );
    end

    if nargin > 4
        xlabel( strrep(img_xlabel, '_', '\_') );
    end

    if nargin > 5
        ylabel( strrep(img_ylabel, '_', '\_') );
    end

    if nargin > 6
        axis(img_axis);
    end

end

