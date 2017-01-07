isOpen  = exportToPPTX();
if ~isempty(isOpen),
    % If PowerPoint already started, then close first and then open a new one
    exportToPPTX('close');
end

exportToPPTX('new');
exportToPPTX('addslide');

exportToPPTX('addpicture','temp2.png','Position',[1 1 2 2]);
exportToPPTX('addpicture','temp2.png','Position',[4 1 2 2]);
exportToPPTX('addpicture','temp2.png','Position',[1 4 2 2]);
exportToPPTX('addpicture','temp2.png','Position',[4 4 2 2]);
exportToPPTX('addtext','Inserted via filename, no aspect ratio','Position',[6 3 3 0.5],'Vert','bottom');

exportToPPTX('save','example');

exportToPPTX('close');

fprintf('New file has been saved: <a href="matlab:winopen(''%s'')">%s</a>\n',newFile,newFile);

