function ifa = image_figure_process( ifa )
%function ifa = image_figure_process( ifa )
%
% This is the first step (image_figure_process2.m is the second step.)
% The process is divided into steps because it gives the option of
% manipulating the results of the first step before processing.
% ifa is a structure, a template of which comes from
% image_figure_arg_struct.m.
%   23 Oct. 2014

    % If a mask radius is specificed, but not a input mask image, then create
    % circular mask.
    if and( length(ifa.input_mask) == 0, ifa.input_mask_radius > 0 )
        ifa.input_mask = mask_surround( square_single_zeros(length(ifa.input_img))+1, ifa.input_mask_radius, 0 );
    end
    
    
    % Input_values are needed for statistics.
    % If there is an input mask, use only unmasked pixels.
    if length(ifa.input_mask) > 0
        ifa.input_values = ifa.input_img(find(ifa.input_mask(:)>0));
    else 
        ifa.input_values = ifa.input_img(:);
    end
    
    
    % Find Input_values statistics.
    ifa.min_val = min(ifa.input_values);
    ifa.max_val = max(ifa.input_values);
    if strcmp(ifa.mid_val_spec, 'median')
        ifa.mid_val = median(ifa.input_values);
    elseif strcmp(ifa.mid_val_spec, 'mean')
        ifa.mid_val = mean(ifa.input_values);
    elseif strcmp(ifa.mid_val_spec, 'middle')
        ifa.mid_val = (ifa.max_val + ifa.min_val)/2;
    elseif strcmp(ifa.mid_val_spec, 'zero')
        ifa.mid_val = 0;
    else
        error('ifa.mid_val_spec unknown option');
    end
    
    % Because of the way images are shown in powerpoint, a low resolution
    % image may optionally be enlarged. Whether or not it is enlarged, it is
    % transfered to ifa.high_res_img.
    ifa.high_res_img = ifa.input_img;
    for i = 1:ifa.high_res_double_factor
        ifa.high_res_img = doubleMatrixSize( ifa.high_res_img );
    end

    % If there is an input mask image, then we need to make a high
    % resolution version of that also.
    if length(ifa.input_mask) > 0
        if length(ifa.high_res_mask) == 0
            if ifa.input_mask_radius == 0
                ifa.high_res_mask = ifa.input_mask;
                for i = 1:ifa.high_res_double_factor
                    ifa.high_res_mask = doubleMatrixSize( ifa.high_res_mask );
                end
            else
                ifa.high_res_mask = mask_surround( 0*ifa.high_res_img+1, ifa.input_mask_radius * 2^ifa.high_res_double_factor, 0 );
            end
        end
    end
    
    ifa.high_res_img_size = size(ifa.high_res_img);
    
    % Prepare a scalebar if needed.
    if ifa.include_scalebar
        
        ifa.high_res_scalebar = zeros(round(ifa.high_res_img_size(1)/10),ifa.high_res_img_size(1),'single') + ifa.mid_val;
        ifa.high_res_scalebar_size = size(ifa.high_res_scalebar);

        y_start = single(round((1/6)*ifa.high_res_scalebar_size(1)));
        y_end = single(round((5/6)*ifa.high_res_scalebar_size(1)));
        x_start = y_start;
        x_end = ifa.high_res_scalebar_size(2) - y_start;

        for x = x_start:x_end
            intensity_value = ifa.min_val + (x-x_start)/(x_end-x_start) * (ifa.max_val-ifa.min_val);
            ifa.high_res_scalebar(y_start:y_end,x) = intensity_value;
        end
    end
    
end

