#! //anaconda/bin/python
# https://pymotw.com/2/argparse/
from kzpy3.utils import *
import argparse

parser = argparse.ArgumentParser(description='krn.py, run specificed cell from scratch_script.py')
parser.add_argument('cell', action="store", type=int, help='cell number')
parser.add_argument('-v', action='store_true', default=False,
    dest='verify',
    help='show cell and verify to run')
parser.add_argument('-s', action='store_true', default=False,
    dest='show_only',
    help='show cell but do not run')

results = parser.parse_args()

zrn(results.cell,results.verify,results.show_only)

