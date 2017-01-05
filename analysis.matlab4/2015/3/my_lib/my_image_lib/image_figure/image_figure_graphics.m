function image_figure_graphics( ifa, opt_fig )
%function image_figure_graphics( ifa )
%   23 Oct. 2014
    if nargin < 2
        opt_fig = 999;
    end
    
    r = 3; c = 3; sp = 1;
    mi(ifa.input_img,opt_fig,[r,c,sp]);  sp=sp+1;
    fsp(opt_fig,[r c sp]); sp=sp+1;
    hist(ifa.input_values,100);
    mi(ifa.high_res_scalebar,opt_fig,[r,c,sp],d2c({sigfig(ifa.min_val,2), sigfig(ifa.mid_val,2), sigfig(ifa.max_val,2)})); sp=sp+1;
    mp({ifa.high_res_scalebar','o'},opt_fig,[r,c,sp]); sp=sp+1;
    mi(ifa.high_res_img,opt_fig,[r,c,sp]); sp=sp+1;

end

