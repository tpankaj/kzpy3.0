#! //anaconda/bin/python

from kzpy3.utils import *
from numpy import *

#print sys.argv[1]

exec(sys.argv[1])

o = sys.argv[1].split('\n')[-1].split(';')[-1]
#exec('print('+o+')')
exec('q = '+o)
print(q)