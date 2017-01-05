function load_subject_data_Kay_2008( subject_number, experiment_version )
% function load_subject_data_Kay_2008( subject_number, experiment_version )
% 12 December 2014

global G;
E = G.constants.KAY_2008;
V = experiment_version;
VAL = G.constants.VAL;
TRN = G.constants.TRN;

    
%    G.e(E).v(V).raw_data_path = [G.home '/' G.Desktop '/fMRI_top_node/data.fMRI/experiment-Kay_2008/data_from_Kay_25Nov2013_not_v7.3' ];
    G.e(E).v(V).raw_data_path = [G.Desktop '/fMRI_top_node/data.fMRI/experiment-Kay_2008/data_from_Kay_25Nov2013'];%_not_v7.3' ];
    G.e(E).v(V).scannerMax.X = 86;
    G.e(E).v(V).scannerMax.Y = 86;
    G.e(E).v(V).scannerMax.Z = 34;
    scannerMax = G.e(E).v(V).scannerMax;


    subject = d2s({'S' subject_number});
    fprintf('%s',d2s({'load_subject_raw_data( ', subject, ' ) . . . '}));
    
    S = [];
    
    if subject_number == 1
        S.description = 'TN';
    elseif subject_number == 2
        S.description = 'KK';
    elseif subject_number == 3
        S.description = 'SN';
    else
        error( d2s({'load_data_Kay_2008: Unkonwn subject #: ' subject_number}) );
    end
    
    S.stim(VAL).description = d2s({'Subject ' subject_number ' val-set voxel responses, 120 photos'});
    S.stim(TRN).description = d2s({'Subject ' subject_number ' trn-set voxel responses, 1750 photos'});

    S.subject = subject;
    
	data_dir_path = [G.e(E).v(V).raw_data_path '/subject-', subject, '/'];
    load( [data_dir_path, subject, 'aux.mat'] );
    
    if V == G.constants.NOV_2013_SINGLE_TRIAL
        G.e(E).v(V).description = 'NOV_2013_SINGLE_TRIAL';
        load( [data_dir_path, subject, 'data_trn_singletrial.mat'] );
        load( [data_dir_path, subject, 'data_val_singletrial.mat'] );
        S.stim(TRN).data = eval( [ 'dataTrnSingle', subject ] );
        S.stim(VAL).data = eval( [ 'dataValSingle', subject ] );
    elseif V == G.constants.NOV_2013_COMBINED_TRIALS
        G.e(E).v(V).description = 'NOV_2013_COMBINED_TRIALS';
        load( [data_dir_path, subject, 'data.mat'] );
        S.stim(TRN).data = eval( [ 'dataTrn', subject ] );
        S.stim(VAL).data = eval( [ 'dataVal', subject ] );
    else
        error('Unknown experiment version');
    end
    
    S.roi = eval( [ 'roi', subject ] );
    S.snr = eval( [ 'snr', subject ] );
    S.voxIdx = eval( [ 'voxIdx', subject ] );
    


    S.num_voxels = length(S.stim(TRN).data);
    if S.num_voxels ~= length(S.stim(VAL).data)
        error('if S.num_voxels ~= length(S.stim(VAL).data)');
    end
    if S.num_voxels ~= length(S.roi)
        error('if S.num_voxels ~= length(S.roi)');
    end
    if S.num_voxels ~= length(S.snr)
        error('if S.num_voxels ~= length(S.snr)');
    end
    if S.num_voxels ~= length(S.voxIdx)
        error('if S.num_voxels ~= length(S.voxIdx)');
    end
    


    S.voxel_scanner_XYZs = zeros( S.num_voxels, 3, 'uint32' );
    S.scanner_XYZs_to_voxel_index = zeros( G.e(E).v(V).scannerMax.X, G.e(E).v(V).scannerMax.Y, G.e(E).v(V).scannerMax.Z, 'uint32' );

    volume_index = zeros( G.e(E).v(V).scannerMax.X * G.e(E).v(V).scannerMax.Y * G.e(E).v(V).scannerMax.Z, 3, 'uint32' );

    fprintf('volume_index...');
    indx = 0;
    for z=1:G.e(E).v(V).scannerMax.Z
        for x=1:G.e(E).v(V).scannerMax.X
            for y=1:G.e(E).v(V).scannerMax.Y
                indx = indx + 1;
                volume_index(indx,:) = [x,y,z];
            end
        end
    end

    fprintf('voxel_scanner_XYZs, scanner_XYZs_to_voxel_index...');
    for voxel = 1:S.num_voxels
        vi = volume_index( S.voxIdx(voxel), : );
        S.voxel_scanner_XYZs( voxel, : ) = vi;
        S.scanner_XYZs_to_voxel_index( vi(1), vi(2), vi(3) ) = voxel;
    end

    

    S.voxels_with_data_for_all_stimuli = zeros(S.num_voxels, 1, 'uint8');

    for voxel = 1:S.num_voxels
        S.voxels_with_data_for_all_stimuli(voxel) = and( min(isfinite(S.stim(TRN).data(voxel,:))), min(isfinite(S.stim(VAL).data(voxel,:))) );
    end
    
    S
    G.e(E).v(V).s(subject_number) = S;
    
    fprintf( 'Done.\n' )