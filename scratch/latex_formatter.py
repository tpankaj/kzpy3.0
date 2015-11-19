from kzpy3.utils import *

"""
[integer]-[subimage letter]-[whatever]{optional: __[integer]}.['png' or 'jpg']
"""

path = '/Users/karlzipser/Google_Drive/2015-11/deep net/18Nov2015 LaTex practice 2'

dir_dic,dir_lst=dir_as_dic_and_list(opj(path,'figures'))

figure_dic = {}

for l in dir_lst:
	a = l.split('.')
	n = int(a[0])
	s = a[1]
	t = a[-1]
	#print((a,n,s,t))
	if t == 'png' or t == 'jpg':
		if n not in figure_dic:
			figure_dic[n] = {}
		figure_dic[n][s] = {}
		figure_dic[n][s]['filename'] = l

for l in dir_lst:
	a = l.split('.')
	n = int(a[0])
	t = a[-1]
	if t == 'txt':
		txt = txt_file_to_list_of_strings(opj(path,'figures',l))
		main_txt = []
		for tx in txt:
			txs = tx.split('|')
			if len(txs) > 1:
				figure_dic[n][txs[1]]['txt'] = txs[2]
			else:
				main_txt.append(tx)
		figure_dic[n]['txt'] = main_txt

print(figure_dic)

a="""
\\begin{figure}[!tbp]
  \\begin{subfigure}{0.15\\textwidth}
    \\includegraphics[width=\\textwidth]{figures/40.a.527.a.png}
    \\caption{This is from face and place}
    \\label{fig:40.a}
  \\end{subfigure}
  \\begin{subfigure}{0.4\\textwidth}
    \\includegraphics[width=\\textwidth]{40.b.527.c3.png}
    \\caption{This is promontory only}
    \\label{fig:40.b}
  \\end{subfigure}
  \\centering
  \\caption{Here are some extra figures.}
\\end{figure}
"""
print(a)
