function correlations = get_correlation_matrix( d )
%function correlations = get_correlation_matrix( d )
% correlations = zeros(size_d(1),size_d(1),'single'); ...
% 2 Sept. 2014
    h = waitbar(0,'get_correlation_matrix()');movegui(h,'northeast')
    
    size_d = size(d);
    
    correlations = zeros(size_d(1),size_d(1),'single');
    
    for v1 = 1:size_d(1)
        waitbar(v1/size_d(1));
        for v2 = v1:size_d(1)
            cc = corrcoef(d(v1,:),d(v2,:));
            correlations(v1,v2) = cc(1,2);
            correlations(v2,v1) = cc(1,2);
        end
    end
close(h); end


