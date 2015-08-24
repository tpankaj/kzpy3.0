############################
# - compatibility with Python 3. This stuff from M. Brett's notebooks
# from __future__ import print_function  # print('me') instead of print 'me'
# The above seems to be slow to load, and is necessary to load in this file
# despite the import from kzpy if I want to use printing fully
#from __future__ import division  # 1/2 == 0.5, not 0
############################

from kzpy3 import *

def kzpy_utils_test():
    print('home_path = ' + home_path)
    print('Done.')

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


def d2s_spacer(args,spacer=' '):
    lst = []
    for e in args:
        lst.append(str(e))
    return spacer.join(lst)
def d2s(*args):
    '''
    e.g.,
    
    d2s('I','like',1,'or',[2,3,4])
    
    yields
    
    'I like 1 or [2, 3, 4]'
    
    '''
    return d2s_spacer(args)
def d2c(*args):
    return d2s_spacer(args,spacer=',')
def d2p(*args):
    return d2s_spacer(args,spacer='.')
   

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        
def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
    

def psave(dic,data_path_key,path):
    save_obj(dic[data_path_key],opj(path,data_path_key))
    
def pload(dic,data_path_key,path):
    dic[data_path_key] = load_obj(opj(path,data_path_key))
