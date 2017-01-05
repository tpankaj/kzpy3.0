if 0
	if not(exist('dataTrnS1'))
		load('/Users/davidzipser/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/data_from_Kay_25Nov2013/subject-S1/S1data.mat')
	end
	if not(exist('all_voxels_responses'))
		load('/Users/davidzipser/Data/analysis/2013/DATA_REPRESENTATIONS/date_labeled_data_DZ_NEW_IMAC/20Nov2013/20Nov2013 cudanet analysis/all_voxels_responses.cuda18Nov.mat')
		load('/Users/davidzipser/Data/analysis/2013/DATA_REPRESENTATIONS/date_labeled_data_DZ_NEW_IMAC/20Nov2013/20Nov2013 cudanet analysis/all_voxels_roi_int_codes.cuda18.mat')
	end

	data = dataTrnS1';
	data(find(not(isfinite(data)))) = 0;

	layer_7 = all_voxels_responses(find(all_voxels_roi_int_codes==-6),:);
end

if 1
	Bs = [];
	for i = 1:size(layer_7,1)
		i
		[B,FitInfo] = lasso(data,layer_7(i,:));
		Bs(i).B = B;
		Bs(i).FitInfo = FitInfo;
	end
end