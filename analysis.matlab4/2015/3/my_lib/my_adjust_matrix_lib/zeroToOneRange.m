function matrix = zeroToOneRange( matrix )
%function matrix = zeroToOneRange( matrix )
% 19 Nov. 2014
    matrix = single(matrix); % added 24 Oct. 2014
    matrix = matrix - min(min(min(matrix)));
    matrix = matrix / max(max(max(matrix)));
end

