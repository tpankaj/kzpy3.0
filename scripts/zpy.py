#! //anaconda/bin/python

from kzpy3.utils import *
from numpy import *


_first = [v for v in globals().keys() if not v.startswith('_')]

if False:
	for f in gg(opjD('temp','*.pkl')):
		vn = f.split('/')[-1].split('.pkl')[0]
		exec( vn + " = load_obj('"+f.strip('.pkl')+"')")



exec(sys.argv[1])

o = sys.argv[1].split('\n')[-1].split(';')[-1]

exec('q = '+o)
print(q)

_second = [v for v in globals().keys() if not v.startswith('_')]

vars = list(set(_second) - set(_first))

if False:
	for v in vars:
		save_obj(globals()[v],opjD('temp',v))

