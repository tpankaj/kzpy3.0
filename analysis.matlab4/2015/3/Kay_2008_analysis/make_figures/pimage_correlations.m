function R = pimage_correlations(Sx_vri_dataset)
%function R = pimage_correlations(Sx_vri_dataset)
%
% e.g., R = pimage_correlations(S1_vri_dataset);
%
% 7 January 2015
% compare the correlation of V1 to V1 P-images across trials with the
% correlation of V1 to V2 P-images across trials.
%
% for reference, will need these data:
% load('~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/after_January_2014/15Oct2014_vri_datasets/S1_vri_dataset.735887.8626.mat')
%%%%%%%%%%%%

    graphics1 = false;
    
    for img = 1:1750;
        
        A = Sx_vri_dataset.V1;
        B = Sx_vri_dataset.V2;
        C = Sx_vri_dataset.V1V2;
        
        r = bbb(A.coverage_mask,B.coverage_mask,A.Trn(img).presentation(1).z_img,A.Trn(img).presentation(2).z_img,graphics1);
        Rs_V1_vs_V1(img) = r;
        

        r = bbb(A.coverage_mask,B.coverage_mask,A.Trn(img).presentation(1).z_img,B.Trn(img).presentation(2).z_img,graphics1);
        Rs_V1_vs_V2(img) = r;
        
        r = bbb(A.coverage_mask,B.coverage_mask,A.Trn(img).average.z_img,B.Trn(img).average.z_img,graphics1);
        Rs_V1_vs_V2_average(img) = r;
        
        r = bbb(C.coverage_mask,C.coverage_mask,C.Trn(img).average.z_img,sqrt(zeroToOneRange(C.Trn(img).predicted.z_img)),graphics1 );
        Rs_V1_vs_V2_vs_model(img) = r;
    
    end
    
    
    RR = corrcoef(Rs_V1_vs_V1,Rs_V1_vs_V2); % = 0.7173
    R = RR(1,2);
    figure(1);
    plot(Rs_V1_vs_V1,Rs_V1_vs_V2,'o');axis('equal');
    title(d2s({'Cross-trial correlation of P-images, r = ' R}));
    xlabel('V1 vs V1');
    ylabel('V1 vs V2');

    fsp(2,[1,2,1]);
    hist(Rs_V1_vs_V1,50);
    title('S1, cross-trial correlation P-images, V1 vs V1');
    xlabel(d2s({'median = ' median(Rs_V1_vs_V1)}));
    
    fsp(2,[1,2,2]);
    hist(Rs_V1_vs_V2,50);
    title('S1, cross-trial correlation P-images, V1 vs V2');
    xlabel(d2s({'median = ' median(Rs_V1_vs_V2)}));
    
    
    figure(3);
    hist(Rs_V1_vs_V2_vs_model,50);
    title('S1, correlation of V1V2 data P-images with V1V2 model P-images');
    xlabel(d2s({'median = ' median(Rs_V1_vs_V2_vs_model)}));
    
    figure(4);
    hist(Rs_V1_vs_V2_average,50);
    title('S1, average-trial correlation P-images, V1 vs V2');
    xlabel(d2s({'median = ' median(Rs_V1_vs_V2_average)}));
    
end

function [ r p pimage1_zvals pimage2_zvals ] = bbb(pimage1_coverage,pimage2_coverage,pimage1_zimg,pimage2_zimg,GRAPHICS)

    joint_coverage = pimage1_coverage .* pimage2_coverage;

    joint_coverage = reshape(joint_coverage, 128^2, 1);
    nonzero_pixels = find(joint_coverage > 0);
    pimage1_zimg = reshape(pimage1_zimg, 128^2, 1);
    pimage2_zimg = reshape(pimage2_zimg, 128^2, 1);

    pimage1_zvals = pimage1_zimg(nonzero_pixels);

    pimage2_zvals = pimage2_zimg(nonzero_pixels);



    cc = corrcoef( pimage1_zvals, pimage2_zvals );
    r = cc(1,2);

    p = nan;

    if GRAPHICS
        mp({pimage1_zvals,pimage2_zvals,'o'},1);
        axis('equal')
        title(r);
        pause;
    end
end


% pimage1_coverage = A.coverage_mask;
% pimage2_coverage = B.coverage_mask;
% pimage1_zimg = A.Trn(img).presentation(1).z_img;
% pimage2_zimg = B.Trn(img).presentation(2).z_img;
% pimage1_zimg = A.Trn(img).average.z_img;
% pimage2_zimg = B.Trn(img).predicted.z_img;


