clc; fprintf('%s\n',[mfilename ' (' mfilename('fullpath') '.m)']);


if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    global G;
    E = G.constants.KAY_2008;
    V = G.constants.NOV_2013_SINGLE_TRIAL;
    VAL = G.constants.VAL;
    TRN = G.constants.TRN;
    load_subject_data_Kay_2008( 1, V )
    load_subject_data_Kay_2008( 1, G.constants.NOV_2013_COMBINED_TRIALS);
    S = G.e(E).v(V).s(1);
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %load_subject_data_Kay_2008( 1, V )

    if not(exist('stimVal512_uint8'))
         load('/Users/internetaccess/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/stimuli-stimVal/version-512px/stimVal512_uint8.mat');
    end
    

    for i = 1:120

        display_brain_slices_general('Kay 2008',S.subject,d2s({'VAL ' i}),...
            S.stim(VAL).data(:,i),S.scanner_XYZs_to_voxel_index,...
            1,4,28,2);
        mi(stimVal512_uint8(i,:,:),2);
        pause%(4);

    end
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %load_subject_data_Kay_2008( 1, V )

    if not(exist('stimVal512_uint8'))
         load('/Users/internetaccess/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/stimuli-stimVal/version-512px/stimVal512_uint8.mat');
    end
    G.stimVal512_uint8 = stimVal512_uint8;
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

if 1
%     if not(exist('voxel_correlations'))
%         load('/Users/internetaccess/Desktop/Matlab_Desktop/v1_1p5_snr_correlations.735963.8688.mat');
%     end
    sorted_voxel_correlation_indicies = 0*voxel_correlations;
    sorted_voxel_correlation_values = 0*voxel_correlations;
    for i = 1:length(voxel_set)
        [Y,I] = sort(-voxel_correlations(i,:));
        sorted_voxel_correlation_indicies(i,:) = I;
        sorted_voxel_correlation_values(i,:) = -Y;
    end
end

if 1 
    NN=16;
    top_correlations_indicies = sorted_voxel_correlation_indicies(:,2:NN);
    top_correlations_values = sorted_voxel_correlation_values(:,2:NN);
    for i = 1:length(voxel_set)
        top_correlations_values(i,:) = top_correlations_values(i,:) - sorted_voxel_correlation_values(i,NN+1);
    end
end

