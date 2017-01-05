if 0
	num_images = 12;
	ms_timing = zeros(num_images,340*900);

	bp = (6*1000);
	for img_num = 1:num_images
		for repeats = 1:4
			ms_timing(img_num,( 2*6*6*1000*(repeats-1) + bp+1+(img_num-1)*bp):( 2*6*6*1000*(repeats-1) + bp+(img_num-1)*bp+(4*1000))) = 1;
		end
	end
	plot(ms_timing(12,1:100:size(ms_timing,2)),'g');



	attention_reading_design_TRs = zeros(340,num_images);
	ctr = 0;
	for t = 1:900:(340*900)
		ctr = ctr + 1;
		for i = 1:num_images
			attention_reading_design_TRs(ctr,i) = ms_timing(i,t);
		end
	end
	ctr
	plot(attention_reading_design_TRs);
end


if 0 % not finished
	num_images = 4;
	ms_timing = zeros(num_images,340*900);

	bp = (6*1000);
	for img_num = 1:num_images
		for repeats = 1:9
			ms_timing(img_num,( 2*6*6*1000*(repeats-1) + 4000 +1+(img_num-1)*bp):( 2*6*6*1000*(repeats-1) + bp+(img_num-1)*4000+(4*1000))) = 1;
		end
	end

	RF_design_TRs = zeros(340,num_images);
	ctr = 0;
	for t = 1:900:(340*900)
		ctr = ctr + 1;
		for i = 1:num_images
			RF_design_TRs(ctr,i) = ms_timing(i,t);
		end
	end
	ctr
	plot(RF_design_TRs);
end

