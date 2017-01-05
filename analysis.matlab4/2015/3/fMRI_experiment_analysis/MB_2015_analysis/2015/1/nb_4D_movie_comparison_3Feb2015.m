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

if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CELL_NUM = 0;
    if not(exist('nii1','var'))
        nii1 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/2/3Feb2015_Zipser_Pilots_HVO/fsl/3Feb2015_Partial_brain_motion_corrected_to_run_006a/20150203_082706mbboldmb615mmPartialPSNs004a001.feat/filtered_func_data.nii.gz');
        img1 = nii1.img;
    end
    if not(exist('nii2','var'))
         nii2 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/2/3Feb2015_Zipser_Pilots_HVO/fsl/3Feb2015_Partial_brain_motion_corrected_to_run_006a/20150203_082706mbboldmb615mmPartialPSNs006a001.feat/filtered_func_data.nii.gz');
        img2 = nii2.img;
    end
    if not(exist('nii3','var'))
         nii3 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/2/3Feb2015_Zipser_Pilots_HVO/fsl/3Feb2015_Partial_brain_motion_corrected_to_run_006a/20150203_082706mbboldmb615mmPartialPSNs008a001.feat/filtered_func_data.nii.gz');
        img3 = nii3.img;
    end
%     if not(exist('nii4','var'))
%         nii4 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/30Jan2015_Zipser_Pilots_HVO/fsl/30Jan2015_motion_corrected_to_first_run/20150130_081412mbboldmb615mmPartialPSNs012a001.feat/filtered_func_data.nii.gz');
%         img4 = nii4.img;
%     end
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
    for i = 1:3
        eval_str = d2s({'[z_img' i ', mean_img' i ', std_img' i '] = z_score_4D_nii(nii' i ');'});
        eval(eval_str);
    end
end
if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 30;
    for i = 1:3
        eval_str = d2s({'runs(' i ').z_img = z_img' i ';'});
        eval(eval_str);
    end
end


if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 50;
    num_TRs = 448;%150;
    MN = -6*4;
    MX = 6*4;
    X=138/2;Y=138/2;Z=36/2;
    hor_sum = 0*rot90(squeeze(runs(i).z_img(:,:,Z,1)));
    hor_sum = reduceMatrixByHalf(hor_sum);
    if false%not(exist('BL_frames'))
        'load Barry Lyndon frames'
        BL_frames = zeros(7500,320,512,3,'uint8');
        for i = 1:7500
            BL_frames(i,:,:,:)=imread(d2s({'~/Desktop/Data/fmri_scanning_experiments/2015/1/17Jan2015_BarryLyndon_material_for_scanning/BarryLyndon_redspot_17Jan2015_1.avi_images/' i '.png'}));
        end
    end
    f=0;
    vox_avg = [];
%     img_last1 = zeros(4,138,138,'single');
%     img_last2 = zeros(4,138,138,'single');
    avg_hor_sum_last1 = zeros(138/2,138/2,'single');
    avg_hor_sum_last2 = zeros(138/2,138/2,'single');
    for tr = 1:num_TRs
        fprintf('%d\n',tr);
        avg_hor_sum = 0 * hor_sum;
        %cor = 0*hor_sum+1;
        for i = 1:length(runs)
            if tr > 2
        day = 1;
            hor_sum  = 0 * hor_sum;
                img = runs(i).z_img;
                hor = rot90(squeeze(sum(img(:,:,6:30,tr),3)));
                hor = reduceMatrixByHalf(hor);
                %cor = cor .* hor;
                hor(1,1)=MN;hor(1,2)=MX;
                hor_sum = hor_sum + hor;
%                 hor_sum = hor_sum -mean(mean(hor_sum));
%                 hstd = std(reshape(hor_sum,138*138,1));
%                 hor_sum = hor_sum ./ hstd;
%                 if i==1
%                     mc(tr);
%                     if mc(tr)>0.1
%                         mcf
%                         hor_sum = 0*hor_sum;
%                         %my_pause
%                     end
%                     
%                     
%                 end
            avg_hor_sum = avg_hor_sum + hor_sum;
           mi(hor_sum,1,[2,4,i],d2s({tr}));%minutes ':' seconds}));

%                 if or(tr < 3,f<1)
%                     fm = 0* BL_frames(1,:,:,:);
%                 else
%                     fm = BL_frames(f+3,:,:,:);
%                 end
        
            end
        temp = avg_hor_sum;
        temp(1,1)=0.5*MN;temp(1,2)=0.5*MX;
        mi(0.5*avg_hor_sum_last2 + avg_hor_sum_last1 + 0.5*temp,1,[2,4,5],d2s({tr*0.667}));
        avg_hor_sum_last2 = avg_hor_sum_last1;
        avg_hor_sum_last1 = avg_hor_sum;
        %vox_avg(tr) = sum(sum(temp(110:130,65:85)));
        %mp({mc},1,[2,4,8]);hold on;mp({tr,mc(tr),'ro'},1,[2,4,8]);hold off
%         f1 = 1+round(300/448*(tr-1)*25-1*(4*25))
%         f2 = round(300/448*(tr)*25-1*(4*25))
        tic
        
%pause(300/448);
%         for f = f1:f2
%             if f > 0
% %                 if length(BL_frames(i).fimg) == 0
% %                     BL_frames(i).fimg=imread(d2s({'~/Desktop/Data/fmri_scanning_experiments/2015/1/17Jan2015_BarryLyndon_material_for_scanning/BarryLyndon_16Jan2015_1.avi_images/' f '.png'}));
% %                 end
% %                fimg=imread(d2s({'~/Desktop/Data/fmri_scanning_experiments/2015/1/17Jan2015_BarryLyndon_material_for_scanning/BarryLyndon_16Jan2015_1.avi_images/' f '.png'}));
%                 mi(BL_frames(f,:,:,:),1,[2,3,5],d2s({f}));
%                 pause(0.01);
%             end
        end
        %mi(cor,1,[2,4,6]);
         my_pause(0.667);
        toc

    end
    f = real(fft(vox_avg));
    fsp(3,[2,1,1]);plot(vox_avg,'o-');
    fsp(3,[2,1,2]);plot(f,'o-');%axis([0,60,min(f),max(f)]);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if 1
CELL_NUM = 30;
X=138/2;Y=138/2;Z=36/2;XYZ=[X Y Z];
k = [1 2 3 2 1];
%k=[1];
ctr22 = 0;
     mi_nii(squeeze(runs(1).z_img(:,:,:,1)),XYZ(1),XYZ(2),XYZ(3),2);
%     mi_nii(r_img,XYZ(1),XYZ(2),XYZ(3),2);
%     mi_nii(mean_func.img,XYZ(1),XYZ(2),XYZ(3),3);
     [y,z] = ginput(1);
     XYZ = [XYZ(1) round(y) 37-round(z)]%[71 21 60]; [54    44    39];
    
    r1r2img=zeros(138,138,'single');
    mi_nii(squeeze(runs(1).z_img(:,:,:,1)),XYZ(1),XYZ(2),XYZ(3),2);

%    mi_nii(r_img,XYZ(1),XYZ(2),XYZ(3),2);
%    mi_nii(mean_func.img,XYZ(1),XYZ(2),XYZ(3),3);
    for X = 135:-1:5
        %X
        for Y = 10:120
    r1 = (1:448)*0;
    r2 = 0*r1;
    for i = 1
        for x = -1:0
            for y = -1:0
                for z = -1:0
        r1 = r1 + squeeze(runs(i).z_img(X+x,Y+y,XYZ(3)+z,:))';
        r2 = r2 + (squeeze(runs(i+1).z_img(X+x,Y+y,XYZ(3)+z,:))'+squeeze(runs(i+2).z_img(X+x,Y+y,XYZ(3)+z,:))')/2;
                end
            end
        end
    end
    r1 = r1 / 4/28;
    r2 = r2 / 4/28;
    cc=corrcoef(r1,r2);
    r1r2img(X,Y)=cc(1,2);
    if cc(1,2)>0.20
        ctr22=ctr22+1;
        ctr22=9;
        r1c=conv(r1,k,'same');
        r2c=conv(r2,k,'same');
        mp({r1c,':'},ctr22,[2,1,1],d2s({cc(1,2)}));
        hold on;
        mp({r2c,'r:'},ctr22,[2,1,1]);
        mp({(r1c+r2c)/2,'ko-'},ctr22,[2,1,1]);
        hold off;
        mp({abs(real(fft(r1c))),':'},ctr22,[2,1,2]);
        hold on;
        mp({abs(real(fft(r2c))),'r:'},ctr22,[2,1,2]);
        mp({abs(real(fft((r2c+r1c)/2))),'ko-'},ctr22,[2,1,2]);
        hold off;
        XYZ
        my_pause;
    end
        end
        r1r2img(find(~isfinite( r1r2img)))=0;
        mi(rot90(r1r2img),2,[2,2,4]);
    end
    
    %mp({r1,r2,'o'},2,[2,2,4],d2s({cc(1,2)}));
end

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