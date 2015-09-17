############################
# - compatibility with Python 3. This stuff from M. Brett's notebooks
from __future__ import print_function  # print('me') instead of print 'me'
from __future__ import division  # 1/2 == 0.5, not 0

# - import common modules
import os
import os.path
import scipy
import scipy.io
import numpy as np  # the Python array package
import string
import glob
import time
import sys
import datetime
import random
import pickle
import re
import subprocess

# - some definitions
home_path = os.path.expanduser("~")
imread = scipy.misc.imread
imsave = scipy.misc.imsave
opj = os.path.join
gg = glob.glob
shape = np.shape
randint = np.random.randint
#random = np.random.random # - this makes a conflict, so don't use it.
randn = np.random.randn
zeros = np.zeros
ones = np.ones
imresize = scipy.misc.imresize
reshape = np.reshape
mod = np.mod


def opjh(*args):
    return opj(home_path,opj(*args))

