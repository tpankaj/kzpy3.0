if 0
	plot(times(:,2),times(:,1),'ko')
	size(times)

	one_time_indicies = find(times(:,1)==1);
	two_time_indicies = find(times(:,1)==2);
	one_times = times(one_time_indicies,2);
	two_times = times(two_time_indicies,2);
	one_vals = times(one_time_indicies,1);
	two_vals = times(two_time_indicies,1);


	one_TRs = zeros(1,340);
	two_TRs = zeros(1,340);

	for i = 1:length(one_times)
		one_TRs(round(one_times(i))) = 1;
	end
	for i = 1:length(two_times)
		two_TRs(round(two_times(i))) = 1;
	end


	one_period = false;
	two_period = false;
	for i = 1:340
		if one_TRs(i)==1
			one_period = true;
			two_period = false;
		end
		if two_TRs(i)==1
			one_period = false;
			two_period = true;
		end
		if one_period
			one_TRs(i) = 1;
		end
		if two_period
			two_TRs(i) = 1;
		end
	end

	ca;
	plot((1:340)*0.9/60,one_TRs,'o');
	hold on;
	plot((1:340)*0.9/60,two_TRs,'rx');
	hold off;

	if 0
		dlmwrite('~/Desktop/one_TRs.txt',int8(one_TRs)','delimiter',' ');
		dlmwrite('~/Desktop/two_TRs.txt',int8(two_TRs)','delimiter',' ');
	end
end
if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if not(exist('RF_mapping'))
        load('/Users/davidzipser/Desktop/Matlab_Desktop/HVO_RF_mapping.736027.5901.mat');
        RF_mapping = HVO_RF_mapping;
    end
end
if 1
	SCREEN_MASK_X = 19;
    SCREEN_MASK_Y = 2;
    % SCREEN_MASK_X = 30;
 %    SCREEN_MASK_Y = 30;
    mask = 0*zeros(128,128,'single'); mask((1+SCREEN_MASK_X):(128-SCREEN_MASK_X),(1+SCREEN_MASK_Y):(128-SCREEN_MASK_Y))=1;
    blank = square_single_zeros(512);
    z_img_data = z_scored_20150319_143524mbboldmb620mmAPPSNs010a001.z_img;%z_scored_20150319_082633mbboldmb620mmAPPSNs010a001.z_img;%z_scored_20150318_082104mbboldmb620mmAPPSNs010a001.z_img;%z_scored_20150319_143524mbboldmb620mmAPPSNs022a001.z_img;%z_scored_20150319_082633mbboldmb620mmAPPSNs010a001.z_img;%z_scored_20150319_143524mbboldmb620mmAPPSNs022a001.z_img;
	
	if not(exist('ver_resampled_data'))
		ver_resampled_data = tseriesinterp_selected_voxels(z_img_data, RF_mapping.selected_voxel_xyzs,0.9,5);
	end
	%ver_resampled_data_20150318_082104mbboldmb620mmAPPSNs010a001 = ver_resampled_data;
	%ver_resampled_data_20150319_082633mbboldmb620mmAPPSNs010a001 = ver_resampled_data;
	%ver_resampled_data_20150319_143524mbboldmb620mmAPPSNs010a001 = ver_resampled_data;
	fcs = [];
	fc_img = 0*img;
	for i = (50*5):(1530-30*5)
		j= 1+round(i/5/0.9);
		img = voronoi_P_image( mean(ver_resampled_data(:,i:(i+5*2)),2), RF_mapping.pixel_to_voxel_assignment, 50);
		img=img.*mask;%img(1,1)=2;img(1,2)=-2;
		%mp({img'},1,[2,1,2]);
		%mi_nii(mean(z_scored_20150318_082104mbboldmb620mmAPPSNs010a001.z_img(:,:,:,j:(j+5*2)),4),50,16,13,9,false);
		st = mean(z_scored_20150318_082104mbboldmb620mmAPPSNs010a001.z_img(:,:,:,j:(j+5*2)),4);
		st = squeeze(st(:,:,4:25));
		mi(makeimagestack(st),1,[2,1,2]);
		fc_vxs = [41 32 14;49 32 17;45 32 15;42 32 14];
		fc = 0;
		for u = 1:size(fc_vxs,1)
			xyz = fc_vxs(u,:);
			xyz;
			fc = fc + mean(z_scored_20150319_082633mbboldmb620mmAPPSNs010a001.z_img(xyz(1),xyz(2),xyz(3),j:j+2),4);
		end
		fcs(j) = fc;
		if fc>-1
			fc_img = fc_img + -fc * img;
		end
		img(1,1)=1;img(1,2)=-1;mi(img,1,[2,1,1],d2sp({fc round(i/5)-6}));%,d2sp({one_TRs(round(1+i/5/0.9)) two_TRs(round(1+i/5/0.9)) round(i/5)}));
		pause(1/100);
	end
end
%for i = 1:340;mi(makeimagestack(mean(z_img_data(:,:,:,i:(i+0)),4)),1);title(d2s({round(i*0.9-6)}));pause(0.09);end