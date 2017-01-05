%%%%%%%%%%% Standard Notebook Beginning %%%%%%%%%%%%
%
clc; fprintf('%s\n',[mfilename ' (' mfilename('fullpath') '.m)']);
this_filename = mfilename('fullpath');
this_file_text = fileread([this_filename,'.m']);
if not(exist('G'))
    error('NOTE: run local_startup.m and G_initalize manually at the beginning of the Matlab session.');
end
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 11 January 2015.
% Relearn how to write powerpoint slides
% This notebook creates/modifies test.pptx on the Desktop
the_slide = '~/Desktop/test.pptx'; the_slide
% 15 Jan. 2015, tested use of color images (in cell 1.1)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This shows example of using pptx_mi function, which gives a
% limited-option but simple access to the pptx writing functions.
    CELL_NUM = 1;

    ctr = 0;

    r = 3;
    c = 6;
    ifa_array = [];

    for ctr = 1:(r*c)
        img_num = ctr -1 + randi(1750-r*c);
        ifa_array(ctr).ifa = pptx_mi( get_Kay_image('Trn',img_num), [r c ctr], d2sp({'stimTrn ' img_num}), false );
    end


    image_figure_create_PPTX_slide(...
            the_slide, ifa_array, this_filename, ['FILE ', this_filename, '\n', this_file_text], ...
            d2s({'CELL_NUM = ' CELL_NUM}));
end
if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This shows example of using pptx_mi function, which gives a
% limited-option but simple access to the pptx writing functions.
% Shows that color images can be used.
    CELL_NUM = 1.1;

    ctr = 0;

    r = 3;
    c = 6;
    ifa_array = [];

    for ctr = 1:(r*c)
        img_num = ctr -1 + randi(1750-r*c);
        img = get_Kay_image('Trn',img_num);
        img = gray_image_to_color(img);
        img(1:100,:,1)=0; %add some color to grayscale image.
        ifa_array(ctr).ifa = pptx_mi( img, [r c ctr], d2sp({'stimTrn ' img_num}), false );
    end


    image_figure_create_PPTX_slide(...
            the_slide, ifa_array, this_filename, ['FILE ', this_filename, '\n', this_file_text], ...
            d2s({'CELL_NUM = ' CELL_NUM}));
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This shows examples of more direct use of the pptx writing functions,
% with direct use of the ifa structure that allows for control of different
% aspects of writing figures, such as varying size, using a circular mask
% or an image mask. See image_figure_arg_struct.m for the full set of
% fields in the ifa structure.

    CELL_NUM = 2;

    ctr = 0;

    ifa_array = [];

    ctr = ctr + 1;
    ifa = image_figure_arg_struct();
    ifa.input_mask_radius = 250;
    ifa.inch_offset = [1 1];
    ifa.title = d2sp({'test ' ctr});
    ifa.input_img = get_Kay_image('Trn',1);
    ifa.include_scalebar = true;
    ifa = image_figure_process( ifa );
    ifa = image_figure_process2( ifa );
    ifa_array(ctr).ifa = ifa;

    ctr = ctr + 1;
    ifa = image_figure_arg_struct();
    ifa.inch_scale = 3;
    ifa.inch_offset = [4 1];
    ifa.title = d2sp({'test ' ctr});
    ifa.input_img = get_Kay_image('Trn',1);
    ifa = image_figure_process( ifa );
    ifa = image_figure_process2( ifa );
    ifa_array(ctr).ifa = ifa;

    ctr = ctr + 1;
    ifa = image_figure_arg_struct();
    ifa.inch_scale = 3;
    ifa.inch_offset = [1 4];
    ifa.title = d2sp({'test ' ctr});
    ifa.input_img = get_Kay_image('Trn',1);
    ifa.input_mask = 0*ifa.input_img;
    ifa.input_mask(find(ifa.input_img<0)) = 1;
    ifa.include_scalebar = true;
    ifa = image_figure_process( ifa );
    ifa = image_figure_process2( ifa );
    ifa_array(ctr).ifa = ifa;

    image_figure_create_PPTX_slide(...
            the_slide, ifa_array, this_filename, ['FILE ', this_filename, '\n', this_file_text], ...
            d2s({'CELL_NUM = ' CELL_NUM}));
end



if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    E = G.constants.KAY_2008;
    V = G.constants.NOV_2013_COMBINED_TRIALS;
    VAL = G.constants.VAL;
    TRN = G.constants.TRN;
    subj = 1;
    load_subject_data_Kay_2008( subj, V );
    S = G.e(E).v(V).s(subj);
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    good = find(S.voxels_with_data_for_all_stimuli>0);
    v3a = find(S.roi==V3a);
    v3b = find(S.roi==V3b);
    v3 = find(S.roi==V3);
    v4 = find(S.roi==V4);
    v1 = find(S.roi==V1);
    v2 = find(S.roi==V2);
    lo = find(S.roi==LO);
    other = find(S.roi==OTHER);
    high_snr = find(S.snr>1.5);
    high_snr = intersect(good, high_snr);
    v3a_high_snr = intersect(v3a,high_snr);
    v3b_high_snr = intersect(v3b,high_snr);
    v3_high_snr = intersect(v3,high_snr);
    v4_high_snr = intersect(v4,high_snr);
    v1_high_snr = intersect(v1,high_snr);
    v2_high_snr = intersect(v2,high_snr);
    lo_high_snr = intersect(lo,high_snr);
    other_high_snr = intersect(other,high_snr);
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    area = v2;
    [~,I] = sort(-S.snr(area));
    for i = 1:length(I)
        j = area(I(i));
        mi(S1_presentation_1and2.rf_stats(j).rf_correlation_image,1);
        title(d2c({i j S.snr(j) S.roi(j)}));
        pause;
    end
end

% 
% if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%     CELL_NUM = 1;
% for i = 1:18%length(I)
%         j = area(I(i));
%         
%     ctr = 0;
% 
%     r = 3;
%     c = 6;
%     ifa_array = [];
% 
%     for ctr = 1:(r*c)
%         img = S1_presentation_1and2.rf_stats(j).rf_correlation_image;
%         ifa_array(ctr).ifa = pptx_mi( img, [r c ctr], d2sp({i j S.snr(j) S.roi(j)}), false );
%     end
% 
% 
%     image_figure_create_PPTX_slide(...
%             the_slide, ifa_array, this_filename, ['FILE ', this_filename, '\n', this_file_text], ...
%             d2s({'CELL_NUM = ' CELL_NUM}));
% end
