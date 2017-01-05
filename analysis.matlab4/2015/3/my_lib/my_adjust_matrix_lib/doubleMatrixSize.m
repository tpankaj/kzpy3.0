function B = doubleMatrixSize( A )
%function B = doubleMatrixSize( A )
%   14 Aug. 2014
    B = kron(single(A),ones(2));
end
