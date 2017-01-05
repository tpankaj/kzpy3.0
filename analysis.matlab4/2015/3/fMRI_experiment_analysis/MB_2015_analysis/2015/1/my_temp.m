for i = 1:100
	image_num = randi(1750);
	image = get_Kay_image('Trn',image_num);
	mi(image,1,[1,1,1],d2s({image_num}));
    pause
end