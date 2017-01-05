if not(exist('nii1','var'))
%     nii1 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/20150118_164630mbboldmb615mmAPPSNs002a001.feat/filtered_func_data.nii.gz');
%    nii1 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/24Jan2015/20150118_164630mbboldmb615mmAPPSNs003a001.feat/filtered_func_data.nii.gz');
    nii1 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/22Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/24Jan2015/20150122_144129mbboldmb615mmAPPSNs003a001.feat/filtered_func_data.nii.gz');
    img1 = nii1.img;
end
if not(exist('nii2','var'))
%     nii2 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/20150118_164630mbboldmb615mmAPPSNs004a001.feat/filtered_func_data.nii.gz');
%     nii2 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/24Jan2015/20150118_164630mbboldmb615mmAPPSNs005a001.feat/filtered_func_data.nii.gz');
     nii2 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/22Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/24Jan2015/20150122_144129mbboldmb615mmAPPSNs005a001.feat/filtered_func_data.nii.gz');
    img2 = nii2.img;
end
if not(exist('nii3','var'))
%     nii3 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/20150118_164630mbboldmb615mmAPPSNs006a001.feat/filtered_func_data.nii.gz');
%     nii3 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/24Jan2015/20150118_164630mbboldmb615mmAPPSNs007a001.feat/filtered_func_data.nii.gz');
     nii3 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/22Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/24Jan2015/20150122_144129mbboldmb615mmAPPSNs007a001.feat/filtered_func_data.nii.gz');
    img3 = nii3.img;
end
if not(exist('nii4','var'))
%     nii1 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/20150118_164630mbboldmb615mmAPPSNs002a001.feat/filtered_func_data.nii.gz');
%    nii1 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/24Jan2015/20150118_164630mbboldmb615mmAPPSNs003a001.feat/filtered_func_data.nii.gz');
    nii4 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/22Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/24Jan2015/20150122_144129mbboldmb615mmAPPSNs003a001.feat/filtered_func_data.nii.gz');
    img4 = nii4.img;
end
if not(exist('nii5','var'))
%     nii2 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/20150118_164630mbboldmb615mmAPPSNs004a001.feat/filtered_func_data.nii.gz');
%     nii2 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/24Jan2015/20150118_164630mbboldmb615mmAPPSNs005a001.feat/filtered_func_data.nii.gz');
     nii5 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/22Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/24Jan2015/20150122_144129mbboldmb615mmAPPSNs005a001.feat/filtered_func_data.nii.gz');
    img5 = nii5.img;
end
if not(exist('nii6','var'))
%     nii3 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/20150118_164630mbboldmb615mmAPPSNs006a001.feat/filtered_func_data.nii.gz');
%     nii3 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/18Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/24Jan2015/20150118_164630mbboldmb615mmAPPSNs007a001.feat/filtered_func_data.nii.gz');
     nii6 = load_untouch_nii('~/Desktop/Data/subjects/HVO/2015/1/22Jan2015_MB_Zipser_Pilot_13Nov2014_HVO/fsl/24Jan2015/20150122_144129mbboldmb615mmAPPSNs007a001.feat/filtered_func_data.nii.gz');
    img6 = nii6.img;
end

c_img2_3_Z = zeros(108,138,138,'single');
ZMIN = 20;
ZMAX = 80;
if 1
    n=100;
    for Z = ZMIN:ZMAX%20:50
        img1crop = squeeze(img1(:,:,Z,:)+img2(:,:,Z,:)+img3(:,:,Z,:));
        img2crop = squeeze(img4(:,:,Z,:)+img5(:,:,Z,:)+img6(:,:,Z,:));

        c_img1 = sqsing(0*img1crop(:,:,1));
        c_img2_3 = sqsing(0*img2crop(:,:,1));

        size_img1crop = size(img1crop);
        img = sum(img1crop,3);
        h=waitbar(0,'processing');
        for X = 25:125
            waitbar(X/80);movegui(h,'southeast');
            for Y=10:60
                if img(X,Y)>0
                    for x = X-1:X+1
                        for y = Y-1:Y+1

                                cc1 = corrcoef(sqsing(img1crop(X,Y,:)),sqsing(img2crop(x,y,:)));
                                c_img1(x,y) = cc1(1,2);
                        end
                    end
                    c_img2_3(X,Y) = summ(c_img1([X-1 X X+1 X-1 X X+1 X-1 X X+1],[Y-1 Y-1 Y-1 Y Y Y  Y+1 Y+1 Y+1]));
%                    c_img2_3(X,Y) = c_img1(X,Y)/2 + c_img2(X,Y)/2;
                end
            end
        end
        close(h);
        mi(img,1,[1,3,1]);%hold on;plot(Y,X,'o');hold off;
        c_img2_3(find(not(isfinite(c_img2_3))))=0;

        
        c_img2_z = zeroToOneRange(c_img2_3);
        c_img2_thresh = c_img2_z;
        c_img2_thresh(find(c_img2_thresh<0.7))=0;
        ci = color_modulation_of_grayscale_image3(img,c_img2_thresh,c_img2_thresh,[], false);
        mi(ci,1,[1,3,3],d2s({Z}));
        drawnow;%my_pause
        c_img2_3_Z(Z,:,:) = c_img2_3';
        mi(c_img2_3_Z(Z,:,:),1,[1,3,2],d2s({Z}));
    end
end

mn = min(min(min(min(min(min(c_img2_3_Z))))));
c_img2_3_Z = c_img2_3_Z - mn;
mx = max(max(max(max(max(max(c_img2_3_Z))))));
c_img2_3_Z = c_img2_3_Z / mx;
    

c_img2_3_Z_thresh = 0*c_img2_3_Z;
for z = 37:50
    img = zeroToOneRange(sqsing(c_img2_3_Z(:,:,z))).^1;
%      img = single(uint8(255*(img-0.3)));
%      img = zeroToOneRange(img).^(1);
    c_img2_3_Z_thresh(:,:,z) = img;
    mi(c_img2_3_Z_thresh(z,:,:),2);
    pause;
end
mi(rot90(sum(c_img2_3_Z_thresh(:,:,37:53),3)),3)