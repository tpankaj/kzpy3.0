function lmpdf(  )
%function lmpdf(  )
%   list marked pdf files
global G;
    G.literature.md = {};
    k=G.literature.marked.keys();
    for n=1:length(k)
        G.literature.md{n} = k{n};
        fps(d2s({n ')  ' G.literature.md{n}}));
    end
end

