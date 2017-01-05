% addpath('/Users/davidzipser/Google_Drive/Data/stimuli/2015/2/fMRI project/sources')
% s=stereogram(imread('DMperson400.jpg'));mi(s,1)
% stereogram(imread('DMperson400.jpg'));mi(s,1)
% p=imread('DMperson400.jpg'));
% p=imread('DMperson400.jpg');
% size(p)
% p = squeeze(p(:,:,1))
% stereogram(p)
% p=zeroToOneRange(single(p))*15-15;
% stereogram(p)
% stereogram(-p)
% p=zeroToOneRange(single(p))*10-10;stereogram(-p);
% p=zeroToOneRange(single(p))*10-10;for i = 1:1000;stereogram(-p);pause(1/5);end
clc
if 0
	pb=imread('DMperson400b.jpg');
	pb=squeeze(pb(:,:,1));
	pb=zeroToOneRange(single(pb))*10-10;
	for i = 1:1000
		m=my_stereogram(-p);
		m=place_img_A_in_img_B_v2(m,zeros(768,1024,'single')+0.5,0,0);
		mi(m,2,[1,1,1],d2s({i}));
		pause(1/5);
	end
end

if 0
	if not(exist('person'))
		person = imread('~/Data/stimuli/2015/3/stereo/DMperson400.jpg');
		person = squeeze(person(:,:,1));
		building = imread('~/Data/stimuli/2015/3/stereo/DMbuildingORIG.jpg');
		building = squeeze(building(:,:,1));
		building = imresize(building,0.5);
		scene = imread('~/Data/stimuli/2015/3/stereo/zdepth_1_crop.jpg');
		scene = squeeze(scene(:,:,1));
		scene = imresize(scene, 0.6);

		person_flip = fliplr(person);
		building_flip = fliplr(building);
		scene_flip = fliplr(scene);

		mi(person,1,[1,3,1],d2s({size(person)}));
		mi(building,1,[1,3,2],d2s({size(building)}));
		mi(scene,1,[1,3,3],d2s({size(scene)}));
	end




		video_name1 = 'stereo12Mar2015';
		mkdir(d2s({'~/Desktop/' video_name1 '.' now}));
		outputVideo1 = VideoWriter(d2s({'~/Desktop/' video_name1 '.' now '/' video_name1 '.' now '.avi'}),'Motion JPEG AVI');%'Uncompressed AVI');%
		outputVideo1.FrameRate = 5;
		outputVideo1.Quality = 99;
		open(outputVideo1);
		video_name2 = 'depthmap12Mar2015';
		mkdir(d2s({'~/Desktop/' video_name2 '.' now}));
		outputVideo2 = VideoWriter(d2s({'~/Desktop/' video_name2 '.' now '/' video_name2 '.' now '.avi'}),'Motion JPEG AVI');%'Uncompressed AVI');%
		outputVideo2.FrameRate = 5;
		outputVideo2.Quality = 75;
		open(outputVideo2);





	depth_maps = {person,person_flip,building, building_flip,scene,scene_flip};
	blank = zeros(768,1024,'single')+0.5;
	for i = 1:10
		randperm_depth_maps = randperm(length(depth_maps));
		for j = 1:length(depth_maps)
			p = imresize(depth_maps{randperm_depth_maps(j)},(1+0.5*rand(1)));
			x1=round(size(p,1)/2-200);
			x2=x1+400-1;
			p2 = p(x1:x2,x1:x2);
			size(p2)
			mi(p2,1,[1,3,1],d2s({size(p2)}));
			%pause(1);
			pb=zeroToOneRange(single(p2))*10-10;
			for k = 1:(5*5)
				m=my_stereogram(-pb);
				m=place_img_A_in_img_B_v2(m,blank,0,0);
				p3=place_img_A_in_img_B_v2(zeroToOneRange(p2),blank,0,0);
				writeVideo(outputVideo1,m);
				writeVideo(outputVideo2,p3);

				mi(m,2,[1,1,1],d2s({i}));
				mi(p3,3,[1,1,1],d2s({i}));
				drawnow;%pause(1/5);
			end
		end
	end

	close(outputVideo1);
	close(outputVideo2);
end


if 0
	f = 1; g = 2; b = 3;
	img_class = 0*(1:60);
	ctr = 0;
	for i = 1:25:1500
		ctr = ctr + 1;
		mi(imread(d2s({'/Users/davidzipser/Google_Drive/Data/stimuli/2015/3/stereo/depthmap12Mar2015.avi_images/' i '.png'})),1,[1,1,1],d2s({i}));
		img_class(i) = input('f g b');
	end
end

if 0
	img_60_class = 0*(1:60);
	ctr = 0;
	for i = 1:25:1500
		ctr = ctr + 1;
		mi(imread(d2s({'/Users/davidzipser/Google_Drive/Data/stimuli/2015/3/stereo/depthmap12Mar2015.avi_images/' i '.png'})),1,[1,1,1],d2s({i}));
		img_60_class(ctr) = img_class(i);
		if img_60_class(ctr) == 1
			str = 'FACE';
		elseif img_60_class(ctr) == 2
			str = 'GLASS';
		elseif img_60_class(ctr) == 3
			str = 'BUILDING';
		else
			error('unknown');
		end
		title(d2sp({ctr str}));
		pause
	end
end
if 0
	tr_class = 0*(1:340);
	for tr = 1:340
		t = (tr)*0.9;
		tr_60 = floor(t/5+1);
		if tr_60 <= 60
			tr_class(tr) = img_60_class(tr_60);
		end
	end
end
if 0
	face_trs = 0*tr_class;
	glass_trs = 0*tr_class;
	building_trs = 0*tr_class;
	for i = 1:length(tr_class)
		if tr_class(i)==1
			face_trs(i) = 1;
		end
		if tr_class(i)==2
			glass_trs(i) = 1;
		end
		if tr_class(i)==3
			building_trs(i) = 1;
		end
	end
end
if 1
	fileID = fopen('~/Desktop/building.txt','w');
	class_trs = building_trs;
	for i = 1:length(tr_class)
		fprintf(fileID,'%d\n',class_trs(i));
	end
	fclose(fileID);
end


