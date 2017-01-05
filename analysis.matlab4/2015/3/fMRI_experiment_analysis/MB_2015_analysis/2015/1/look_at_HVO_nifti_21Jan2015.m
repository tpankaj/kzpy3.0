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




if 0
    n=100;
    for Z = 37:70%20:50
        img1crop = squeeze(img1(30:115,7:n,Z,:));
        img2crop = squeeze(img2(30:115,7:n,Z,:));
        img3crop = squeeze(img3(30:115,7:n,Z,:));

        c_img1 = sqsing(0*img1crop(:,:,1));
        c_img2 = sqsing(0*img2crop(:,:,1));
        c_img2_3 = sqsing(0*img2crop(:,:,1));

        size_img1crop = size(img1crop);
        img = sum(img1crop,3);
        h=waitbar(0,'processing');
        for X = 3:83
            waitbar(X/80);movegui(h,'southeast');
            for Y=3:(n-18)
                for x = X-1:X+1
                    for y = Y-1:Y+1
                        
                            cc1 = corrcoef(sqsing(img1crop(X,Y,:)),sqsing(img2crop(x,y,:)));
                            c_img1(x,y) = cc1(1,2);
                            cc2 = corrcoef(sqsing(img1crop(X,Y,:)),sqsing(img3crop(x,y,:)));
                            c_img2(x,y) = cc2(1,2);
                    end
                end
                c_img2_3(X,Y) = summ(c_img1([X-1 X X+1 X-1 X X+1 X-1 X X+1],[Y-1 Y-1 Y-1 Y Y Y  Y+1 Y+1 Y+1]))/16 + ...
                    summ(c_img2([X-1 X X+1 X-1 X X+1 X-1 X X+1],[Y-1 Y-1 Y-1 Y Y Y  Y+1 Y+1 Y+1]))/16;
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
end
c_img2_3_Z_thresh = 0*c_img2_3_Z;
for z = 37:50
    img = zeroToOneRange(sqsing(c_img2_3_Z(:,:,z))).^1;
%      img = single(uint8(255*(img-0.3)));
%      img = zeroToOneRange(img).^(1);
    c_img2_3_Z_thresh(:,:,z) = img;
    mi(c_img2_3_Z_thresh(:,:,z),2);
    pause;
end
mi(rot90(sum(c_img2_3_Z_thresh(:,:,37:53),3)),3)