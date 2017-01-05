function d = chmod_in_depth( the_path )
    fprintf('%s\n',the_path);
    d = dir( the_path );
    
    for i = 1:length(d)
        if not(strcmp(d(i).name,'.'))
            if not(strcmp(d(i).name,'..'))
                
                if d(i).isdir
                    system(['chmod 777 ' unix_str([the_path '/*'])]);
                    %my_pause
                    chmod_in_depth( [the_path '/' d(i).name] );
                end
            end
        end
    end

end