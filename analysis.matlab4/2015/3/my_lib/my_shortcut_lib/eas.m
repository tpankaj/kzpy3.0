function vals = eas( structure, accessor )
%function vals = eas( structure, accessor )
%   e.g., vals = eas( REGISTRATION, {'stimTrn',1,'human_face_frontal_3_pts_27Sept2014','registration','moving_points'})
    vals = eval_access_struct( structure, accessor );
end

