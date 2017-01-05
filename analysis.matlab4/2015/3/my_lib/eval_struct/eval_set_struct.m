function structure = eval_set_struct( structure, accessor, value )
%function structure = eval_set_struct( structure, accessor, value )
    str = ['structure', access_struct_str( accessor ), ' = value;'];
    eval(str);
end

