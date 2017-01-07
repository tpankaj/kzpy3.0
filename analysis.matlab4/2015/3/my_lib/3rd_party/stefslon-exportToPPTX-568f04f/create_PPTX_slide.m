function create_PPTX_slide(slide_file_path_name, image_file_path_names, image_positions, texts, text_positions)
%function create_PPTX_slide(slide_file_path_name, image_file_path_names, image_positions)%, texts, text_positions)
% e.g., create_PPTX_slide('slide1', {'temp2.png'}, {[0,0,4,4]},{},{});
    isOpen  = exportToPPTX();
    if ~isempty(isOpen),
        % If PowerPoint already started, then close first and then open a new one
        exportToPPTX('close');
    end

    exportToPPTX('new');
    exportToPPTX('addslide');

    for i = 1:length(image_file_path_names)
        exportToPPTX('addpicture',image_file_path_names{i});%,'Position',image_positions{i});
    end

	for i = 1:length(texts)
        exportToPPTX('addtext', texts{i},'Position', text_positions{i}, 'Vert', 'top');
    end

    %exportToPPTX('addtext','Inserted via filename, no aspect ratio','Position',[6 3 3 0.5],'Vert','bottom');

    newFile = exportToPPTX('save', slide_file_path_name);

    exportToPPTX('close');

    fprintf('New file has been saved: %s\n',newFile);

end

