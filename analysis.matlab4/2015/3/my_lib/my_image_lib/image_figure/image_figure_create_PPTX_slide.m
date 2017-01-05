function image_figure_create_PPTX_slide(slide_file_path_name, ifa_array, controling_file, comments, slide_title )
% image_figure_create_PPTX_slide(slide_file_path_name, ifa_array, controling_file, comments)
%

    isOpen  = exportToPPTX();
    if ~isempty(isOpen),
        % If PowerPoint already started, then close first and then open a new one
        exportToPPTX('close');
    end

    if length(dir(slide_file_path_name)) == 0
        exportToPPTX('new',slide_file_path_name);
        exportToPPTX('addslide');
    else
        exportToPPTX('open',slide_file_path_name);
        exportToPPTX('addslide','Position',1);
    end
    
    for j = 1:length(ifa_array)
        
        ifa = ifa_array(j).ifa;
        
        for i = 1:length(ifa.image_file_path_names)
            exportToPPTX('addpicture',ifa.image_file_path_names{i},'Position',ifa.image_positions{i});
        end

        for i = 1:length(ifa.texts)
            exportToPPTX('addtext', ifa.texts{i},'Position', ifa.text_positions{i}, 'Vert', 'top', 'FontSize', 9);
        end

    end
    
    exportToPPTX('addtext', [ datestr(now,'mmmm dd, yyyy HH:MM:SS.FFF AM'), ' ', controling_file ],'Position', [0 0 10 0.3], 'Vert', 'top', 'FontSize',9,'Color',[0.5 0.5 0.5]);

    exportToPPTX('addtext', slide_title,'Position', [0 0.2 10 0.5], 'Vert', 'top', 'FontSize',15,'Color',[0 0 0]);
    
    exportToPPTX('addtext', comments,'Position', [-5.25 0 5 20], 'Vert', 'top', 'FontSize', 5, 'Color',[0 0 0], 'BackgroundColor',[1 1 1]);
    
    newFile = exportToPPTX('save', slide_file_path_name);

    exportToPPTX('close');
    
    system('rm ~/Desktop/Pictures_Desktop/TEMP_PPTX_IMAGES/*.png');
    
    fprintf('File has been saved: %s\n',newFile);

end


