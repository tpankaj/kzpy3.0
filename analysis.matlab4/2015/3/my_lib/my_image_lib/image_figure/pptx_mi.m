function ifa = pptx_mi( img, subplot_array, img_title, opt_include_scalebar )
% function ifa = pptx_mi( img, subplot_array, img_title, opt_include_scalebar )
%
% e.g., ifa_array(ctr).ifa = pptx_mi( get_Kay_image('Trn',img), [r c ctr], d2sp({'stimTrn ' img}), false );

    if nargin < 4
      opt_include_scalebar = true;
    end


    ifa = image_figure_arg_struct();
        ifa.include_scalebar = opt_include_scalebar;
    s = 0;
    
    for x = 1:subplot_array(1)
        for y = 1:subplot_array(2)
            s = s + 1;
            if s == subplot_array(3)
                X = x; Y = y;
            end
        end
    end
    
    inches_from_upper_left = 1;
    
    if ifa.include_scalebar
        col_spacer = 0.25;
        row_spacer = 0.25;
    else
        col_spacer = 0.125;
        row_spacer = 0.125;
    end        
    
    ifa.inch_offset = inches_from_upper_left + [(1+col_spacer)*(Y-1) (1+row_spacer)*(X-1)] * ifa.inch_scale;
    ifa.title = img_title;
    ifa.input_img = img;
    ifa = image_figure_process( ifa );
    ifa = image_figure_process2( ifa );

end

