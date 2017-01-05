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
    z1 = z_scored_filtered_func_data_8.z_img;
    z2 = z_scored_filtered_func_data_13.z_img;
    for i = 2:444
        img_lst1={};
        img_lst2={};
        for j = 1:20
            img_lst1{j}=squeeze(sum(z1(:,:,j+10,(i-1):(i+1)),4));
            img_lst2{j}=squeeze(sum(z2(:,:,j+10,(i-1):(i+1)),4));
        end
        displayCellArrayOfPicturesAndClick( img_lst1,{},0,98,d2s({i}),0);
        displayCellArrayOfPicturesAndClick( img_lst2,{},0,99,'',0);
        pause(3)
    end
end
if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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
if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    z1 = z_scored_filtered_func_data6.z_img;
    z2 = z_scored_filtered_func_data8.z_img;
    z2b = z_scored_filtered_func_data6.z_img;
    z3 = z1+z2+z2b;
    for i = 2:444
        mi_nii(sum(squeeze(z1(:,:,:,(i-1):(i+3))),4),57,27,14,1,false)
        mi_nii(sum(squeeze(z2(:,:,:,(i-1):(i+3))),4),57,27,14,2,false)
        mi_nii(sum(squeeze(z3(:,:,:,(i-1):(i+3))),4),57,27,14,3,false)
        pause(0.67)
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
