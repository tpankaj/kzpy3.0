%d = dir('/Users/davidzipser/Desktop/Archive/preprocessfigures/EPIfinal/*.png');
if 0
	dir_str = '/Users/davidzipser/Desktop/Archive/preprocessfiguresFMAP/EPIfinal/';
	d = dir([dir_str '*.png']);

	for i = 1:length(d)
		imgs(i,:,:) = imread(d2s({dir_str d(i).name}));
	end

	%imgs_original = imgs;
	%imgs_FM = imgs;
end

if 0
	imgs_str = 'imgs_FM';
	eval(d2s({'imgs = double(' imgs_str ');'}));
	c_img = double(0*squeeze(imgs(1,:,:)));
	for i = 1:size(imgs,1)
		i
		for j = 1:1:size(imgs,1)
			if ~(i==j)
				c_img = c_img + squeeze(imgs(i,:,:).*imgs(j,:,:));
			end
		end
	end
	mi(c_img,1,[1,1,1],imgs_str);
end
%c_img_original = c_img;
%c_img_FM = c_img;

if 0
	imgs_str = 'imgs_FM';
	eval(d2s({'imgs = double(' imgs_str ');'}));
	for i = 1:size(imgs,1)
		mi(imgs(i,:,:),1,[1,1,1],imgs_str);
		axis([100,400,100,400]);
		pause;
	end
end

