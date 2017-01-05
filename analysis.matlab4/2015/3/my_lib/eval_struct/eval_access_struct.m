function vals = eval_access_struct( structure, accessor )
%function vals = eval_access_struct( structure, accessor )
%   e.g., vals = eval_access_struct( REGISTRATION, {'stimTrn',1,'human_face_frontal_3_pts_27Sept2014','registration','moving_points'})
    str = access_struct_str( accessor );
    vals = eval(['structure', str, ';']);
end

