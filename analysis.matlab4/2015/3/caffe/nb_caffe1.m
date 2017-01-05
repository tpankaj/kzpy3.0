
if 0
	d=dir('/Volumes/neuro-calhpc.berkeley.edu/imagenet_fall11_whole/*.tar');
end

% a=strrep(d(1).name,'n','')

% b=strrep(a,'.tar','')

% c=str2num(b)
% end
if 0
	for i = 1:152
		mkdir(d2s({'/Volumes/neuro-calhpc.berkeley.edu/imagenet_fall11_whole_unpacked/' i}));
	end
end

if 1
	clear ns;
	emax=0;
	ns = 0*(1:152);
	for i = 1:length(d)
		a=strrep(d(i).name,'n','');
		b=strrep(a,'.tar','');
		c=double(str2num(b));
		e = round(c/100000)+1;
		e
		if e>emax
			emax=e;
		end
		ns(e) = ns(e) + 1;
		system(d2s({''}))
	end
	emax
	plot(ns)
end