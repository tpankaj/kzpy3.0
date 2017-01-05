function mark_pdf( num_or_vec, m )
%function rpdf( i )
%   read pdf file. i comes from indicies printed by lpdf
global G
% G_initalize
% G.literature.history=[]
% G.literature.marked = containers.Map;
    for j = 1:length(num_or_vec)
        i = num_or_vec(j)
        lpdf(true);
        G.literature.current_paper_name = G.literature.d(i).name;
        fps(['marking ' G.literature.current_paper_name]);
        paper.dir = G.literature.current_dir;
        paper.marks = [m];
        paper.clock = clock;
        G.literature.marked(G.literature.current_paper_name) = paper;
        G_literature_save;
    end
end