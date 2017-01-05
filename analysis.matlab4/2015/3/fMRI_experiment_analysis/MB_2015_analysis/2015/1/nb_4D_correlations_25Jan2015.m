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
CELL_NUM = 10;

    if not(exist('cat_z_imgs','var'))
        cat_z_imgs = zeros(138,138,108,150*9,'single');
        for i = 1:9
            i
            cat_z_imgs(:,:,:,((i-1)*150+1):(i*150)) = runs(i).z_img;
        end
    end
    
    if not(exist('mask','var'))
        mask = zeros(138,138,108,'uint8');
        for x = 1:138
            for y = 1:138
                for z = 1:108
                    if not(cat_z_imgs(x,y,z,1) == 0)
                        mask(x,y,z) = 1;
                    end
                end
            end
        end
    end
    
    %if not(exist('r_img'))
        h = waitbar(0,'processing');movegui('southeast');
    %    r_img = zeros(138,138,108,'single');
        for x = 1:138
            
            waitbar(x/138);
            for y = 1:138
                for z = 1:108            
                    if and(mask(x,y,z),or(not(isfinite(r_img(x,y,z))),r_img(x,y,z)==0))
                        r_sum = 0;
                        for dx = -1:1
                            for dy = -1:1
                                for dz = -1:1
                                    if and(x+dx>0,and(y+dy>0,z+dz>0))
                                        cc = corrcoef(cat_z_imgs(x,y,z,:),cat_z_imgs(x+dx,y+dy,z+dz,:));
                                        c = cc(1,2);
                                        if(isfinite(c))
                                            r_sum = r_sum + c;
                                        end
                                    end
                                end
                            end
                        end
                        r_img(x,y,z) = r_sum - 1;
                    end
                end
            end
            mi_nii(r_img,x,20+randi(40),20+randi(40),1);title(x);
        end
        close(h);
    %end
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 100;
    r_img = zeros(138,138,108);
    if not(exist('cat_z_imgs','var'))
        cat_z_imgs = zeros(138,138,108,150*1,'single');
        for i = 1:1
            i
            cat_z_imgs(:,:,:,((i-1)*150+1):(i*150)) = runs(i).z_img;
        end
    end
    
    if not(exist('mask','var'))
        mask = zeros(138,138,108,'uint8');
        for x = 1:138
            for y = 1:138
                for z = 1:108
                    if not(cat_z_imgs(x,y,z,1) == 0)
                        mask(x,y,z) = 1;
                    end
                end
            end
        end
    end
    
    %if not(exist('r_img'))
        h = waitbar(0,'processing');movegui('southeast');
    %    r_img = zeros(138,138,108,'single');
        for x = 1:138
            
            waitbar(x/138);
            for y = 1:138
                for z = 1:108            
                    if and(mask(x,y,z),or(not(isfinite(r_img(x,y,z))),r_img(x,y,z)==0))
                        r_sum = 0;
                        for dx = -1:1
                            for dy = -1:1
                                for dz = -1:1
                                    if and(x+dx>0,and(y+dy>0,z+dz>0))
                                        cc = corrcoef(cat_z_imgs(x,y,z,:),cat_z_imgs(x+dx,y+dy,z+dz,:));
                                        c = cc(1,2);
                                        if(isfinite(c))
                                            r_sum = r_sum + c;
                                        end
                                    end
                                end
                            end
                        end
                        r_img(x,y,z) = r_sum - 1;
                    end
                end
            end
            mi_nii(r_img,x,20+randi(40),20+randi(40),1);title(x);
        end
        close(h);
    %end
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 20;
    if not(exist('mean_func','var'))
        mean_func = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/25Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/28Jan2015_50s_HP_motion_corrected_to_22Jan2015/20150125_124420mbboldmb615mmAPPSNs005a001.feat/mean_func.nii.gz');
    end
    for x = 138:-1:1
        mi_nii(mean_func.img,138/2,x,30,1);
        mi_nii(r_img,138/2,x,30,2);
        %mi_nii(c,138/2,x,30,3);
        pause;
    end
end

if 1
CELL_NUM = 30;
     mi_nii(r_img,XYZ(1),XYZ(2),XYZ(3),2);
     mi_nii(mean_func.img,XYZ(1),XYZ(2),XYZ(3),3);
     [y,z] = ginput(1);
     XYZ = [XYZ(1) round(y) 109-round(z)]%[71 21 60]; [54    44    39];
    
    r1r2img=zeros(138,138,'single');
    mi_nii(r_img,XYZ(1),XYZ(2),XYZ(3),2);
    mi_nii(mean_func.img,XYZ(1),XYZ(2),XYZ(3),3);
    for X = 135:-1:5
        X
        for Y = 10:120
    r1 = (1:150)*0;
    r2 = 0*r;
    for i = 1:4
        for x = -1:1
            for y = -1:1
                for z = -1:1
        r1 = r1 + squeeze(runs(i).z_img(X+x,Y+y,XYZ(3)+z,:))';
        r2 = r2 + squeeze(runs(i+4).z_img(X+x,Y+y,XYZ(3)+z,:))';
                end
            end
        end
    end
    r1 = r1 / 4/28;
    r2 = r2 / 4/28;
    cc=corrcoef(r1,r2);
    r1r2img(X,Y)=cc(1,2);
    
        end
        r1r2img(find(~isfinite( r1r2img)))=0;
        mi(rot90(r1r2img),2,[2,2,4]);
    end
    
    %mp({r1,r2,'o'},2,[2,2,4],d2s({cc(1,2)}));
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 20;
    masked = find(mask>0);
    t2 = mean_func.img(masked);
    c = r_img(masked);
    figure(100);plot(t2,c,'.')
end