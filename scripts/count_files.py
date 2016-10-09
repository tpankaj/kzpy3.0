#!/usr/bin/python
import os
import glob
cwd = os.getcwd()
#os.chdir(home_path)
#from kzpy3.utils import *

print len(glob.glob(os.path.join(cwd,'*')))#s    )),'files')
