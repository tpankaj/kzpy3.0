function G_literature_save
%function G_literature_save
%   1/28/2015
global G

    G_literature_marked = G.literature.marked;
    G_literature_history = G.literature.history;
    
    save('~/Google Drive/analysis.matlab4/2015/2/literature/G_literature_marked.mat','G_literature_marked');
	save('~/Google Drive/analysis.matlab4/2015/2/literature/G_literature_history.mat','G_literature_history');

    %my_save(G.literature.marked, 'G_literature_marked');
    %my_save(G.literature.history, 'G_literature_history');
    
end

