function resampled_data = tseriesinterp_selected_voxels(run_data, selected_voxel_xyzs, TR, Hz )
% function sampled_data = tseriesinterp_selected_voxels(run_data, selected_voxel_xyzs, TR, Hz )
%
    %resampled_data = zeros(length(selected_voxel_xyzs),1500);
    h=waitbar(0,'procesing...');movegui(h,'southeast');
    for j = 1:length(selected_voxel_xyzs)
        waitbar(j/length(selected_voxel_xyzs));
        a = selected_voxel_xyzs(j,:);
        rd = squeeze(run_data(a(1),a(2),a(3),:));
        rd_interp = tseriesinterp(rd,TR,1/Hz);
        if j == 1
            resampled_data = zeros(length(selected_voxel_xyzs),length(rd_interp));
        end
        resampled_data(j,:) = tseriesinterp(rd,TR,1/Hz);
    end
    close(h);
end