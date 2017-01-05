function big_img = compose_img( img_specification_cell_array )
% function img = compose_img( img_specification_cell_array )
% e.g.,
% a = zeroToOneRange(sqsing(GD.stimTrn512_int8(1,:,:)));
% b = zeroToOneRange(sqsing(GD.stimTrn512_int8(1750,:,:)));
% c={{{zeros(1500,1500,'single')+0.5},{0 0}},{{a},{0 0}},{{b},{0 522}}};
% d = compose_image(c);
% mi(d,1);

% make it act on color images as well

    

    big_img = [];
    
    for i = 1:length(img_specification_cell_array)
        %i
        img = img_specification_cell_array{i}{1}{1};
        size_img = size(img);
        if length(size_img) < 3
            img = gray_image_to_color(img);
        end
        x = img_specification_cell_array{i}{2}{1};
        y = img_specification_cell_array{i}{2}{2};
        big_img((x+1):(x+size_img(1)),(y+1):(y+size_img(2)),:) = img;
        %mi(img,1,[1,2,i],d2c({x y}));
    end
    %mi(big_img,2);
end