function [ output_args ] = mi_nii( img, X,Y,Z,fig_num )
%function [ output_args ] = mi_nii( img, X,Y,Z, fig_num )
%
        img_size = size(img);
        
        mi(rot90(squeeze(img(X,:,:))),fig_num,[2,2,1],d2c({X Y Z}));
        hold on; plot([1,img_size(1)],[img_size(3)+1-Z,img_size(3)+1-Z],'r-'); plot([Y,Y],[1,img_size(3)],'r-');hold off;
        mi(rot90(squeeze(img(:,Y,:))),fig_num,[2,2,2]);
        hold on; plot([1,img_size(1)],[img_size(3)+1-Z,img_size(3)+1-Z],'r-'); plot([X,X],[1,img_size(3)],'r-');hold off;
        mi(rot90(squeeze(img(:,:,Z))),fig_num,[2,2,3]);
        hold on; plot([1,img_size(2)+1],[img_size(2)+1-Y,img_size(2)+1-Y],'r-'); plot([X,X],[1,img_size(2)+1],'r-');hold off;
end

