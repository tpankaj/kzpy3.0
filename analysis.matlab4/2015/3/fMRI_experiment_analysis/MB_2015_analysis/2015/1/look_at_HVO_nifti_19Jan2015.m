if not(exist('nii1','var'))
    nii1 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/20150118_164630mbboldmb615mmAPPSNs002a001.feat/filtered_func_data.nii.gz');
    img1 = nii1.img;
end
if not(exist('nii2','var'))
    nii2 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/20150118_164630mbboldmb615mmAPPSNs004a001.feat/filtered_func_data.nii.gz');
    img2 = nii2.img;
end
if not(exist('nii3','var'))
    nii3 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/20150118_164630mbboldmb615mmAPPSNs006a001.feat/filtered_func_data.nii.gz');
    img3 = nii3.img;
end





n=100;
for z = 30:70%20:50
img1crop = squeeze(img1(30:115,7:n,z,:));
img2crop = squeeze(img2(30:115,7:n,z,:));
img3crop = squeeze(img3(30:115,7:n,z,:));

% img1crop = squeeze(img1(30:115,z,10:100,:));
% img2crop = squeeze(img2(30:115,z,10:100,:));
% img3crop = squeeze(img3(30:115,z,10:100,:));

% img1crop = squeeze(sum(img1(30:115,7:n,(z-1):(z+1),:),3));
% img2crop = squeeze(sum(img2(30:115,7:n,(z-1):(z+1),:),3));
% img3crop = squeeze(sum(img3(30:115,7:n,(z-1):(z+1),:),3));
c_img1 = sqsing(0*img1crop(:,:,1));
c_img2 = sqsing(0*img2crop(:,:,1));
c_img2_3 = sqsing(0*img2crop(:,:,1));

size_img1crop = size(img1crop);
img = sum(img1crop,3);
h=waitbar(0,'processing');
for X = 3:83
    waitbar(X/80);movegui(h,'southeast');
    %X
for Y=3:(n-18)%60
% for x = X-1:X+1%1:size_img1crop(1)
%     for y = Y-1:Y+1%1:size_img1crop(2)
for x = X%1:size_img1crop(1)
    for y = Y%1:size_img1crop(2)
        cc1 = corrcoef(sqsing(img1crop(x,y,:)),sqsing(img2crop(X,Y,:)));
        c_img1(x,y) = cc1(1,2);
        cc2 = corrcoef(sqsing(img1crop(x,y,:)),sqsing(img3crop(X,Y,:)));
        c_img2(x,y) = cc2(1,2);
        c_img2_3(X,Y) = summ(c_img1([X-1 X X+1 X-1 X X+1 X-1 X X+1],[Y-1 Y-1 Y-1 Y Y Y  Y+1 Y+1 Y+1]))/16 + ...
            summ(c_img2([X-1 X X+1 X-1 X X+1 X-1 X X+1],[Y-1 Y-1 Y-1 Y Y Y  Y+1 Y+1 Y+1]))/16;
%         c_img2_3(X,Y) = summ(c_img1(X,Y))/16 + ...
%             summ(c_img2(X,Y))/16;
    end
end
for x = X%1:size_img1crop(1)
    for y = Y%1:size_img1crop(2)
        cc1 = corrcoef(sqsing(img1crop(x,y,:)),sqsing(img2crop(X,Y,:)));
        c_img1(x,y) = cc1(1,2);
        cc2 = corrcoef(sqsing(img1crop(x,y,:)),sqsing(img3crop(X,Y,:)));
        c_img2(x,y) = cc2(1,2);
        c_img2_3(X,Y) = summ(c_img1([X-1 X X+1 X-1 X X+1 X-1 X X+1],[Y-1 Y-1 Y-1 Y Y Y  Y+1 Y+1 Y+1]))/16 + ...
            summ(c_img2([X-1 X X+1 X-1 X X+1 X-1 X X+1],[Y-1 Y-1 Y-1 Y Y Y  Y+1 Y+1 Y+1]))/16;
%         c_img2_3(X,Y) = summ(c_img1(X,Y))/16 + ...
%             summ(c_img2(X,Y))/16;
    end
end
end
end
close(h);
mi(img,1,[1,3,1]);%hold on;plot(Y,X,'o');hold off;
c_img2_3(find(not(isfinite(c_img2_3))))=0;

mi(c_img2_3(:,:),1,[1,3,2],d2s({z}));
c_img2_z = zeroToOneRange(c_img2_3);
c_img2_thresh = c_img2_z;
c_img2_thresh(find(c_img2_thresh<0.7))=0;
ci = color_modulation_of_grayscale_image3(img,c_img2_thresh,c_img2_thresh,[], false);
mi(ci,1,[1,3,3],d2s({z}));
drawnow;%my_pause
c_img2_3_Z(:,:,z) = c_img2_3;
end
