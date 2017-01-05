function describe_keys_values( a_map )

    the_keys = a_map.keys;
    disp(the_keys);
    for i = 1:length(the_keys)
        a_key = the_keys{i};
        disp( d2s({i,') ', a_key, '(', length(a_map(a_key)),')'}) );
    end

end