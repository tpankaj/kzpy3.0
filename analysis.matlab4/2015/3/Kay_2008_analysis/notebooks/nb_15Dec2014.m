clc; fprintf('%s\n',[mfilename ' (' mfilename('fullpath') '.m)']);


if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    global G;
    E = G.constants.KAY_2008;
    V = G.e(E).constants.NOV_2013_COMBINED_TRIALS
    VAL = G.e(E).constants.VAL;
    TRN = G.e(E).constants.TRN;
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %load_subject_data_Kay_2008( 2, 2 )
    S = G.e(E).v(V).s(2);

    for i = 1:1750

        display_brain_slices_general('Kay 2008',S.subject,d2s({'VAL ' i}),...
            S.stim(VAL).data(:,i),S.scanner_XYZs_to_voxel_index,...
            1,4,28,0);

        pause%(4);

    end
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    v = 26154;%50228;%49869; %50038;
     
    rf = zeros(128^2,1,'single');
    voxel_responses = G.e(1).v(2).s(1).stim(1).data(v,1:1750);
    %pixel_values = sqrt(pixel_values);
    for i = 1:(128^2)

        cc = corrcoef( voxel_responses, pixel_values(:,i) );
        rf(i) = cc(1,2);
    end

    rf = reshape(rf,128,128)';
    mi(rf,v+100000);
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    Pimage(2).coverage = S2_vri_dataset.V1V2.coverage_mask;
    Pimage(2).Pimages = zeros(1750,128,128,'single');
    for i = 1:1750
        Pimage(2).Pimages(i,:,:) = S2_vri_dataset.V1V2.Trn(i).average.z_img;
    end
end
if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    Pimage(1).coverage = S1_vri_dataset.V1V2.coverage_mask;
    Pimage(1).Pimages = zeros(1750,128,128,'single');
    for i = 1:1750
        Pimage(1).Pimages(i,:,:) = S1_vri_dataset.V1V2.Trn(i).average.z_img;
    end
end
if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    Pimage(3).coverage = S3_vri_dataset.V1V2.coverage_mask;
    Pimage(3).Pimages = zeros(1750,128,128,'single');
    for i = 1:1750
        Pimage(3).Pimages(i,:,:) = S3_vri_dataset.V1V2.Trn(i).average.z_img;
    end
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    Pimage(2).coverage = S2_vri_dataset.V1V2.coverage_mask;
    Pimage(2).Pimages = zeros(1750,128,128,'single');
    for i = 1:1750
        Pimage(2).Pimages(i,:,:) = S2_vri_dataset.V1V2.Trn(i).predicted.z_img;
    end
end
if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    Pimage(1).coverage = S1_vri_dataset.V1V2.coverage_mask;
    Pimage(1).Pimages = zeros(1750,128,128,'single');
    for i = 1:1750
        Pimage(1).Pimages(i,:,:) = S1_vri_dataset.V1V2.Trn(i).predicted.z_img;
    end
end
if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    Pimage(3).coverage = S3_vri_dataset.V1V2.coverage_mask;
    Pimage(3).Pimages = zeros(1750,128,128,'single');
    for i = 1:1750
        Pimage(3).Pimages(i,:,:) = S3_vri_dataset.V1V2.Trn(i).predicted.z_img;
    end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%% 13, 14 December 2014 %%%%%%%%%%%%%%%%%%%%%%%%
if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %load_subject_data_Kay_2008(1,NOV_2013_COMBINED_TRIALS);

    S=G.e(KAY_2008).v(NOV_2013_COMBINED_TRIALS).s(1);
    good = find(S.voxels_with_data_for_all_stimuli>0);
    v3a = find(S.roi==V3a);
    v3b = find(S.roi==V3b);
    v3 = find(S.roi==V3);
    v4 = find(S.roi==V4);
    v1 = find(S.roi==V1);
    lo = find(S.roi==LO);
    other = find(S.roi==OTHER);
    high_snr = find(S.snr>4.5);
    high_snr = intersect(good, high_snr);
    v3a_high_snr = intersect(v3a,high_snr);
    v3b_high_snr = intersect(v3b,high_snr);
    v3_high_snr = intersect(v3,high_snr);
    v4_high_snr = intersect(v4,high_snr);
    v1_high_snr = intersect(v1,high_snr);
    lo_high_snr = intersect(lo,high_snr);
    other_high_snr = intersect(other,high_snr);
    
    rf_pimage = zeros(128,128,'single');
    rf = zeros(128^2,1,'single');
    voxel_set = lo_high_snr;
    voxel_set_name = 'lo_high_snr';
    
    if not(exist('Pv1v2S1S2'))
        Pv1v2S1S2 = ( PimageV1V2(2).Pimages + PimageV1V2(3).Pimages )/2;
    end
%     if not(exist('Pv1v2S1S2'))
%         Pv1v2S1S2 = ( PimageV1V2_predicted(2).Pimages + PimageV1V2_predicted(3).Pimages )/2;
%     end
    for i = 1:length(voxel_set)
        vx = voxel_set(i);%50272;%49869;
        v=G.e(KAY_2008).v(NOV_2013_COMBINED_TRIALS).s(1).stim(TRN).data(vx,:);
        rf_pimage = 0*rf_pimage;
        for x = 1:128
            for y = 1:128
                p = Pv1v2S1S2(:,x,y);
                cc = corrcoef( v, p );
                rf_pimage(x,y) = cc(1,2);
            end
        end
        
        rf = 0*rf;
        voxel_responses = S.stim(TRN).data(vx,1:1750);
        %pixel_values = sqrt(pixel_values);
        for i = 1:(128^2)

            cc = corrcoef( voxel_responses, pixel_values(:,i) );
            rf(i) = cc(1,2);
        end
        rf = reshape(rf,128,128)';

        %mi(rf,vx,[1,2,1],d2c({voxel_set_name vx S.snr(vx)}))
        mi(rf_pimage,vx,[1,2,2],d2c({voxel_set_name vx S.snr(vx)}))
        drawnow;
    end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if 0
    if not(exist('stimTrn512_int8'))
         load('/Users/internetaccess/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/stimuli-stimTrn/version-512px/stimTrn512_int8.mat');
    end
    if not(exist('Pv1v2'))
        Pv1v2 = ( PimageV1V2(1).Pimages + PimageV1V2(2).Pimages + PimageV1V2(3).Pimages )/3;
    end
%     if not(exist('Pv1v2'))
%         Pv1v2 = ( PimageV1V2_predicted(1).Pimages + PimageV1V2_predicted(2).Pimages + PimageV1V2_predicted(3).Pimages )/3;
%     end
    dxy = 2;
    for x = 40:10:80
        for y = 40:10:80
            e = Pv1v2(:,(x-dxy):(x+dxy),(y-dxy):(y+dxy));
            e = sum(sum(e,2),3) / (dxy+1)^2;
            [p,I] = sort(e);
            for i = 1:25
                %mi(stimTrn512_int8(I(i),(x*4-40):(x*4+40),(y*4-40):(y*4+40)),1,[5,5,i]);
                mi(stimTrn512_int8(I(1751-i),:,:),1,[5,5,i]);
                hold on; plot(y*4,x*4,'o'); hold off;
            end
            [x,y]
            my_pause
        end
    end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if 1
    if not(exist('stimTrn512_int8'))
    	load('/Users/internetaccess/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/stimuli-stimTrn/version-512px/stimTrn512_int8.mat');
    end
    Pv1v2S1 = PimageV1V2(1).Pimages;
    Pv1v2S2S3 = ( PimageV1V2(2).Pimages + PimageV1V2(3).Pimages )/2;
    Pv1v2S2S3_predicted = ( PimageV1V2_predicted(2).Pimages + PimageV1V2_predicted(3).Pimages )/2;
    S1_S2S3 = zeros(1750,1,'single');
    S1_S2S3_predicted = zeros(1750,1,'single');
    stimLst = [500,1270,695,640,253,473,428,612,792,1716];
    for j = 1:length(stimLst)
        i=stimLst(j);
        mi(squeeze(Pv1v2S1(i,:,:)).*PimageV1V2(1).coverage,1,[1,4,1]);
        mi(Pv1v2S2S3(i,:,:),1,[1,4,2]);
        mi(Pv1v2S2S3_predicted(i,:,:),1,[1,4,3]);
        mi(stimTrn512_int8(i,:,:),1,[1,4,4],d2s({'Trn ' i}));
        my_pause;
    end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
