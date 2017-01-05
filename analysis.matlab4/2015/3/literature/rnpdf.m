function rpdf( new_name, i )
%function rpdf( i )
%   rename pdf file. i comes from indicies printed by lpdf
global G
	new_name = [new_name '.pdf'];
	new_name = strrep(new_name, '(', '');
	new_name = strrep(new_name, ')', '');
	new_name = strrep(new_name, ':', ' -');
    lpdf(true);
    if nargin > 1
    	G.literature.current_paper_name = G.literature.d(i).name;
    end
    l = length(G.literature.history);
    G.literature.history(l+1).paper.name = G.literature.current_paper_name;
    G.literature.history(l+1).paper.dir = G.literature.current_dir;
    G.literature.history(l+1).paper.clock = clock;

    system_str = d2s({'mv ' unix_str(G.literature.current_paper_name) ' ' unix_str(new_name)});

   % reply = input(['Confirm:' system_str ' [Y]:'],'s');
   % if isempty(reply)
   %    reply = 'Y';
   % end
   % if reply == 'Y'
   	system(system_str)
   % end
   G_literature_save;
   lpdf
end

