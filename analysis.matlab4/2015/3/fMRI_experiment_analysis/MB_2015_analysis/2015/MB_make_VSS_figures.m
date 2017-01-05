function MB_make_VSS_figures(ver_frames)

	experiments = {...
	'attend_face_or_read',...
	'attend_vase_or_read',...
	'attend_vase_or_face',...
	'attend_object_or_body',...
	'attend_gnd_near_vase_or_face',...
	'fixate_or_read',...
	'attend_scene_or_face'...
	}

	p_image_map = containers.Map;
	p_image_result_map = containers.Map;

    %if not(exist('ver_frames'))
    %    ver_frames = MB_load_frames('vermeer_attention','attend_face_or_read');
    %end

	SCREEN_MASK_X = 19;
	SCREEN_MASK_Y = 2;
	offset = 4 * 5;
	mask = 0*zeros(128,128,'single'); mask((1+SCREEN_MASK_X):(128-SCREEN_MASK_X),(1+SCREEN_MASK_Y):(128-SCREEN_MASK_Y))=1;

	mask512=gray_image_to_color(doubleMatrixSize(doubleMatrixSize(mask)));
	white_bkg= 1-mask512;

	for j = 1:length(experiments)
		e = experiments{j};
		epath = ['~/Desktop/Matlab_Desktop/p_images.' e '.mat']
		load(epath);
		p_image_map(e) = p_images;
	end

	pimgs = []
	for i = 1:6
		pimg = p_image_map('attend_face_or_read').imgs(i).img;
		pimg = pimg + p_image_map('attend_vase_or_face').imgs(i+6).img;
		pimg = pimg + p_image_map('attend_scene_or_face').imgs(i+6).img;
		pimgs(i).img = pimg/3.0
	end
	p_image_result_map('attend_face')=pimgs;

	pimgs = []
	for i = 1:6
		pimg = p_image_map('attend_vase_or_read').imgs(i).img;
		pimg = pimg + p_image_map('attend_vase_or_face').imgs(i).img;
		pimgs(i).img = pimg/2.0
	end
	p_image_result_map('attend_vase')=pimgs;


	pimgs = []
	for i = 1:6
		pimg = p_image_map('attend_face_or_read').imgs(i+6).img;
		pimg = pimg + p_image_map('attend_vase_or_read').imgs(i+6).img;
		pimg = pimg + p_image_map('fixate_or_read').imgs(i+6).img;
		pimgs(i).img = pimg/3.0
	end
	p_image_result_map('read')=pimgs;





	% pimgs = p_image_result_map('attend_face');
	% for i = 1:6
	% 	mi(pimgs(i).img,i,[1,3,1])
	% end

	% pimgs = p_image_result_map('read');
	% for i = 1:6
	% 	mi(pimgs(i).img,i,[1,3,2])
	% end


	for i = 1:6

		final_image = 1+zeros(2*512,3*512,3,'single');

		pimgs = p_image_result_map('attend_face');
	
		f = 6*5+6*5*(i-1)+2;
		p1 = pimgs(i).img;
		vf1 = squeeze(ver_frames(f,:,:,:));

		vf = zeroToOneRange(vf1);
		final_image(1:512,513:1024,:)=vf.*mask512+white_bkg;

		pby = mask512.*BY_p_image(p1,vf1,mask);
		mi(pby,i,[1,3,1])
		final_image(513:1024,1:512,:)=pby+white_bkg;

		pimgs = p_image_result_map('read');

		f = 6*5+6*5*(i-1+6)+2;
		p1 = pimgs(i).img;
		vf1 = squeeze(ver_frames(f,:,:,:));
		pby = mask512.*BY_p_image(p1,vf1,mask);
		mi(pby,i,[1,3,2])
		final_image(513:1024,513:1024,:)=pby+white_bkg;

		pimgs = p_image_result_map('attend_vase');

		f = 6*5+6*5*(i-1)+2;
		p1 = pimgs(i).img;
		vf1 = squeeze(ver_frames(f,:,:,:));
		pby = mask512.*BY_p_image(p1,vf1,mask);
		mi(pby,i,[1,3,3])
		final_image(513:1024,1025:1536,:)=pby+white_bkg;

		mi(final_image,1000,[6,1,i],d2s({i}));
		my_imwrite(final_image,d2s({i '.face.read.vase'}),'VSS_figures_13May2015')

	end


		
		



end


function MB_make_VSS_figures1(ver_frames)

	experiments = {...
	'attend_face_or_read',...
	'attend_vase_or_read',...
	'attend_vase_or_face',...
	'attend_object_or_body',...
	'attend_gnd_near_vase_or_face',...
	'fixate_or_read',...
	'attend_scene_or_face'...
	}


    %if not(exist('ver_frames'))
    %    ver_frames = MB_load_frames('vermeer_attention','attend_face_or_read');
    %end

	for j = 1:length(experiments)
		e = experiments{j};
		epath = ['~/Desktop/Matlab_Desktop/p_images.' e '.mat']
		load(epath);
		MB_make_fig(p_images,ver_frames,j,e)
	end
end

function MB_make_fig(p_images,ver_frames,fig_num,experiment)

	SCREEN_MASK_X = 19;
	SCREEN_MASK_Y = 2;
	offset = 4 * 5;
	mask = 0*zeros(128,128,'single'); mask((1+SCREEN_MASK_X):(128-SCREEN_MASK_X),(1+SCREEN_MASK_Y):(128-SCREEN_MASK_Y))=1;

	mask512=gray_image_to_color(doubleMatrixSize(doubleMatrixSize(mask)));
	white_bkg= 1-mask512;


	ctr = 0;
	for i = 1:6

		f = 6*5+6*5*(i-1)+2;
		p1 = p_images.imgs(i).img;
		vf1 = squeeze(ver_frames(f,:,:,:));
		pimg1 = mask512.*BY_p_image(p1,vf1,mask);

		f = 6*5+6*5*(i+6-1)+2;
		p2= p_images.imgs(i+6).img;
		vf2 = squeeze(ver_frames(f,:,:,:));
		pimg2 = mask512.*BY_p_image(p2,vf2,mask);

		vf = zeroToOneRange(vf1);
		%ctr = ctr +1;
		%mi(pimg1,fg,[6,3,ctr]);
		%ctr = ctr +1;
		%mi(vf,fg,[6,3,ctr]);
		%ctr = ctr +1;
		%mi(pimg2,fg,[6,3,ctr]);

		final_image = zeros(512,3*512,3,'single');
		final_image(1:512,1:512,:)=pimg1+white_bkg;
		final_image(1:512,513:1024,:)=vf.*mask512+white_bkg;
		final_image(1:512,1025:1536,:)=pimg2+white_bkg;
		mi(final_image,fig_num,[6,1,i],experiment);
		my_imwrite(final_image,d2s({experiment '.' i}),'VSS_figures_13May2015')
		%mi(vf,fg+100,[2,6,i]);
	end
end


function ci = BY_p_image(p,vf,mask)

	t = p(mask>0);
	p=p-mean(t);
	p=p/std(t);

	p512 = doubleMatrixSize(doubleMatrixSize(p));

	pn = p512;
	pn(p512>0) = 0;
	pn = -pn;
	pn=zeroToOneRange(pn);
	pp = p512;
	pp(p512<0) = 0;
	pp=zeroToOneRange(pp);

	v = mean(vf,3);

	e = 1.5;
	ci = color_modulation_of_grayscale_image_YB(v,pp.^e,pp.^e,pn.^e,false);
end