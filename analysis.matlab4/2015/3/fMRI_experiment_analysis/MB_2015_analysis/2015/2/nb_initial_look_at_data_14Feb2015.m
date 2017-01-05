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
% Looking at z-scored data
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        img_lst1={};
        for j = 1:40
            img_lst1{j}=squeeze(z_scored_20150212_081609mbboldmb620mmAPPSNs006a001.mean_img(:,:,j+10));
        end
        displayCellArrayOfPicturesAndClick( img_lst1,{},0,100,d2s({i}),0);
end
if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    a=0;b=0;
    for i = (a+1):444
        img_lst1={};
        img_lst2={};
        
        indicies1 = [(0*40+i-a):(0*40+i+b) (2*40+i-a):(2*40+i+b) (4*40+i-a):(4*40+i+b) (6*40+i-a):(6*40+i+b)];
        indicies2 = [(1*40+i-a):(1*40+i+b) (3*40+i-a):(3*40+i+b) (5*40+i-a):(5*40+i+b) (7*40+i-a):(7*40+i+b)];

        for j = 1:40
            img_lst1{j}=squeeze(sum(z_sum(:,:,j+10,indicies1),4));
            img_lst2{j}=squeeze(sum(z_sum(:,:,j+10,indicies2),4));
        end
        displayCellArrayOfPicturesAndClick( img_lst1,{},0,98,d2s({i}),0);
        displayCellArrayOfPicturesAndClick( img_lst2,{},0,99,d2s({i}),0);
        pause(3)
    end
end
if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    z1 = z_scored_filtered_func_data_8.z_img;
     z2=z_scored_filtered_func_data_13.z_img;
     z3 = z1+z2;
    for i = 2:444
        mi_nii(sum(squeeze(z1(:,:,:,(i-1):(i+1))),4),57,20,22,1,false)
        mi_nii(sum(squeeze(z2(:,:,:,(i-1):(i+1))),4),57,20,22,2,false)
        mi_nii(sum(squeeze(z3(:,:,:,(i-1):(i+1))),4),57,20,22,3,false)
        pause(1.5)
    end
end
if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    t=0;
    z1 = z_scored_filtered_func_data_6.z_img;
    z2 = z_scored_filtered_func_data_8.z_img;
    z3 = z_scored_filtered_func_data_10.z_img;
    z4 = z_scored_20150214_082112mbboldmb620mmAPPSNs006a001.z_img;
    z5 = z_scored_20150214_082112mbboldmb620mmAPPSNs008a001.z_img;
    z6 = z_scored_20150214_082112mbboldmb620mmAPPSNs010a001.z_img;
    z_sum = z1+z2+z3+z4+z5+z6;
    a=1;
    X=57;Y=15;Z = 25;
    for i = (a+1):444
        indicies1 = [(0*40+i-a):(0*40+i+a)];% (2*40+i-a):(2*40+i+a) (4*40+i-a):(4*40+i+a) (6*40+i-a):(6*40+i+a)];
        indicies2 = [(1*40+i-a):(1*40+i+a)];% (3*40+i-a):(3*40+i+a) (5*40+i-a):(5*40+i+a) (7*40+i-a):(7*40+i+a)];

        mi_nii(sum(squeeze(z1(:,:,:,indicies1)),4),X,Y,Z,1,false);
        mi_nii(sum(squeeze(z2(:,:,:,indicies1)),4),X,Y,Z,2,false);
        mi_nii(sum(squeeze(z3(:,:,:,indicies1)),4),X,Y,Z,3,false);
        mi_nii(sum(squeeze(z_sum(:,:,:,indicies1)),4),X,Y,Z,4,false);

        mi_nii(sum(squeeze(z1(:,:,:,indicies2)),4),X,Y,Z,5,false);
        mi_nii(sum(squeeze(z2(:,:,:,indicies2)),4),X,Y,Z,6,false);
        mi_nii(sum(squeeze(z3(:,:,:,indicies2)),4),X,Y,Z,7,false);
        mi_nii(sum(squeeze(z_sum(:,:,:,indicies2)),4),X,Y,Z,8,false);
        %mi_nii(sum(squeeze(z_sum(:,:,:,indicies2)-z_sum(:,:,:,indicies1)),4),X,Y,Z,9,false);
        axis('on');xlabel(0.9*i);
        pause(0.9);
    end
end
if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    fft_img = zeros(138,138,'single');
for z = 2:35
for xx = 2:137
for yy = 2:137
    t = squeeze(z_scored_img.z_img(xx,yy,z,:));
    t = t + squeeze(z_scored_img.z_img(xx+1,yy,z,:));
    t = t + squeeze(z_scored_img.z_img(xx-1,yy,z,:));
    t = t + squeeze(z_scored_img.z_img(xx,yy-1,z,:));
    t = t + squeeze(z_scored_img.z_img(xx,yy+1,z,:));
    t = t + squeeze(z_scored_img.z_img(xx,yy,z-1,:));
    t = t + squeeze(z_scored_img.z_img(xx,yy,z+1,:));
    f = abs(real(fft(conv(t-mean(t),k))));
    m = mean(f(49:52))/mean(f);
    fft_img(xx,yy) = m;
    if m>8
        mp({f},2,[2,1,2]);
        
    end
end
end
mi(fft_img,1,[1,1,1],d2c({xx z}));
my_pause(1);

end
    
end


if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 10;
    sd=40;%img_wid/2^5;
    img_wid = 512+2*16;
    img = square_single_zeros(img_wid);
    img_blank = img;
    
    g=gaussian_matrix2(4*sd,sd);
    
    mi(img);
    ctr=0;
    for x = (-img_wid/2+2*sd+1):(2*sd):(img_wid/2-2*sd+1)
        for y = (-img_wid/2+2*sd+1):(2*sd):(img_wid/2-2*sd+1)
            ctr=ctr+1;
            if randn(1)>0
                img_blank = 0*img_blank;
                img = img + place_img_A_in_img_B(g,img_blank,x,y);
                mi(img,1);drawnow;
            end
        end
    end
    ctr
end
if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    h = 0*(1:10000);
    for i = 1:10000
        h(i) = model_HRF(i/1000);
    end
    s = 0*(1:448);
    t=0*(1:(300*1000));
    for i = 0:1:47
        i
        t(6000+(i*6000):(6000+i*6000+4000)) = 1;
    end
    c=conv(t,h,'same');
    c=c-mean(c);c=c/std(c);
    f=real(abs(fft(c)));
    mp({c,'.-'},9,[2,1,1]);
    mp({f,'o-'},9,[2,1,2]);axis([0,100,0,max(f)]);

end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 100;
    A_B_12_1 = imread('/Users/davidzipser/Desktop/fsl temp/12Feb/cluster_zstat3.png');
    A_B_12_2 = imread('/Users/davidzipser/Desktop/fsl temp/12Feb/cluster_zstat3-1.png');
    A_B_12_3 = imread('/Users/davidzipser/Desktop/fsl temp/12Feb/cluster_zstat3-2.png');
    B_A_12_1 = imread('/Users/davidzipser/Desktop/fsl temp/12Feb/cluster_zstat4.png');
    B_A_12_2 = imread('/Users/davidzipser/Desktop/fsl temp/12Feb/cluster_zstat4-1.png');
    B_A_12_3 = imread('/Users/davidzipser/Desktop/fsl temp/12Feb/cluster_zstat4-2.png');
    A_B_14_1 = imread('/Users/davidzipser/Desktop/fsl temp/14Feb/cluster_zstat3.png');
    A_B_14_2 = imread('/Users/davidzipser/Desktop/fsl temp/14Feb/cluster_zstat3-1.png');
    A_B_14_3 = imread('/Users/davidzipser/Desktop/fsl temp/14Feb/cluster_zstat3-2.png');
    B_A_14_1 = imread('/Users/davidzipser/Desktop/fsl temp/14Feb/cluster_zstat4.png');
    B_A_14_2 = imread('/Users/davidzipser/Desktop/fsl temp/14Feb/cluster_zstat4-1.png');
    B_A_14_3 = imread('/Users/davidzipser/Desktop/fsl temp/14Feb/cluster_zstat4-2.png');
    mi((A_B_12_1)/6+(A_B_12_2)/6+(A_B_12_3)/6+(A_B_14_1)/6+(A_B_14_2)/6+(A_B_14_3)/6,1999,[1,2,1]);
    mi((B_A_12_1)/6+(B_A_12_2)/6+(B_A_12_3)/6+(B_A_14_1)/6+(B_A_14_2)/6+(B_A_14_3)/6,1999,[1,2,2]);
end
