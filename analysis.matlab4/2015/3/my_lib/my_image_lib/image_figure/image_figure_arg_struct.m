function ifa = image_figure_arg_struct()

    % set these to reasonable default values
    %
    ifa.inch_scale = 2;
    ifa.input_img = [];
    ifa.input_mask = [];
    ifa.input_mask_radius = 0;
    ifa.high_res_double_factor = 0;
    ifa.include_scalebar = true;
    ifa.mid_val_spec = 'middle';
    %
    %%%%%%%%%
    
    ifa.text.strs = {};
    ifa.text.positions = {};
    
    
    
        ifa.input_values = [];
            ifa.min_val = nan;
            ifa.max_val = nan;
            ifa.mid_val = nan;
            ifa.high_res_scalebar = [];
            
        ifa.high_res_img = [];
        ifa.high_res_mask = [];
    
end