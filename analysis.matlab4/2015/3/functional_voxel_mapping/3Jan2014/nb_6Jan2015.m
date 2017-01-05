clc; fprintf('%s\n',[mfilename ' (' mfilename('fullpath') '.m)']);

if not(exist('G'))
    error('NOTE: run local_startup.m and G_initalize manually at the beginning of the Matlab session.');
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    E = G.constants.KAY_2008;
    V = G.constants.NOV_2013_SINGLE_TRIAL;
    VAL = G.constants.VAL;
    TRN = G.constants.TRN;
    subj = 1;
    load_subject_data_Kay_2008( subj, V );
    load_subject_data_Kay_2008( subj, G.constants.NOV_2013_COMBINED_TRIALS);
    %S = G.e(E).v(V).s(subj);
    S = G.e(E).v(G.constants.NOV_2013_COMBINED_TRIALS).s(subj);
end

if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    good = find(S.voxels_with_data_for_all_stimuli>0);
    v3a = find(S.roi==V3a);
    v3b = find(S.roi==V3b);
    v3 = find(S.roi==V3);
    v4 = find(S.roi==V4);
    v1 = find(S.roi==V1);
    v2 = find(S.roi==V2);
    lo = find(S.roi==LO);
    other = find(S.roi==OTHER);
    high_snr = find(S.snr>1.5);
    high_snr = intersect(good, high_snr);
    v3a_high_snr = intersect(v3a,high_snr);
    v3b_high_snr = intersect(v3b,high_snr);
    v3_high_snr = intersect(v3,high_snr);
    v4_high_snr = intersect(v4,high_snr);
    v1_high_snr = intersect(v1,high_snr);
    v2_high_snr = intersect(v2,high_snr);
    lo_high_snr = intersect(lo,high_snr);
    other_high_snr = intersect(other,high_snr);
    
    voxel_set = high_snr;%union(v1_high_snr,v2_high_snr);
    voxel_set_name = 'high_snr';
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    voxel_correlations = zeros(length(voxel_set),length(voxel_set),'single');
    for i = 1:length(voxel_set)
        i
        for j = 1:i
            vi = voxel_set(i);
            vj = voxel_set(j);
            cc = corrcoef( S.stim(TRN).data(vi,1:1750), S.stim(TRN).data(vj,1751:3500) );
            c = cc(1,2);
            voxel_correlations(i,j) = c; voxel_correlations(j,i) = c;
        end
    end
    %mi(voxel_correlations,1,[1,1,1],'voxel_correlations');
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    sorted_voxel_correlation_indicies = 0*voxel_correlations;
    sorted_voxel_correlation_values = 0*voxel_correlations;
    for i = 1:length(voxel_set)
        [Y,I] = sort(-voxel_correlations(i,:));
        sorted_voxel_correlation_indicies(i,:) = I;
        sorted_voxel_correlation_values(i,:) = -Y;
    end
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    NN=16;
    % note, in cross-trial correlations, autocorrelation is not necessarily
    % the highest correlation.
    top_correlations_indicies = sorted_voxel_correlation_indicies(:,2:NN);
    top_correlations_values = sorted_voxel_correlation_values(:,2:NN);
    distances = 0 * top_correlations_values;
    for i = 1:length(voxel_set)
        a = S.voxel_scanner_XYZs(voxel_set(i),:);
        for j = 1:(NN-1)
            b = S.voxel_scanner_XYZs(voxel_set(top_correlations_indicies(i,j)),:);
            d = distance_vec(single(a),single(b));
            distances(i,j) = distances(i,j) + d;
        end
    end
    for i = 1:length(voxel_set)
        top_correlations_values(i,:) = top_correlations_values(i,:) - sorted_voxel_correlation_values(i,NN+1);
    end
    for i = 1:length(voxel_set)
        for j = 1:(NN-1)
            top_correlations_values(i,j) = top_correlations_values(i,j) / ((distances(i,j)+1)^2);
        end
    end
end

if 1  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   data_good = S.stim(TRN).data(voxel_set,:);
   z_data_good = 0 * data_good;
   for i = 1:1750%3500
       d = data_good(:,i);
       zd = d - mean(d);
       zd = zd / std(zd);
       z_data_good(:,i) = zd;
   end
   z_data = 0 * S.stim(TRN).data;
   z_data(voxel_set,:) = z_data_good;
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    photo_correlations = zeros(1750,1750,'single');
    for i = 1:1750
        i
        for j = 1:i
            cc = corrcoef( (z_data(voxel_set,i)+z_data(voxel_set,i+1750))/2, (z_data(voxel_set,j)+z_data(voxel_set,j+1750))/2 );
            c = cc(1,2);
            photo_correlations(i,j) = c; photo_correlations(j,i) = c;
        end
    end
    mi(photo_correlations,1,[1,1,1],d2s({'photo_correlations: ' voxel_set_name}));
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    photo_correlations = zeros(1750,1750,'single');
    for i = 1:1750
        i
        for j = 1:i
            cc1 = corrcoef( (z_data_S1(voxel_set_S1,i)+z_data_S1(voxel_set_S1,i+1750))/2, (z_data_S1(voxel_set_S1,j)+z_data_S1(voxel_set_S1,j+1750))/2 );
            c1 = cc1(1,2);
            
            cc2 = corrcoef( (z_data_S2(voxel_set_S2,i)+z_data_S2(voxel_set_S2,i+1750))/2, (z_data_S2(voxel_set_S2,j)+z_data_S2(voxel_set_S2,j+1750))/2 );
            c2 = cc2(1,2);
            
            cc3 = corrcoef( (z_data_S3(voxel_set_S3,i)+z_data_S3(voxel_set_S3,i+1750))/2, (z_data_S3(voxel_set_S3,j)+z_data_S3(voxel_set_S3,j+1750))/2 );
            c3 = cc3(1,2);
            
            c = (c1+c2+c3)/3;
            photo_correlations(i,j) = c; photo_correlations(j,i) = c;
        end
    end
    mi(photo_correlations,1,[1,1,1],d2s({'photo_correlations: ' voxel_set_name}));
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    pc = photo_correlations;
    for i = 1:1750
        i
        for j = 1:i
            if abs(i-j)<70
                pc(i,j)=0;pc(j,i)=0;
            end
        end
    end
    mi(pc,1,[1,1,1],d2s({'pc: ' voxel_set_name}));
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    sorted_photo_correlation_indicies = 0*pc;
    sorted_photo_correlation_values = 0*pc;
    for i = 1:1750
        [Y,I] = sort(-pc(i,:));
        sorted_photo_correlation_indicies(i,:) = I;
        sorted_photo_correlation_values(i,:) = -Y;
    end
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    NN=16;
    % note, in cross-trial correlations, autocorrelation is not necessarily
    % the highest correlation.
    top_correlations_indicies = sorted_photo_correlation_indicies(:,1:NN);
    top_correlations_values = sorted_photo_correlation_values(:,1:NN);
    distances = 0 * top_correlations_values;
    for i = 1:1750
        top_correlations_values(i,:) = top_correlations_values(i,:) - sorted_photo_correlation_values(i,NN+1);
    end
end

if 0
    G.stimTrn128 = zeros(1750,128,128,'single');
    G.stimTrn64 = zeros(1750,64,64,'single');
    h = waitbar(0, 'Now processing...');
    for i = 1:1750
        waitbar(i/1750);
        p512 = sqsing(G.stimTrn512_int8(i,:,:));
        p128 = reduceMatrixByHalf(reduceMatrixByHalf(p512));
        p64 = reduceMatrixByHalf(p128);
        G.stimTrn128(i,:,:) = p128;
        G.stimTrn64(i,:,:) = p64;
    end
    close(h);
    my_save(G.stimTrn64,'stimTrn64');
    my_save(G.stimTrn128,'stimTrn128');
end

if 0
    load('~/Desktop/Matlab_Desktop/6Jan2014_photo_run1.S1,2,3.final.735971.2506.vox_xys.mat')
    vox_xys(:,1) = vox_xys(:,1) - min(vox_xys(:,1));
    vox_xys(:,2) = vox_xys(:,2) - min(vox_xys(:,2));
    max_vox_x = max(vox_xys(:,1));
    max_vox_y = max(vox_xys(:,2));
    n = 64;
    %photo_montage = zeros(n*max_vox_x,n*max_vox_y,'single');
    %hold off;
    %figure(1);
    h = waitbar(0, 'Now processing...');
    for i = 1:length(vox_xys)
        waitbar(i/length(vox_xys));
        x = vox_xys(i,1);
        y = vox_xys(i,2);
        %plot(x,y,'o');
        photo_montage( (64*x+1):(64*(x+1)),(64*y+1):(64*(y+1)) ) = squeeze(G.stimTrn64(i,:,:));
    end
    close(h);
    mi(photo_montage,1);
return;
    my_save(photo_montage,'photo_montage');
end
if 0
    load('~/Desktop/Matlab_Desktop/6Jan2014_photo_run1.S1,2,3.final.735971.2506.vox_xys.mat')
    vox_xys(:,1) = vox_xys(:,1) - min(vox_xys(:,1));
    vox_xys(:,2) = vox_xys(:,2) - min(vox_xys(:,2));
    max_vox_x = max(vox_xys(:,1));
    max_vox_y = max(vox_xys(:,2));
    n = 64;
    %photo_montage = zeros(n*max_vox_x,n*max_vox_y,'single');
    %hold off;
    %figure(1);
    h = waitbar(0, 'Now processing...');
    for i = 1:length(vox_xys)
        waitbar(i/length(vox_xys));
        x = vox_xys(i,1);
        y = vox_xys(i,2);
        %plot(x,y,'o');
        photo_montage( (64*x+1):(64*(x+1)),(64*y+1):(64*(y+1)) ) = squeeze(G.stimTrn64(i,:,:));
    end
    close(h);
    mi(photo_montage,1);
return;
    my_save(photo_montage,'photo_montage');
end

if 1
    %load('~/Desktop/Matlab_Desktop/FVM_runs/4Jan2014_run3/4Jan2014_run3.735968.9694.vox_xys.mat');    vox_xys(:,1) = vox_xys(:,1) - min(vox_xys(:,1));
    %load('~/Desktop/Matlab_Desktop/stimTrn64.735971.8596.mat'); G.stimTrn64 = stimTrn64;
    load('~/Desktop/Matlab_Desktop/FVM_runs/2Jan2014_first_run.735968.6241.vox_xys.mat')
    vox_xys(:,1) = vox_xys(:,1) - min(vox_xys(:,1));
    vox_xys(:,2) = vox_xys(:,2) - min(vox_xys(:,2));
    max_vox_x = max(vox_xys(:,1));
    max_vox_y = max(vox_xys(:,2));
    n = 64;
    %return
    photo_montage = zeros(n*max_vox_x,n*max_vox_y,'single');
    %hold off;
    %figure(1);
    h = waitbar(0, 'Now processing...');
    for i = 1:length(vox_xys)
        waitbar(i/length(vox_xys));
        x = vox_xys(i,1);
        y = vox_xys(i,2);
        %plot(x,y,'o');
        [Y,I] = sort(-z_data_good(i,1:1750));
        img_num = I(1);
        photo_montage( (64*x+1):(64*(x+1)),(64*y+1):(64*(y+1)) ) = squeeze(G.stimTrn64(img_num,:,:));
    end
    close(h);
    mi(photo_montage,1);
%return;
    my_save(photo_montage,'photo_montage');
    my_imwrite(photo_montage,'photo_montage');
end
