function [x_final,y_final,z_final] = mi_nii( img, X,Y,Z,opt_fig_num, opt_click )
%function [ output_args ] = mi_nii( img, X,Y,Z, fig_num )
%
        if nargin < 5
            opt_fig_num = 121;
        end
%                 t=squeeze(img4d(X,Y,Z,:)); mp({t},2,[2,1,1]); mp({abs(real(fft(t-mean(t))))},2,[2,1,2]);

        img_size = size(img);
        
        sagital = rot90(squeeze(img(X,:,:)));
        coronal = rot90(squeeze(img(:,Y,:)));
        horizontal = rot90(squeeze(img(:,:,Z)));
        sagital = zeroToOneRange(sagital);
        coronal = zeroToOneRange(coronal);
        horizontal = zeroToOneRange(horizontal);
        max_sag = max(size(sagital));
        max_cor = max(size(coronal));
        max_hor = max(size(horizontal));
        max_dim = max(max(max_sag,max_cor),max_hor);
        min_sag = min(size(sagital));
        min_cor = min(size(coronal));
        min_hor = min(size(horizontal));
        min_dim = min(min(min_sag,min_cor),min_hor);
        max_intensity = max(max(maxx(horizontal),maxx(sagital)),maxx(coronal));
        sagital(max_dim,max_dim)=0;%max_intensity; % this does padding so that all views are same size;
        coronal(max_dim,max_dim)=0;%max_intensity;
        horizontal(max_dim,max_dim)=0;%max_intensity;
        num_clicks = 0;
        if opt_click
            num_clicks = 1;
        end
        [selectedImages, Xs, Ys, displayMatrix ] = ...
            displayCellArrayOfPicturesAndClick( {sagital coronal horizontal},{'sagital','coronal','horizontal'},0,opt_fig_num,d2c({X Y Z}),num_clicks);
        
        if length(selectedImages) == 0
            x_final = X;
            y_final = Y;
            z_final = Z;
            return;
        end
        Xs
        Ys
        if selectedImages(1) == 1
            Y_new = round(Xs(1));
            X_new = X;
            Z_new = min_dim+1-round(Ys(1));

        elseif selectedImages(1) == 2
            X_new = round(Xs(1));
            Y_new = Y;
            Z_new = min_dim+1-round(Ys(1));

        elseif selectedImages(1) == 3
            Y_new = max_dim+1-round(Ys(1));
            X_new = round(Xs(1));
            Z_new = Z;
        else
            error('');
        end

        [x_final,y_final,z_final] = mi_nii( img, X_new,Y_new,Z_new,opt_fig_num,true );
%         displayCellArrayOfPicturesAndClick( {sagital coronal horizontal},{},0,opt_fig_num,'',0);
        
end

