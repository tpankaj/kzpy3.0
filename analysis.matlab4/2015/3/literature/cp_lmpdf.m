function cp_lmpdf(  )
%function lmpdf(  )
%   list marked pdf files
global G;

    k=G.literature.marked.keys();
    for i=1:length(k)
        system(d2s({'cp ' unix_str(['~/Google Drive/' G.literature.marked(k{i}).dir '/' k{i}]) ' ~/Desktop/temp'}));

    end
end

