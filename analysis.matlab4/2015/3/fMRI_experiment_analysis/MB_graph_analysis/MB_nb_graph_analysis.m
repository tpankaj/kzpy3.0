if 0
	c = 0 * ori_MB_experiment.runs(1).z_scored_filtered_func_data.std_img;
	c_vals = 0 * 1:27;
	for z = 1+randperm(size(c,3)-2)
		for e = 1:3
			if e == 1
				MB_experiment = ori_MB_experiment;
			elseif e == 2
				MB_experiment = ecc_MB_experiment;
			elseif e == 3
				MB_experiment = ver_MB_experiment;
			else
				error('unknown experiment');
			end
			for r = 1:length(MB_experiment.runs)

				a = MB_experiment.runs(r).z_scored_filtered_func_data.std_img;
				b = MB_experiment.runs(r).z_scored_filtered_func_data.z_img;

				tic
				h=waitbar(0,'processing...');movegui(h,'southeast');
				for x = 2:(size(b,1)-1)
					waitbar(x/size(b,1));
					for y = 2:(size(b,2)-1)
						%for z = 25%13:30%2:(size(b,3)-1)
							if a(x,y,z) > 0
								ctr = 0;
								c_vals = 0 * c_vals;
								for xx = (x-1):(x+1)
									for yy = (y-1):(y+1)
										for zz = (z-1):(z+1)
											cc = corrcoef(b(xx,yy,zz,:),b(x,y,z,:));
											ctr = ctr + 1;
											c_vals(ctr) = cc(1,2);
										end
									end
								end
								c_vals = -1*sort(-c_vals);
								m = mean(c_vals(2:4));
								if isfinite(m)
									c(x,y,z) = c(x,y,z) + m; %c_vals(2);%mean(c_vals(2:7));
								end
							end
						%end
					end
				end
				close(h);
				toc

				%mi_nii(c(:,:,:,1),xx,yy,zz,v,false);title(d2c({xx yy zz r}));
				q = c;%
				%q=cs(3).c;
				t = -1;%0.6;%
				qt=q;
				i=find(and(q>=t,q<1));
				figure(98);hist(q(i),100);
				title(length(i));j=find(q<t);
				qt(j)=0;
				mi(makeimagestack(qt),99)
				p = squeeze(c(:,:,z));
				m = median(median(p(find(p>0))));
				t=1.0*m;q = c;qt=q;i=find(and(q>=t,q<1));figure(98);hist(q(i),100);title(length(i));j=find(q<t);qt(j)=0;mi(makeimagestack(qt),100)

			end

		end
	end
	%c = c / length(MB_experiment.runs);
end

if 0

					q = local_correlations;%
				% %q=cs(3).c;
				% t = -1;%0.6;%
				% qt=q;
				% i=find(and(q>=t,q<1));
				% figure(98);hist(q(i),100);
				% title(length(i));j=find(q<t);
				% qt(j)=0;
				% mi(makeimagestack(qt),99)
				% p = squeeze(c(:,:,z));
				m = median(median(median(q(find(q>0)))));
				t=1.1*m;qt=q;
				i=find(and(q>=t,q<1));
				% figure(98);
				% hist(q(i),100);
				title(length(i));j=find(q<t);
				qt(j)=0;
				QTT=qt;
				mi(makeimagestack(qt),100);
end

if 0
	zc_sum = 0 * ori_MB_experiment.runs(1).z_scored_filtered_func_data.std_img;
	for e = 1:3
		if e == 1
			MB_experiment = ori_MB_experiment;
		elseif e == 2
			MB_experiment = ecc_MB_experiment;
		elseif e == 3
			MB_experiment = ver_MB_experiment;
		else
			error('unknown experiment');
		end
		for r = 1:length(MB_experiment.runs)

			zc_sum = zc_sum + MB_experiment.zc_sum;
		end
	end
end

if 1
	cs = [];
	ctr = 0;
	for v = 1:100000000
		xyzs = RF_mapping.selected_voxel_xyzs(randi(length(RF_mapping.selected_voxel_xyzs)),:);
		xx = xyzs(1); yy = xyzs(2); zz = xyzs(3);
		xx = randi(106);yy=randi(106);zz=randi(60);
		if QTT(xx,yy,zz) > 0
			ctr = ctr + 1;
			c = QTT * 0;
			for e = 1:3
				if e == 1
					MB_experiment = ori_MB_experiment;
				elseif e == 2
					MB_experiment = ecc_MB_experiment;
				elseif e == 3
					MB_experiment = ver_MB_experiment;
				else
					error('unknown experiment');
				end
				for r = 1:length(MB_experiment.runs)

					a = MB_experiment.runs(r).z_scored_filtered_func_data.std_img;
					b = MB_experiment.runs(r).z_scored_filtered_func_data.z_img;

					
					%xx = 35; yy = 80; zz = 30;
					%mi_nii(b(:,:,:,1),xx,yy,zz,1,false);

					
					bb = b(xx,yy,zz,:);

					brain_voxels = 0;

					tic
					h=waitbar(0,'processing...');movegui(h,'southeast');
					for x = 1:size(b,1)
						waitbar(x/size(b,1));
						for y = 1:size(b,2)
							for z = 1:size(b,3)
								if QTT(x,y,z) > 0
									brain_voxels = brain_voxels + 1;
									cc = corrcoef(bb,b(x,y,z,:));
									c(x,y,z) = c(x,y,z) + cc(1,2);
								end
							end
						end
					end
					brain_voxels
					close(h);
					toc
					c(xx,yy,zz)=0;
					c(xx,yy,zz) = 1.25*max(max(max(c)));
					%mi_nii(c(:,:,:,1),xx,yy,zz,v,false);title(d2c({xx yy zz r}));
					q = c;%
					%q=cs(3).c;
					t = -1;%0.6;%
					qt=q;
					i=find(and(q>=t,q<1));
					figure(98);hist(q(i),100);
					title(length(i));j=find(q<t);
					qt(j)=0;
					mi(makeimagestack(qt),99)
				end
			end
			c = c / length(MB_experiment.runs);
			c(xx,yy,zz) = 1;
			cs(ctr).c = c;
			ctr
		end
	end
end
