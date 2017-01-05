function ifa = image_figure_process2( ifa )    
global G;

        G.temp.temp_image_file_counter = G.temp.temp_image_file_counter + 1;
        vx = d2s({'temp.',G.temp.temp_image_file_counter});
        
        inch_scale = ifa.inch_scale;
        ifa.texts = {};
        texts_counter = 0;
        
        img_wid = ifa.high_res_img_size(1);
        txt_wid = img_wid/4;
        
        ifa.high_res_img_file_path = my_imwrite_alpha( ifa.high_res_img, ifa.high_res_mask, d2s({vx,'.high_res_img'}), 'TEMP_PPTX_IMAGES' );
        ifa.image_file_path_names = {};
        ifa.image_file_path_names{1} = ifa.high_res_img_file_path;%{ifa.high_res_scalebar_file_path, };
        
        ifa.image_positions{1} = [0,0,img_wid,img_wid]*inch_scale/img_wid + [ifa.inch_offset(1) ifa.inch_offset(2) 0 0];

        
        
        if length(ifa.title) > 0
            texts_counter = texts_counter + 1;
            ifa.texts{texts_counter} = ifa.title;
            ifa.text_positions{texts_counter} = [0,-txt_wid/2,img_wid,txt_wid/2]*inch_scale/img_wid + [ifa.inch_offset(1) ifa.inch_offset(2) 0 0];
        end

        
        if ifa.include_scalebar
            scale_height = ifa.high_res_scalebar_size(1);
            ifa.high_res_scalebar_file_path = my_imwrite( ifa.high_res_scalebar, d2s({vx,'.high_res_scalebar'}), 'TEMP_PPTX_IMAGES' );
            ifa.image_file_path_names{2} = ifa.high_res_scalebar_file_path;
            ifa.image_positions{2} = [0,img_wid,img_wid,scale_height]*inch_scale/img_wid + [ifa.inch_offset(1) ifa.inch_offset(2) 0 0];
            texts_counter = texts_counter + 1;
            ifa.texts{texts_counter} = sprintf('%1.2f',ifa.min_val);
            ifa.text_positions{texts_counter} = [0-txt_wid/2,scale_height+img_wid,txt_wid,txt_wid/2]*inch_scale/img_wid + [ifa.inch_offset(1) ifa.inch_offset(2) 0 0];
            texts_counter = texts_counter + 1;
            ifa.texts{texts_counter} = sprintf('%1.2f',ifa.max_val);
            ifa.text_positions{texts_counter} = [img_wid-txt_wid/2,scale_height+img_wid,txt_wid,txt_wid/2]*inch_scale/img_wid + [ifa.inch_offset(1) ifa.inch_offset(2) 0 0];
        end



end