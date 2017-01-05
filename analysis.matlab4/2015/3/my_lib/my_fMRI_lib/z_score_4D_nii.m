function z_scored_img = z_score_4D_nii(nii)
% function [z_img, mean_img, std_img] = z_score_4D_nii(nii)
%
GRAPHICS = true;

    img = nii.img;

    img_size = size(img);
    x_size = img_size(1);
    y_size = img_size(2);
    z_size = img_size(3);
    num_TRs = img_size(4);

    mean_img = sum(img,4)/num_TRs;

    if GRAPHICS
        X=x_size/2;Y=y_size/2;Z=z_size/2;
        X=round(X);Y=round(Y);Z=round(Z);
         mi_nii( mean_img, X, Y, Z, 1, false );
%         
%         mi(rot90(squeeze(mean_img(X,:,:))),1,[2,2,1]);title('T2*');
%         mi(rot90(squeeze(mean_img(:,Y,:))),1,[2,2,2]);
%         mi(rot90(squeeze(mean_img(:,:,Z))),1,[2,2,3]);
    end

    std_img = 0 * mean_img;
    h=waitbar(0,'processing voxel variance');
    for x = 1:x_size
        waitbar(x/x_size);movegui(h,'southeast');
        for y = 1:y_size
            for z = 1:z_size
                if mean_img(x,y,z) > 0
                    std_img(x,y,z) = std(img(x,y,z,:));
                end
            end
        end
    end
    close(h);
    if GRAPHICS
         mi_nii( std_img, X, Y, Z, 2, false );
        X=x_size/2;Y=y_size/2;Z=z_size/2;
%         mi(rot90(squeeze(std_img(X,:,:))),1,[2,2,1]);title('std of T2*');
%         mi(rot90(squeeze(std_img(:,Y,:))),1,[2,2,2]);
%         mi(rot90(squeeze(std_img(:,:,Z))),1,[2,2,3]);
    end

    z_img = 0 * img;
    h=waitbar(0,'processing z-scoring of voxels');
    for x = 1:x_size
        waitbar(x/x_size);movegui(h,'southeast');
        for y = 1:y_size
            for z = 1:z_size
                if mean_img(x,y,z) > 0
                    z_img(x,y,z,:) = img(x,y,z,:) - mean_img(x,y,z);
                    z_img(x,y,z,:) = z_img(x,y,z,:) / std(img(x,y,z,:));
                end
            end
        end
    end
    close(h);

    z_scored_img.z_img = z_img;
    z_scored_img.mean_img = mean_img;
    z_scored_img.std_img = std_img;
end

