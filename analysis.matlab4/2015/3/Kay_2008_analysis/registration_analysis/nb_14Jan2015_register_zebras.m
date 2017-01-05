%%%%%%%%%%% Standard Notebook Beginning %%%%%%%%%%%%
%
clc; fprintf('%s\n',[mfilename ' (' mfilename('fullpath') '.m)']);
this_filename = mfilename('fullpath');
this_file_text = fileread([this_filename,'.m']);
if not(exist('G'))
    error('NOTE: run local_startup.m manually at the beginning of the Matlab session.');
end
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
GRAPHICS = 1;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Description . . .
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    stimSet_str = 'Trn';
    
    set_of_indicies = get_set_of_indicies2_1('~/Desktop/set-animals-textured-bodies-selected/','png')

    Xs = [326.1140  207.8450   97.0614   37.1784  209.3421];
    Ys = [200.3596  200.3596  182.3947  248.2661  345.5760];   
    fixed_points = [Xs ; Ys]';
    
    img_num = 1049;
    img = get_Kay_image( stimSet_str, img_num );    
    [ Xs, Ys ] = mark_image( img, img_num );
    moving_points = [Xs ; Ys]';

    transform = fitgeotrans(moving_points,fixed_points,'Similarity');
	warped_image = imwarp(img,transform,'OutputView',imref2d([512 512]));

    mi(warped_image,2);hold on; plot(fixed_points(:,1),fixed_points(:,2),'o');hold off;
end
