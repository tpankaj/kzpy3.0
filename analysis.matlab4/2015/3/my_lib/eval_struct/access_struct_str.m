function str = access_struct_str( accessor )
%function str = access_struct_str( structure, accessor )
%   vals = access_struct_str( {'stimTrn',1,'human_face_frontal_3_pts_27Sept2014','registration','moving_points'})
    str = [];
    for i = 1:length(accessor)
        q = accessor{i};
        if isnumeric(q)
            str = d2s({str, '(', q, ')'});
        elseif isstr(q)
            str = d2s({str, '.', q});
        else
            error('what is it?');
        end
    end
end
