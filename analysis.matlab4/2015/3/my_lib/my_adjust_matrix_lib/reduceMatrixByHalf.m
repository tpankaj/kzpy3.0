function B = reduceMatrixByHalf( A )
%function B = reduceMatrixByHalf( A )
%   19 Nov. 2014
    i = 1:2:size(A,1)-1;
    j = 1:2:size(A,2)-1;

    B = 0.25 * (A(i,j) + A(i+1,j) + A(i,j+1) + A(i+1,j+1));
end

