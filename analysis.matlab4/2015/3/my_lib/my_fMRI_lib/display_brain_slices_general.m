function displayMatrix = display_brain_slices_general( experiment, subject, ...
    run_str, voxel_rs, scanner_coordinates_to_voxel_index, FIG_NUM, opt_start_slice, opt_end_slice, opt_rotate_CCW )
%function displayMatrix = display_brain_slices_general( experiment, subject, run_str, voxel_rs, scanner_coordinates_to_voxel_index, FIG_NUM, opt_start_slice, opt_end_slice, opt_rotate_CCW )
% 15 Sept. 2014
% 

    vox_counter = 0;
    imageList = {};
    imgs = 0;
    size_sc = size(scanner_coordinates_to_voxel_index);

    if nargin < 8
        opt_start_slice = 1;
        opt_end_slice = size_sc(3);
        opt_rotate_CCW = 0;
    end
    
    
    strList = {};    

    for z = opt_start_slice:opt_end_slice
        brain_slice = zeros(max(size_sc(2),size_sc(3)),max(size_sc(2),size_sc(3)),'single');

            for x = 1:size_sc(1)
                for y = 1:size_sc(2)
                    v = scanner_coordinates_to_voxel_index(x,y,z);
                    if v > 0
                        brain_slice(x,y) = voxel_rs(v);
                        vox_counter = vox_counter + 1;
                    end
                end
            end
            if opt_rotate_CCW
                brain_slice = rot90(brain_slice, opt_rotate_CCW);
            end
        %brain_slices(z).img = brain_slice;
        imgs = imgs + 1;
        imageList{imgs} = brain_slice;
        strList{imgs} = int2str(z);
    end
%     for i = 1:length(brain_slices)
%         mi(brain_slices(i).img,i+1000);
%     end
%    FIG_NUM
    figure(FIG_NUM);
    set(FIG_NUM,'name',mfilename('fullpath'),'menubar', 'none');
    
    [selected_image_list, Xs, Ys, displayMatrix ] = displayCellArrayOfPicturesAndClick( imageList, strList, 0, FIG_NUM, data2str({data2commaStr({experiment, subject, run_str}),', ' vox_counter,' voxels'}) , 0 );
    
end