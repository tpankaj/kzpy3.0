function matrix = uint8range( matrix )
% function matrix = uint8range( matrix )
% 20 Nov. 2014
    matrix = uint8( 255 * zeroToOneRange( single( matrix ) ) );

end