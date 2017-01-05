function rmpdf( i )
%function rpdf( i )
%   read marked pdf file. i comes from indicies printed by lmpdf
global G
% FIGURE OUT HOW TO GET THIS RIGHT
    G.literature.current_paper_name = G.literature.md{i};
    l = length(G.literature.history);
    G.literature.history(l+1).paper.name = G.literature.current_paper_name;
    G.literature.history(l+1).paper.dir = G.literature.marked(G.literature.current_paper_name).dir;
    G.literature.history(l+1).paper.clock = clock;
    system(d2s({'open ' unix_str(['~/Google Drive/' G.literature.marked(G.literature.current_paper_name).dir '/' G.literature.current_paper_name])}));
    G_literature_save;
end

