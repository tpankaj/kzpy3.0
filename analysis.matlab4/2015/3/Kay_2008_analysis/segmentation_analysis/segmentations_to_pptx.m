function segmentations_to_pptx( images, segmentation1, segmentation2, segmentation3,  the_slide, description_str )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Look at segmentations in color. Write results to pptx file...
% from CELL_NUM = 40 in nb_15Jan2015_segmentation_analysis.m
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% segmentation1 is the controlling segmentation. If it is zeros, the image
% will be skipped. segmentation2 and segmentation3 can be [], in which case
% the are ignored.
%
%
%

GRAPHICS = 1;
%     if length(segmentation1) == 0
%         segmentation1 = 1+ 0 * images;
%     end
    if length(segmentation2) == 0
        segmentation2 = 0 * segmentation1;
    end
    if length(segmentation3) == 0
        segmentation3 = 0 * segmentation1;
    end
    
    if ~minn(size(segmentation1)==size(segmentation2))
        error('if ~minn(size(segmentation1)==size(segmentation2))');
    end
    if ~minn(size(segmentation1)==size(segmentation3))
        error('if ~minn(size(segmentation1)==size(segmentation3))');
    end

    ctr = 0;
    r = 3;
    c = 6;
    
    ifa_array = [];
    
    size_images = size(images);
    
    for i = 1:size_images(1)
        s1 = sqsing( segmentation1(i,:,:) );
        if summ( s1 ) > 0
            s2 = sqsing( segmentation2(i,:,:) );
            s3 = sqsing( segmentation3(i,:,:) );
            if GRAPHICS
                ci = gray_image_to_color(sqsing(images(i,:,:)));
                ci(:,:,1) = ci(:,:,1) .* (1-s1);
                ci(:,:,2) = ci(:,:,2) .* (1-s2);
                ci(:,:,3) = ci(:,:,3) .* (1-s3);
                ctr=ctr+1;
                mi(ci,1,[r,c,ctr],d2s({i}));
                ifa_array(ctr).ifa = pptx_mi( ci, [r c ctr], d2sp({'stimTrn ' i}), false );
                if ctr == 18
                    ctr = 0;
                    image_figure_create_PPTX_slide(...
                        the_slide, ifa_array, 'this_filename', ['FILE ', 'this_filename', '\n', 'this_file_text'], ...
                        d2s({description_str}));
                    ifa_array = [];
                end
            end   
        end
    end
    if length(ifa_array) > 0
        image_figure_create_PPTX_slide(...
                the_slide, ifa_array, 'this_filename', ['FILE ', 'this_filename', '\n', 'this_file_text'], ...
                d2s({description_str}));
    end
    
end


