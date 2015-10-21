import re

dir_name = re.compile(r'[a-zA-Z0-9_-]+')
path = re.compile(r'[~/]?{dir_name}')
#s = '/subjects/S1_2015/2015/6/20/0/func_runs/pp_b0'
s = '/Users/karlzipser/Research/data/subjects/S1_2015/2015/6/20/0/stats/pp_b0'
sub_ses_re = re.compile(r"""
	/
	(subjects/
		(?P<subject>\w+)/
		(?P<year>[0-9]+)/
		(?P<month>[0-9]+)/
		(?P<day>[0-9]+)/
		(?P<session>[0-9]+)/
		(?P<dtype>stats|func_runs)/
		(?P<pp>pp_[a-z][0-9]+)
		)
""",re.VERBOSE)
result = sub_ses_re.search(s)
print(result.group())
print(result.group('subject'))
print(result.group('year'))
print(result.group('month'))
print(result.group('day'))
print(result.group('session'))
print(result.group('dtype'))
print(result.group('pp'))
'''
p1 = re.compile('\S*subjects')
p2 = re.compile('\S*func_runs')
p3 = re.compile('\S*stats')

def extract_session_from_func_run_path(path_str):
	session_str = path_str[p1.match(path_str).span()[1]+1:]
	session_str = session_str[:(p2.match(session_str).span()[1]-10)]
	return session_str
'''