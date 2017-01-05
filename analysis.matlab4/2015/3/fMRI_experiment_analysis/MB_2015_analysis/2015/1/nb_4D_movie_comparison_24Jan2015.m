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

if 0 %%%%%%% high pass 20s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CELL_NUM = 0;
    if not(exist('nii1','var'))
        nii1 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/24Jan2015/20150118_164630mbboldmb615mmAPPSNs003a001.feat/filtered_func_data.nii.gz');
        img1 = nii1.img;
    end
    if not(exist('nii2','var'))
         nii2 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/24Jan2015/20150118_164630mbboldmb615mmAPPSNs005a001.feat/filtered_func_data.nii.gz');
        img2 = nii2.img;
    end
    if not(exist('nii3','var'))
         nii3 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/24Jan2015/20150118_164630mbboldmb615mmAPPSNs007a001.feat/filtered_func_data.nii.gz');
        img3 = nii3.img;
    end
    if not(exist('nii4','var'))
        nii4 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/22Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/24Jan2015/20150122_144129mbboldmb615mmAPPSNs003a001.feat/filtered_func_data.nii.gz');
        img4 = nii4.img;
    end
    if not(exist('nii5','var'))
         nii5 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/22Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/24Jan2015/20150122_144129mbboldmb615mmAPPSNs005a001.feat/filtered_func_data.nii.gz');
        img5 = nii5.img;
    end
    if not(exist('nii6','var'))
         nii6 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/22Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/24Jan2015/20150122_144129mbboldmb615mmAPPSNs007a001.feat/filtered_func_data.nii.gz');
        img6 = nii6.img;
    end
end

if 0 %%%%%%% high pass 50s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CELL_NUM = 0;
    if not(exist('nii1','var'))
        nii1 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/25Jan2015/20150118_164630mbboldmb615mmAPPSNs003a001.feat/filtered_func_data.nii.gz');
        img1 = nii1.img;
    end
    if not(exist('nii2','var'))
         nii2 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/25Jan2015/20150118_164630mbboldmb615mmAPPSNs005a001.feat/filtered_func_data.nii.gz');
        img2 = nii2.img;
    end
    if not(exist('nii3','var'))
         nii3 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/25Jan2015/20150118_164630mbboldmb615mmAPPSNs007a001.feat/filtered_func_data.nii.gz');
        img3 = nii3.img;
    end
    if not(exist('nii4','var'))
        nii4 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/22Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/25Jan2015/20150122_144129mbboldmb615mmAPPSNs003a001.feat/filtered_func_data.nii.gz');
        img4 = nii4.img;
    end
    if not(exist('nii5','var'))
         nii5 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/22Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/25Jan2015/20150122_144129mbboldmb615mmAPPSNs005a001.feat/filtered_func_data.nii.gz');
        img5 = nii5.img;
    end
    if not(exist('nii6','var'))
         nii6 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/22Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/25Jan2015/20150122_144129mbboldmb615mmAPPSNs007a001.feat/filtered_func_data.nii.gz');
        img6 = nii6.img;
    end
    if not(exist('nii7','var'))
        nii7 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/25Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/25Jan2015_50s_HP/20150125_124420mbboldmb615mmAPPSNs005a001.feat/filtered_func_data.nii.gz');
        img7 = nii7.img;
    end
    if not(exist('nii8','var'))
         nii8 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/25Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/25Jan2015_50s_HP/20150125_124420mbboldmb615mmAPPSNs007a001.feat/filtered_func_data.nii.gz');
        img8 = nii8.img;
    end
    if not(exist('nii9','var'))
         nii9 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/25Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/25Jan2015_50s_HP/20150125_124420mbboldmb615mmAPPSNs009a001.feat/filtered_func_data.nii.gz');
        img9 = nii9.img;
    end
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 20;
    for i = 7:9
        eval_str = d2s({'[z_img' i ', mean_img' i ', std_img' i '] = z_score_4D_nii(nii' i ');'});
        eval(eval_str);
    end
end
if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 30;
    for i = 7:9
        eval_str = d2s({'runs(' i ').z_img = z_img' i ';'});
        eval(eval_str);
    end
end

% if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% CELL_NUM = 1;
%     nii = nii1;
%     img = nii.img;
%     img_size = size(img);
%     x_size = img_size(1);
%     y_size = img_size(2);
%     z_size = img_size(3);
%     num_TRs = img_size(4);
%     mean_img = sum(img,4)/num_TRs;
% 
%     if GRAPHICS
%         X=50;Y=50;Z=50;
%         mi(rot90(squeeze(mean_img(X,:,:))),1,[2,2,1]);
%         mi(rot90(squeeze(mean_img(:,Y,:))),1,[2,2,2]);
%         mi(rot90(squeeze(mean_img(:,:,Z))),1,[2,2,3]);
%     end
% end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 
% 
% if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% CELL_NUM = 2;
%     
%     std_img = 0 * mean_img;
%     h=waitbar(0,'processing');
%     for x = 1:x_size
%         waitbar(x/x_size);movegui(h,'southeast');
%         for y = 1:y_size
%             for z = 1:z_size
%                 if mean_img(x,y,z) > 0
%                     std_img(x,y,z) = std(img(x,y,z,:));
%                 end
%             end
%         end
%     end
%     close(h);
%     if GRAPHICS
%         X=50;Y=50;Z=50;
%         mi(rot90(squeeze(std_img(X,:,:))),1,[2,2,1]);
%         mi(rot90(squeeze(std_img(:,Y,:))),1,[2,2,2]);
%         mi(rot90(squeeze(std_img(:,:,Z))),1,[2,2,3]);
%     end
% 
% end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 
% if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% CELL_NUM = 3;
%     
%     z_img = 0 * img;
%     h=waitbar(0,'processing');
%     for x = 1:x_size
%         waitbar(x/x_size);movegui(h,'southeast');
%         for y = 1:y_size
%             for z = 1:z_size
%                 if mean_img(x,y,z) > 0
%                     z_img(x,y,z,:) = img(x,y,z,:) - mean_img(x,y,z);
%                     z_img(x,y,z,:) = z_img(x,y,z,:) / std(img(x,y,z,:));
%                 end
%             end
%         end
%     end
%     close(h);
% end
% 
% if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% CELL_NUM = 4;
%     MN = -4;
%     MX = 4;
%     horAB=0*horA;
%     z_imgA = runs(1).z_img;
%     for i = 2:3
%         z_imgA = z_imgA + runs(i).z_img;
%     end
%     z_imgB = runs(4).z_img;
%     for i = 5:6
%         z_imgB = z_imgB + runs(i).z_img;
%     end
%     for tr = 1:num_TRs
%         if GRAPHICS
%             
%             X=50;Y=50;Z=37;
%             sagA = rot90(squeeze(z_imgA(X,:,:,tr))); sag(1,1)=MN;sag(1,2)=MX;
%             corA = rot90(squeeze(z_imgA(:,Y,:,tr))); cor(1,1)=MN;cor(1,2)=MX;
%             horA = rot90(squeeze(z_imgA(:,:,Z,tr))); hor(1,1)=MN;hor(1,2)=MX;
%             %sagA=reduceMatrixByHalf(reduceMatrixByHalf(sagA));corA=reduceMatrixByHalf(reduceMatrixByHalf(corA));horA=reduceMatrixByHalf(reduceMatrixByHalf(horA));
%             mi(sagA,1,[2,2,1],d2s({tr}));
%             mi(corA,1,[2,2,2],d2s({tr}));
%             mi(horA,1,[2,2,3],d2s({tr}));
%             
%             sagB = rot90(squeeze(z_imgB(X,:,:,tr))); sag(1,1)=MN;sag(1,2)=MX;
%             corB = rot90(squeeze(z_imgB(:,Y,:,tr))); cor(1,1)=MN;cor(1,2)=MX;
%             horB = rot90(squeeze(z_imgB(:,:,Z,tr))); hor(1,1)=MN;hor(1,2)=MX;
%             %sagB=reduceMatrixByHalf(reduceMatrixByHalf(sagB));corB=reduceMatrixByHalf(reduceMatrixByHalf(corB));horB=reduceMatrixByHalf(reduceMatrixByHalf(horB));
%             mi(sagB,2,[2,2,1],d2s({tr}));
%             mi(corB,2,[2,2,2],d2s({tr}));
%             mi(horB,2,[2,2,3],d2s({tr}));
%             horAB = horAB+horA.*horB;
%             mi(sagA.*sagB,3,[2,2,1],d2s({tr}));
%             mi(corA.*corB,3,[2,2,2],d2s({tr}));
%             mi(horA.*horB,3,[2,2,3],d2s({tr}));
%             mi(horAB,3,[2,2,4]);
%         end
%         pause(0.1);
%     end
% end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 50;
    num_TRs = 150;
    MN = -2*4;
    MX = 2*4;
    X=50;Y=50;Z=46;
    hor_sum = 0*rot90(squeeze(runs(i).z_img(:,:,Z,1)));

    if not(exist('BL_frames'))
        'load Barry Lyndon frames'
        BL_frames = zeros(7500,320,512,3,'uint8');
        for i = 1:7500
            BL_frames(i,:,:,:)=imread(d2s({'~/Desktop/Data/fmri_scanning_experiments/2015/1/17Jan2015_BarryLyndon_material_for_scanning/BarryLyndon_16Jan2015_1.avi_images/' i '.png'}));
        end
    end
    f=0;
    day_avg = zeros(138,138,'single');
    for tr = 1:num_TRs
        fprintf('%d\n',tr);
        
        %for i = 1:length(runs)
        day_avg = 0*day_avg;
        for day = 1:3
            hor_sum  = 0 * hor_sum;
            for j = 1:3
                i = (day-1)*3+j;
                img = runs(i).z_img;
                hor = rot90(squeeze(sum(img(:,:,(Z-1):(Z+1),tr),3)));
                day_avg = day_avg + hor;
                hor(1,1)=MN;hor(1,2)=MX;
                hor_sum = hor_sum + hor;       
                %mi(hor,1,[1,7,i],d2s({tr}));
            end

            mi(hor_sum,1,[2,3,day],d2s({tr}));%minutes ':' seconds}));

                %my_imwrite(hor_sum,d2s({tr '.hor'}),'TRs');
                if or(tr < 3,f<1)
                    fm = 0* BL_frames(1,:,:,:);
                else
                    fm = BL_frames(f+3,:,:,:);
                end
                %my_imwrite(fm,d2s({tr '.frame'}),'TRs');
        
        end
        mi(day_avg,1,[2,3,4],d2s({tr}));
        f1 = 1+round(2*(tr-1)*25-1*(4*25));
        f2 = round(2*(tr)*25-1*(4*25));
        tic

        for f = f1:f2
            if f > 0
%                 if length(BL_frames(i).fimg) == 0
%                     BL_frames(i).fimg=imread(d2s({'~/Desktop/Data/fmri_scanning_experiments/2015/1/17Jan2015_BarryLyndon_material_for_scanning/BarryLyndon_16Jan2015_1.avi_images/' f '.png'}));
%                 end
%                fimg=imread(d2s({'~/Desktop/Data/fmri_scanning_experiments/2015/1/17Jan2015_BarryLyndon_material_for_scanning/BarryLyndon_16Jan2015_1.avi_images/' f '.png'}));
                mi(BL_frames(f,:,:,:),1,[2,3,5],d2s({f}));
                pause(2/60);
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