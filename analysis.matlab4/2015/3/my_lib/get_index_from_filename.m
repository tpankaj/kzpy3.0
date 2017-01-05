function index = get_index_from_filename( filename, extension_str )
%function index = get_index_from_mat_filename( filename, extension_str )
%   16 Feb. 2014
    split_str = strsplit( filename, '.' );
    if split_str{length(split_str)} ~= extension_str
        error('expected ', extension_str, ' file');
    end
    index = str2num( split_str{1} );
    if length( index ) < 1
        error('index not a number');
    end
    
end
    
    