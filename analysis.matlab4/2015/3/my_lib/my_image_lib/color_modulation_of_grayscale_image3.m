function ci = color_modulation_of_grayscale_image3(img,r,opt_g,opt_b, opt_lower_contrast)
%function ci = color_modulation_of_grayscale_image3(img,r,opt_g,opt_b, opt_lower_contrast)
%
% e.g.
%     a = sqsing(G.stimTrn512_int8(1,:,:));
%     b = sqsing(G.stimTrn512_int8(17,:,:));
%     c = sqsing(G.stimTrn512_int8(1469,:,:));
%     ci = color_modulation_of_grayscale_image2(a,zeroToOneRange(b).^4,zeroToOneRange(c).^4,[],1);
%     mi(ci,1);
%
%%%%%
% 11 January 2015, revising color_modulation_of_grayscale_image2 to
% color_modulation_of_grayscale_image3.
%
%
    if length(size(img))>2
        img_sum = sum(img,3);
        img_sum = zeroToOneRange(img); % ?
    else
        img_sum = zeroToOneRange(img);
    end
    
    if nargin > 4
        if opt_lower_contrast
            img_sum = zeroToOneRange(img_sum);
            img_sum = (1+img_sum)/3;
        end
    end
        
    ci = single(img*0); % ?
    ci(:,:,1)=img_sum;
    ci(:,:,2)=img_sum;
    ci(:,:,3)=img_sum;

    ci=ci/max(max(max(ci)));

    if length(r)>0 % ?
        r = zeroToOneRange(r);
        ci(:,:,1) = (1-r) .* ci(:,:,1) + r  .* ci(:,:,1)/maxx(ci(:,:,1));
        ci(:,:,2) = (1-r) .* ci(:,:,2);
        ci(:,:,3) = (1-r) .* ci(:,:,3);
    end

    if nargin > 2
        if length(opt_g)>0
                opt_g = zeroToOneRange(opt_g);
                ci(:,:,2) = (1-opt_g) .* ci(:,:,2) + opt_g;%  .* ci(:,:,2)/maxx(ci(:,:,2));
        end
    end
    if nargin > 3
        if length(opt_b)>0
                opt_b = zeroToOneRange(opt_b);
                ci(:,:,3) = (1-opt_b) .* ci(:,:,3) + opt_b;%  .* ci(:,:,3)/maxx(ci(:,:,3));
                ci(:,:,2) = (1-opt_b) .* ci(:,:,2);
                ci(:,:,1) = (1-opt_b) .* ci(:,:,1);
        end
    end
end

