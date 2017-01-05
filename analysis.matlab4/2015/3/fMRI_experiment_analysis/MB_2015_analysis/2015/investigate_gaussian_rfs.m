
if 0
	if not(exist('RF_mapping'))
		load('~/Desktop/Matlab_Desktop/HVO_RF_mapping.736252.5459.mat');
		RF_mapping = HVO_RF_mapping;
	end
	if not(exist('localizer2_data'))
		load('/Users/davidzipser/Desktop/Matlab_Desktop/localizer2_data.736023.8621.mat');
	end
end

if 1
	RF_mapping = [];
	RF_mapping.gaussian_r_volume = gaussian_r_volume;
	RF_mapping.gaussians = gaussians;
	RF_mapping.coverage_img = coverage_img;
	RF_mapping.selected_voxel_vol = selected_voxel_vol;
	RF_mapping.selected_voxel_xyzs = selected_voxel_xyzs;
	RF_mapping.voxel_rf_peaks = voxel_rf_peaks;
	RF_mapping.mean_img = z_scored_filtered_func_data.mean_img;
	RF_mapping.subject = 'HVO';
	RF_mapping.pixel_to_voxel_assignment = pixel_to_voxel_assignment;
	my_save(RF_mapping,'HVO_RF_mapping');
end

if 0
	RF_mapping.voxel_orientation_ecc = 0*RF_mapping.voxel_rf_peaks;
	RF_mapping.ecc_vol = 0*zc_sum;
	RF_mapping.ori_vol = 0*zc_sum;
	for i = 1:length(RF_mapping.voxel_rf_peaks)
		xy = RF_mapping.voxel_rf_peaks(i,:);
		[xdeg, ydeg, orientation, eccentricity] = visual_coordinates_from_fixated_image( xy(1),xy(2), 64, 64, 6.4 )
		RF_mapping.voxel_orientation_ecc(i,:) = [orientation,eccentricity];
		xyz = RF_mapping.selected_voxel_xyzs(i,:);
		RF_mapping.ecc_vol(xyz(1),xyz(2),xyz(3)) = eccentricity;
		RF_mapping.ori_vol(xyz(1),xyz(2),xyz(3)) = orientation;
	end
end

if 0 % zc_sum to pycortex format
	data = RF_mapping.ori_vol;
	 temp = find(data>180);
	data(temp) = 360-data(temp);
    zc_sum1 = zeros(60,106,106);
    for z = 1:60
        for x = 1:106
            for y = 1:106
        %zc_sum1(i,:,:) = zc_sum(:,:,i);
                zc_sum1(z,y,x) = data(x,y,z);
            end
        end
    end
    save('~/Desktop/ori_vol.mat','zc_sum1');
end

if 0
	voxel_rf_peaks = zeros(length(selected_voxel_xyzs),2,'single');
	c=gaussian_matrix2(9,1.5);c=c(1:8,1:8);mi(c)
	h = waitbar(0,'processing');movegui('southeast');
	for j = 1:length(selected_voxel_xyzs)
		waitbar(j/length(selected_voxel_xyzs));
		a = selected_voxel_xyzs(j,:);
		b = squeeze(gaussian_r_volume(a(1),a(2),a(3),:));
		img = sqsing(512);
		for i = 1:length(b)
			img = img + (b(i).^4) * gaussians(i).img;
		end
		d = find(b(:)==max(b));
		img_smooth = conv2(zeroToOneRange(img),c,'same');
		[x,y] = get_peak_xy( gaussians(d).img );
		[xp,yp] = get_peak_xy( img_smooth );
		voxel_rf_peaks(j,:) = [xp,yp];
		if 0
			mi(img,10,[1,3,1]);
			mi(img_smooth,10,[1,3,2],d2s({j}));
			mi(gaussians(d).img,10,[1,3,3]);
			fsp(10,[1,3,2]);
			hold on;
			mp({y,x,'o'});
			mp({yp,xp,'rx'});
			hold off;
			fsp(10,[1,3,3]);
			hold on;
			mp({y,x,'o'});
			mp({yp,xp,'rx'});
			hold off;
			% d = squeeze(avg_ori(a(1),a(2),a(3),:));
			% data = tseriesinterp(d,0.9,1/5);
			% mp({data,'o-'},1,[2,1,1])
			% mp({abs(real(fft(data))),'o-'},1,[2,1,2])
			pause;
		end
	end
	close(h);
end

if 0
	pixel_to_voxel_assignment = assign_voxels_to_pixels( voxel_rf_peaks, 128, 100 );
end

if 0
	vermeer_images = zeros(1500,384,512,3,'uint8');
	for i = 1:1500
		vermeer_images(i,:,:,:) = imread(d2s({'/Users/davidzipser/Data/stimuli/2015/2/11Feb2015_Vermeer_reading_videos/vermeer1to10.avi_images/' i '.png'}));
	end
end

if 0
	vdw_images = zeros(1500,384,512,3,'uint8');
	for i = 1:1500
		vdw_images(i,:,:,:) = imresize(imread(d2s({'/Users/davidzipser/Data/experiments/van_der_Weyden_short_presentations/vanDerWeyden1_25Feb2015/movie_frames/' i '.png'})),0.5);
	end
end

if 0
	T=1;%0.25;
	SCREEN_MASK_X = 19;
    SCREEN_MASK_Y = 2;
	% SCREEN_MASK_X = 30;
 %    SCREEN_MASK_Y = 30;
    mask = 0*zeros(128,128,'single'); mask((1+SCREEN_MASK_X):(128-SCREEN_MASK_X),(1+SCREEN_MASK_Y):(128-SCREEN_MASK_Y))=1;
    blank = square_single_zeros(512);
    the_data = localizer2_data{2};
    the_frames = frames;
    offset = 4 * 5;
	for i = 2:1:(size(the_data,2)-offset);
		voxel_responses = sum(the_data(:,(i+offset):(i+offset)),2);
		img = mask .* voronoi_P_image( voxel_responses, RF_mapping.pixel_to_voxel_assignment, 25);
		img(1,1)=T;
		img(1,2)=-T;
		mi( img,1,[1,3,1],d2s({floor((i-1)/5)}));
		if 1
			simg2 = blank+0.5;;

			simg = squeeze(sum(single(the_frames(i,:,:,:)),1));
			simg = simg/ max(max(max(simg)));
			% simg2(64:447,:) = squeeze(simg(:,:,1));
			% simg2 = zeroToOneRange(simg2)-0.5;
			% %simg2(1,1)=0.5;simg2(1,2)=-0.5;
			% simg3 = simg2 .* doubleMatrixSize(doubleMatrixSize(zeroToOneRange(img).^2));
			% simg3 = simg3(120:392,120:392);
			
			% mi( simg3,1,[1,3,2],d2s({floor((i-1)/5)}));
			mi( simg,1,[1,3,2],d2s({floor((i-1)/5)}));
		end
		pause(1/10);
	end
end

if 0
	T=1;%0.25;
	SCREEN_MASK_X = 19;
    SCREEN_MASK_Y = 2;
	% SCREEN_MASK_X = 30;
 %    SCREEN_MASK_Y = 30;
    mask = 0*zeros(128,128,'single'); mask((1+SCREEN_MASK_X):(128-SCREEN_MASK_X),(1+SCREEN_MASK_Y):(128-SCREEN_MASK_Y))=1;
    blank = square_single_zeros(512);
    the_data = localizer2_data{1};%vdw_selected_voxels;%
    offset = 4 * 5;
	for i = 1:1:(size(the_data,2)-offset);
		voxel_responses = the_data(:,i);
		%voxel_responses = sum(the_data(:,(i+offset-5):(i+offset+5)),2)/11;
		% voxel_responses = voxel_responses + the_data(:,360 + i+offset);
		% voxel_responses = voxel_responses + the_data(:,720 + i+offset);
		% voxel_responses = voxel_responses + the_data(:,3*360 + i+offset);
		% voxel_responses = voxel_responses/4;
		%fsp(11,[1,1,1]);hist(voxel_responses,100);axis([-3,3,0,50]);
		%img = mask .* zeroToOneRange(voronoi_P_image( voxel_responses, pixel_to_voxel_assignment, 40)).^2;
		img = mask .* voronoi_P_image( voxel_responses, RF_mapping.pixel_to_voxel_assignment, 25);
		img(1,1)=T;
		img(1,2)=-T;
		mi( img,1,[1,3,1],d2s({floor((i-1)/5)}));
		if 0
			simg2 = blank+0.5;;

			simg = squeeze(sum(single(vdw_images((i-6):(i+6),:,:,:)),1));
			simg = simg/ max(max(max(simg)));
			simg2(64:447,:) = squeeze(simg(:,:,1));
			simg2 = zeroToOneRange(simg2)-0.5;
			%simg2(1,1)=0.5;simg2(1,2)=-0.5;
			simg3 = simg2 .* doubleMatrixSize(doubleMatrixSize(zeroToOneRange(img).^2));
			simg3 = simg3(120:392,120:392);
			
			mi( simg3,1,[1,3,2],d2s({floor((i-1)/5)}));
			mi( simg,1,[1,3,3],d2s({floor((i-1)/5)}));
		end
		pause(1/10);
	end
end

if 0
	data = {}
	data{1} = zeros(length(selected_voxel_xyzs),1500);
	data{2} = zeros(length(selected_voxel_xyzs),1500);
	h=waitbar(0,'procesing...');movegui('southeast');
	for j = 1:length(selected_voxel_xyzs)
		waitbar(j/length(selected_voxel_xyzs));
		a = selected_voxel_xyzs(j,:);
		ori = squeeze(avg_ori(a(1),a(2),a(3),:));
		ori5Hz = tseriesinterp(ori,0.9,1/5);
		ecc = squeeze(avg_ecc(a(1),a(2),a(3),:));
		ecc5Hz = tseriesinterp(ecc,0.9,1/5);
		data{1}(j,:) = ori5Hz(1:1500);
		data{2}(j,:) = ecc5Hz(1:1500);
	end
	close(h);
	localizer2_data = data;
end
if 0
	vermeer_selected_voxels = zeros(length(selected_voxel_xyzs),1500);
	h=waitbar(0,'procesing...');movegui('southeast');
	for j = 1:length(selected_voxel_xyzs)
		waitbar(j/length(selected_voxel_xyzs));
		a = selected_voxel_xyzs(j,:);
		ver = squeeze(avg_vermeer(a(1),a(2),a(3),:));
		ver5Hz = tseriesinterp(ver,0.9,1/5);
		vermeer_selected_voxels(j,:) = ver5Hz(1:1500);
	end
	close(h);
end
if 0
	vdw_selected_voxels = zeros(length(selected_voxel_xyzs),1500);
	h=waitbar(0,'procesing...');movegui('southeast');
	for j = 1:length(selected_voxel_xyzs)
		waitbar(j/length(selected_voxel_xyzs));
		a = selected_voxel_xyzs(j,:);
		vdw = squeeze(avg_vanderweyden(a(1),a(2),a(3),:));
		vdw5Hz = tseriesinterp(vdw,0.9,1/5);
		vdw_selected_voxels(j,:) = vdw5Hz(1:1500);
	end
	close(h);
end
if 0
	load('/Users/davidzipser/Data/stimuli/2015/2/5Feb2015_localizer2/localizer2_orientation_5Feb2015.736000.8698/mat/localizer2_orientation_5Feb2015.texture_energy_images_128.mat');
	ori_texture_energy_images_128 = texture_energy_images_128;
	load('/Users/davidzipser/Data/stimuli/2015/2/5Feb2015_localizer2/localizer2_eccentricity_5Feb2015.736000.8919/mat/localizer2_eccentricity_5Feb2015.texture_energy_images_128.mat');
	ecc_texture_energy_images_128 = texture_energy_images_128;


	kay_compatible_stimulus{1} = zeros(128,128,1500,'single');
	kay_compatible_stimulus{2} = zeros(128,128,1500,'single');

	for i = 1:1500
		kay_compatible_stimulus{1}(:,:,i) = ori_texture_energy_images_128(i,:,:);
		kay_compatible_stimulus{2}(:,:,i) = ecc_texture_energy_images_128(i,:,:);
	end
end

if 0
	data_subset = {};
	data_subset{1}=localizer2_data{1}(1:10,:);
	data_subset{2}=localizer2_data{2}(1:10,:);
	results = analyzePRF(kay_compatible_stimulus,data_subset,1,struct('seedmode',[0 1],'display','off'));

	%% Inspect the results

	% The stimulus is 100 pixels (in both height and weight), and this corresponds to
	% 10 degrees of visual angle.  To convert from pixels to degreees, we multiply
	% by 10/100.
	cfactor = 10/100;

	% Visualize the location of each voxels pRF
	figure; hold on;
	set(gcf,'Units','points','Position',[100 100 400 400]);
	cmap = jet(size(results.ang,1));
	for p=1:size(results.ang,1)
	  xpos = results.ecc(p) * cos(results.ang(p)/180*pi) * cfactor;
	  ypos = results.ecc(p) * sin(results.ang(p)/180*pi) * cfactor;
	  ang = results.ang(p)/180*pi;
	  sd = results.rfsize(p) * cfactor;
	  h = drawellipse(xpos,ypos,ang,2*sd,2*sd);  % circle at +/- 2 pRF sizes
	  set(h,'Color',cmap(p,:),'LineWidth',2);
	  set(scatter(xpos,ypos,'r.'),'CData',cmap(p,:));
	end
	drawrectangle(0,0,10,10,'k-');  % square indicating stimulus extent
	axis([-10 10 -10 10]);
	straightline(0,'h','k-');       % line indicating horizontal meridian
	straightline(0,'v','k-');       % line indicating vertical meridian
	axis square;
	set(gca,'XTick',-10:2:10,'YTick',-10:2:10);
	xlabel('X-position (deg)');
	ylabel('Y-position (deg)');
	%%

	% Please see the example2.m script for an example of how to inspect the model fit 
	% and compare it to the data.
end

if 0
	results = analyzePRF(kay_compatible_stimulus,localizer2_data,1,struct('seedmode',[0 1],'display','off'));
end
