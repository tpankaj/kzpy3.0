function lpdf( opt_no_display )
%function lpdf( opt_no_display )
%   list pdf files in current dir.
global G
    if nargin < 1
        opt_no_display = false;
    end
    
    G.literature.d = dir('*.pdf');
    G.literature.current_dir = strrep((pwd),[G.home '/Google Drive/'],'');
    
    if ~opt_no_display
        fps(G.literature.current_dir);
        for i = 1:length(G.literature.d)
            fps(d2s({i ') ' G.literature.d(i).name }));
        end
    end
end