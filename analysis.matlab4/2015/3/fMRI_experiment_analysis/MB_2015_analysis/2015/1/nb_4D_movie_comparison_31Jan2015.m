%%%%%%%%%%% Standard Notebook Beginning %%%%%%%%%%%%
%
clc; fprintf('%s\n',[mfilename ' (' mfilename('fullpath') '.m)']);
this_filename = mfilename('fullpath');
this_file_text = fileread([this_filename,'.m']);
if not(exist('G'))
    error('NOTE: run local_startup.m manually at the beginning of the Matlab session.');
end
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
GRAPHICS = 1;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Description . . .
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CELL_NUM = 0;
    if not(exist('nii1','var'))
        nii1 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/30Jan2015_Zipser_Pilots_HVO/fsl/30Jan2015_motion_corrected_to_first_run/20150130_081412mbboldmb615mmPartialPSNs006a001.feat/filtered_func_data.nii.gz');
        img1 = nii1.img;
    end
    if not(exist('nii2','var'))
         nii2 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/30Jan2015_Zipser_Pilots_HVO/fsl/30Jan2015_motion_corrected_to_first_run/20150130_081412mbboldmb615mmPartialPSNs008a001.feat/filtered_func_data.nii.gz');
        img2 = nii2.img;
    end
    if not(exist('nii3','var'))
         nii3 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/30Jan2015_Zipser_Pilots_HVO/fsl/30Jan2015_motion_corrected_to_first_run/20150130_081412mbboldmb615mmPartialPSNs010a001.feat/filtered_func_data.nii.gz');
        img3 = nii3.img;
    end
    if not(exist('nii4','var'))
        nii4 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/30Jan2015_Zipser_Pilots_HVO/fsl/30Jan2015_motion_corrected_to_first_run/20150130_081412mbboldmb615mmPartialPSNs012a001.feat/filtered_func_data.nii.gz');
        img4 = nii4.img;
    end
%     if not(exist('nii5','var'))
%          nii5 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/22Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/24Jan2015/20150122_144129mbboldmb615mmAPPSNs005a001.feat/filtered_func_data.nii.gz');
%         img5 = nii5.img;
%     end
%     if not(exist('nii6','var'))
%          nii6 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/22Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/24Jan2015/20150122_144129mbboldmb615mmAPPSNs007a001.feat/filtered_func_data.nii.gz');
%         img6 = nii6.img;
%     end
end


if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 20;
    for i = 3:4
        eval_str = d2s({'[z_img' i ', mean_img' i ', std_img' i '] = z_score_4D_nii(nii' i ');'});
        eval(eval_str);
    end
end
if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 30;
    for i = 3:4
        eval_str = d2s({'runs(' i ').z_img = z_img' i ';'});
        eval(eval_str);
    end
end


if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 50;
mc=(1:448)*0;
    num_TRs = 448;%150;
    MN = -6*4;
    MX = 6*4;
    X=138/2;Y=138/2;Z=36/2;
    hor_sum = 0*rot90(squeeze(runs(1).z_img(:,:,Z,1)));

    if not(exist('BL_frames'))
        'load Barry Lyndon frames'
        BL_frames = zeros(7500,320,512,3,'uint8');
        for i = 1:7500
            BL_frames(i,:,:,:)=imread(d2s({'~/Desktop/Data/fmri_scanning_experiments/2015/1/17Jan2015_BarryLyndon_material_for_scanning/BarryLyndon_redspot_17Jan2015_1.avi_images/' i '.png'}));
        end
    end
    f=0;
%     img_last1 = zeros(4,138,138,'single');
%     img_last2 = zeros(4,138,138,'single');
    for tr = 1:num_TRs
        fprintf('%d\n',tr);
        avg_hor_sum = 0 * hor_sum;
        for i = 1:4%:length(runs)
            if tr > 2
%                 img_last2(i,:,:) = img_last1(i,:,:);
%                 img_last1(i,:,:) = hor_sum(i,:,:);
            end

        %for day = 1:3
        day = 1;
            hor_sum  = 0 * hor_sum;
            %for j = 1:3
                %i = 1%(day-1)*3+j;
                img = runs(i).z_img;
                hor = rot90(squeeze(sum(img(:,:,6:30,tr),3)));
                hor(1,1)=MN;hor(1,2)=MX;
                hor_sum = hor_sum + hor;
                hor_sum = hor_sum -mean(mean(hor_sum));
                hstd = std(reshape(hor_sum,138*138,1));
                hor_sum = hor_sum ./ hstd;
                if i==1
                    mc(tr);
                    if mc(tr)>0.1
                        mcf
                        hor_sum = 0*hor_sum;
                        %my_pause
                    end
                    
                    
                end
                %mi(hor,1,[1,7,i],d2s({tr}));
            %end
            avg_hor_sum = avg_hor_sum + hor_sum;
            %mi(0.5*hor_sum+squeeze(img_last1(i))+0.5*squeeze(img_last2(i)),1,[2,3,i],d2s({tr}));%minutes ':' seconds}));
            mi(hor_sum,1,[2,4,i],d2s({tr}));%minutes ':' seconds}));

                %my_imwrite(hor_sum,d2s({tr '.hor'}),'TRs');
                if or(tr < 3,f<1)
                    fm = 0* BL_frames(1,:,:,:);
                else
                    fm = BL_frames(f+3,:,:,:);
                end
                %my_imwrite(fm,d2s({tr '.frame'}),'TRs');
        
        end
        avg_hor_sum(1,1)=1*MN;avg_hor_sum(1,2)=1*MX;
        mi(avg_hor_sum,1,[2,4,5],d2s({tr}));
        mp({mc},1,[2,4,8]);hold on;mp({tr,mc(tr),'ro'},1,[2,4,8]);hold off
        f1 = 1+round(300/448*(tr-1)*25-1*(4*25))
        f2 = round(300/448*(tr)*25-1*(4*25))
        tic
        %my_pause
%pause(300/448);
        for f = f1:f2
            if f > 0
%                 if length(BL_frames(i).fimg) == 0
%                     BL_frames(i).fimg=imread(d2s({'~/Desktop/Data/fmri_scanning_experiments/2015/1/17Jan2015_BarryLyndon_material_for_scanning/BarryLyndon_16Jan2015_1.avi_images/' f '.png'}));
%                 end
%                fimg=imread(d2s({'~/Desktop/Data/fmri_scanning_experiments/2015/1/17Jan2015_BarryLyndon_material_for_scanning/BarryLyndon_16Jan2015_1.avi_images/' f '.png'}));
                mi(BL_frames(f,:,:,:),1,[2,3,5],d2s({f}));
                pause(0.01);
            end
        end
        toc

    end
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 60;

    tr_img = zeros(108,138,138,6,'single');
    
    %for tr = 1:num_TRs
    tr = 25;

        for i = 1:6
            for z = 1:108
                tr_img(z,:,:,i) = runs(i).z_img(:,:,z,32)';
            end
        end
        tr_img = sum(tr_img,4);
	my_save(tr_img,'tr_img');
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%