if 0
	if not(exist('betas'))
		load('/Users/davidzipser/Desktop/preprocessFMAP/preprocessFMAP/GLMdenoisefiguresFMAP.mat');
	end

	zbetas = 0*betas;
	ctr = 0;
	for x = 1:106
		x
		for y = 1:106
			for z = 1:60
				b = squeeze(betas(x,y,z,:));
				if max(not(isfinite(b)))==0
					ctr=ctr+1;
					zbetas(x,y,z,:) = zscore(betas(x,y,z,:));
				end
			end
		end
	end
	ctr
end

if 1
	for i = 1:12
		mi_nii(squeeze(zbetas(:,:,:,i)),50,30,20,i,false);
	end
end
