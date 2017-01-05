function d2 = ddir( p )
%function d2 = ddir( p )
%
	if nargin < 1
		p = '.';
	end
	d1 = dir(p);
	ctr = 0;
	for i = 1:length(d1)
		if d1(i).name(1) ~= '.'
			ctr = ctr + 1;
			d2(ctr) = d1(i);
		end
	end
	if not(exist('d2'))
		d2 = [];
	end
end
