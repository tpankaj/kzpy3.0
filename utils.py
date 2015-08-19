############################
# - compatibility with Python 3. This stuff from M. Brett's notebooks
# from __future__ import print_function  # print('me') instead of print 'me'
# The above seems to be slow to load, and is necessary to load in this file
# despite the import from kzpy if I want to use printing fully
#from __future__ import division  # 1/2 == 0.5, not 0
############################ ####iiii

from kzpy3 import *

def kzpy_utils_test():
    print('home_path = ' + home_path)

def zeroToOneRange(m):
    min_n = 1.0*np.min(m)
    return (1.0*m-min_n)/(1.0*np.max(m)-min_n)

z2o = zeroToOneRange

def dir_as_dic_and_list( path ):
    """Returns a dictionary and list of files and directories within the path.

    Keyword argument:
        path

    Certain types are ignored:
        .*      -- I want to avoid hidden files and directories.
        _*      -- I use underscore to indicate things to ignore.
        Icon*   -- The Icon? files are a nuisance created by
                  Google Drive that I also want to ignore."""
    return_dic = {}
    return_list = []
    for filename in os.listdir(path):
        if not filename[0] == '.': # ignore /., /.., and hidden directories and files
            if not filename[0] == '_': # ignore files starting with '_'
                if not filename[0:4] == 'Icon': # ignore Google Drive Icon things
                    return_dic[filename] = {}
                    return_list.append(filename)
    return_list.sort(key=natural_keys)
    return (return_dic,return_list)


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]

def str_contains(str,str_list):
    for s in str_list:
        if not s in str:
            return False
    return True

def str_contains_one(str,str_list):
    for s in str_list:
        if s in str:
            return True
    return False

def select_keys(dic,str_list):
    key_list = []
    for k in dic.keys():
        if str_contains(k,str_list):
            key_list.append(k)
    key_list.sort(key=natural_keys) # if these are not sorted, the keys can be returned in different orders each time. If even and odd are compared, a different result can occur each time.
    return key_list




def unix(command_line_str, print_stdout=True, print_stderr=False):
    command_line_str = command_line_str.replace('~',home_path)
    p = subprocess.Popen(command_line_str.split(), stdout=subprocess.PIPE)
    stdout,stderr = p.communicate()
    if print_stdout:
        print(stdout)
    if print_stderr:
        print(stderr)
    return stdout,stderr


'''
class ProgressBar:

    def __init__(self, iterations):
        self.iterations = iterations
        self.prog_bar = '[]'
        self.fill_char = '*'
        self.width = 50
        self.__update_amount(0)

    def animate(self, iter):
        print('\r', self, end='')
        sys.stdout.flush()
        self.update_iteration(iter + 1)

    def update_iteration(self, elapsed_iter):
        self.__update_amount((elapsed_iter / float(self.iterations)) * 100.0)
        self.prog_bar += '  %d of %s complete' % (elapsed_iter, self.iterations)

    def __update_amount(self, new_amount):
        percent_done = int(round((new_amount / 100.0) * 100.0))
        all_full = self.width - 2
        num_hashes = int(round((percent_done / 100.0) * all_full))
        self.prog_bar = '[' + self.fill_char * num_hashes + ' ' * (all_full - num_hashes) + ']'
        pct_place = (len(self.prog_bar) // 2) - len(str(percent_done))
        pct_string = '%d%%' % percent_done
        self.prog_bar = self.prog_bar[0:pct_place] + \
            (pct_string + self.prog_bar[pct_place + len(pct_string):])

    def __str__(self):
        return str(self.prog_bar)
'''
