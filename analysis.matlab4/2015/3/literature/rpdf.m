function rpdf( i )
%function rpdf( i )
%   read pdf file. i comes from indicies printed by lpdf
global G

    lpdf(true);
    G.literature.current_paper_name = G.literature.d(i).name;
    l = length(G.literature.history);
    G.literature.history(l+1).paper.name = G.literature.current_paper_name;
    G.literature.history(l+1).paper.dir = G.literature.current_dir;
    G.literature.history(l+1).paper.clock = clock;
    system(d2s({'open ' unix_str(G.literature.current_paper_name)}));
    G_literature_save;
end

