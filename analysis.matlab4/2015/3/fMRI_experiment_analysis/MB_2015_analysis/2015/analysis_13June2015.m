function rd7 = main(opposite,to_show)

	if opposite
		str = 'attend_opposite_x';
	else
		str = 'attend_x';
	end

	if 0
		for i = 1:12
			mi(p_images.imgs(i).img,10,[2,6,i])
			my_imwrite(p_images.imgs(i).img,d2s({i}));
		end

		for i = 1:6
			mi(p_images.imgs(i).img-p_images.imgs(i+6).img,11,[2,6,i+6])
		end

		for i = 1:6
			mi(p_images.imgs(i+6).img-p_images.imgs(i).img,11,[2,6,i])
		end
	end

	%opposite = true;
	if opposite
		fig_offset = 200;
		r1=single(imread('/Users/davidzipser/Desktop/Pictures_Desktop/13June2015_p_images.attend_opposite_x/rotated/1.png'));
		r2=single(imread('/Users/davidzipser/Desktop/Pictures_Desktop/13June2015_p_images.attend_opposite_x/rotated/2.png'));
		r3=single(imread('/Users/davidzipser/Desktop/Pictures_Desktop/13June2015_p_images.attend_opposite_x/rotated/3.png'));
		r4=single(imread('/Users/davidzipser/Desktop/Pictures_Desktop/13June2015_p_images.attend_opposite_x/rotated/4.png'));
		r5=single(imread('/Users/davidzipser/Desktop/Pictures_Desktop/13June2015_p_images.attend_opposite_x/rotated/5.png'));
		r6=single(imread('/Users/davidzipser/Desktop/Pictures_Desktop/13June2015_p_images.attend_opposite_x/rotated/6.png'));
		r7=single(imread('/Users/davidzipser/Desktop/Pictures_Desktop/13June2015_p_images.attend_opposite_x/rotated/7.png'));
		r8=single(imread('/Users/davidzipser/Desktop/Pictures_Desktop/13June2015_p_images.attend_opposite_x/rotated/8.png'));
		r9=single(imread('/Users/davidzipser/Desktop/Pictures_Desktop/13June2015_p_images.attend_opposite_x/rotated/9.png'));
		r10=single(imread('/Users/davidzipser/Desktop/Pictures_Desktop/13June2015_p_images.attend_opposite_x/rotated/10.png'));
		r11=single(imread('/Users/davidzipser/Desktop/Pictures_Desktop/13June2015_p_images.attend_opposite_x/rotated/11.png'));
		r12=single(imread('/Users/davidzipser/Desktop/Pictures_Desktop/13June2015_p_images.attend_opposite_x/rotated/12.png'));
		img1 = imread('/Users/davidzipser/Desktop/Artists/Nakayama/1b.png');
		img1(190:194,254:258,:)=0;
		img1_outlines = get_outlines(img1);
		dots1 = get_dots(img1_outlines);
		img7 = imread('/Users/davidzipser/Desktop/Artists/Nakayama/7b.png');
		img7(190:194,254:258,:)=0;
		img7_outlines = get_outlines(img7);
		dots7 = get_dots(img7_outlines);
		dots1_7 = dots1+dots7;
		img2 = imread('/Users/davidzipser/Desktop/Artists/Nakayama/2b.png');
		img2(190:194,254:258,:)=0;
		img8 = imread('/Users/davidzipser/Desktop/Artists/Nakayama/8b.png');
		img8(190:194,254:258,:)=0;
	else 	
		fig_offset = 100;
		r1=single(imread('/Users/davidzipser/Desktop/Pictures_Desktop/13June2015_p_images.attend_x/rotated/1.png'));
		r2=single(imread('/Users/davidzipser/Desktop/Pictures_Desktop/13June2015_p_images.attend_x/rotated/2.png'));
		r3=single(imread('/Users/davidzipser/Desktop/Pictures_Desktop/13June2015_p_images.attend_x/rotated/3.png'));
		r4=single(imread('/Users/davidzipser/Desktop/Pictures_Desktop/13June2015_p_images.attend_x/rotated/4.png'));
		r5=single(imread('/Users/davidzipser/Desktop/Pictures_Desktop/13June2015_p_images.attend_x/rotated/5.png'));
		r6=single(imread('/Users/davidzipser/Desktop/Pictures_Desktop/13June2015_p_images.attend_x/rotated/6.png'));
		r7=single(imread('/Users/davidzipser/Desktop/Pictures_Desktop/13June2015_p_images.attend_x/rotated/7.png'));
		r8=single(imread('/Users/davidzipser/Desktop/Pictures_Desktop/13June2015_p_images.attend_x/rotated/8.png'));
		r9=single(imread('/Users/davidzipser/Desktop/Pictures_Desktop/13June2015_p_images.attend_x/rotated/9.png'));
		r10=single(imread('/Users/davidzipser/Desktop/Pictures_Desktop/13June2015_p_images.attend_x/rotated/10.png'));
		r11=single(imread('/Users/davidzipser/Desktop/Pictures_Desktop/13June2015_p_images.attend_x/rotated/11.png'));
		r12=single(imread('/Users/davidzipser/Desktop/Pictures_Desktop/13June2015_p_images.attend_x/rotated/12.png'));
		img1 = imread('/Users/davidzipser/Desktop/Artists/Nakayama/1a.png');
		img1(190:194,254:258,:)=0;
		img1_outlines = get_outlines(img1);
		dots1 = get_dots(img1_outlines);
		img7 = imread('/Users/davidzipser/Desktop/Artists/Nakayama/7a.png');
		img7(190:194,254:258,:)=0;
		img7_outlines = get_outlines(img7);
		dots7 = get_dots(img7_outlines);
		dots1_7 = dots1+dots7;
		img2 = imread('/Users/davidzipser/Desktop/Artists/Nakayama/2a.png');
		img2(190:194,254:258,:)=0;
		img8 = imread('/Users/davidzipser/Desktop/Artists/Nakayama/8a.png');
		img8(190:194,254:258,:)=0;
	end	


	if nargin == 2
		out_img = apply_dots(to_show,dots7);
		my_imwrite(out_img,d2s({'all_difference'}));
		mi(out_img,15+fig_offset,[1,1,1])
		mi(subimage2(img7),1);

		return
    end	
	

	rd1 = r1+r3+r4+r6;
	rd2 = r7+r9+r10+r12;
	rd3 = r2+r5;
	rd4 = r8+r11;
	rd5 = r7+r9+r10+r12-(r1+r3+r4+r6);
	rd6 = r8+r11-(r2+r5);
	rd7 = (r7+r9+r10+r12)/4-(r1+r3+r4+r6)/4+(r8+r11)/2-(r2+r5)/2;

	% mi(apply_dots(rd1,dots1),12+fig_offset,[2,3,2])
	% mi(apply_dots(rd2,dots7),12+fig_offset,[2,3,1])
	% mi(apply_dots(rd5,dots1_7),12+fig_offset,[2,3,3])
	% mi(img7,12+fig_offset,[2,3,4])
	% mi(img1,12+fig_offset,[2,3,5])

	% mi(apply_dots(rd3,dots1),13+fig_offset,[2,3,2])
	% mi(apply_dots(rd4,dots7),13+fig_offset,[2,3,1])
	% mi(apply_dots(rd6,dots7),13+fig_offset,[2,3,3])
	% mi(img8,13+fig_offset,[2,3,4])
	% mi(img2,13+fig_offset,[2,3,5])

	mi(apply_dots(rd7,dots7)/2,15+fig_offset,[1,1,1])
	mi(subimage2(img1),1);


% a = zeroToOneRange(sqsing(GD.stimTrn512_int8(1,:,:)));
% b = zeroToOneRange(sqsing(GD.stimTrn512_int8(1750,:,:)));
c={{{1+zeros(2*384,3*512,3,'uint8')},{0 0}},...
	{{apply_dots(rd2,dots7)},{0 0}},...
	{{apply_dots(rd1,dots1)},{0 512}},...
	{{apply_dots(rd5,dots1_7)},{0 2*512}},...
	{{zeroToOneRange(img7)},{384 0}},...
	{{zeroToOneRange(img1)},{384 1*512}},...
};
d = compose_image(c);
mi(d,1+fig_offset);
my_imwrite(d,d2s({str '.vertical'}))

e={{{1+zeros(2*384,3*512,3,'uint8')},{0 0}},...
	{{apply_dots(rd4,dots7)},{0 0}},...
	{{apply_dots(rd3,dots1)},{0 512}},...
	{{apply_dots(rd6,dots1_7)},{0 2*512}},...
	{{zeroToOneRange(img8)},{384 0}},...
	{{zeroToOneRange(img2)},{384 1*512}},...
};
f = compose_image(e);
mi(f,2+fig_offset);
my_imwrite(f,d2s({str '.horizontal'}))



end

%	img1 = imread('/Users/davidzipser/Desktop/Artists/Nakayama/7.png');
function img1_outlines = get_outlines(img1)
	%mi(img1,1,[1,2,1]);
	img1_outlines = 0*img1(:,:,1);
	img1_outlines(find(img1(:,:,1)<100)) = 1;
	%mi(img1_outlines,1,[1,2,2]);
end

function dots = get_dots(img1_outlines)
	ctr = 0;

	dots = zeros(512,512,'uint8');
	for x = 1:384
		for y = 1:512
			if img1_outlines(x,y)>0
				ctr = ctr + 1;
				if ctr > 0%5
					dots(64+x,y) = 1;
					ctr = 0;
				end
			end
		end
	end
	%mi(dots,9);
end

function s = subimage(R1)
	q = 15;
	s = R1((q+64):(64+384-q),q:(512-9),:);
end
function s = subimage2(R1)
	q = 15;
	s = R1((q):(384-q),q:(512-9),:);
end

function R1 = apply_dots(r,dots)
	%r = (r7+r9+r10+r12)/4-(r1+r3+r4+r6)/4+(r8+r11)/2-(r2+r5)/2;
	r = 255*zeroToOneRange(single(r));
	R1 = zeros(512,512,3,'uint8');
	R1(:,:,1)  = imresize(r,4);
	R1(:,:,2)  = R1(:,:,1);
	R1(:,:,3)  = R1(:,:,1);
	R1(:,:,1) = R1(:,:,1) .* (1-dots);
	R1(:,:,2) = R1(:,:,2) .* (1-dots);
	R1(:,:,3) = R1(:,:,3) .* (1-dots);
	R1(:,:,1) = R1(:,:,1) + 255*dots;
	
	R1 = zeroToOneRange(subimage(R1));

	%mi(R1,10);
end