from kzpy3.utils import *

"""
[integer]-[subimage letter]-[whatever]{optional: __[integer]}.['png' or 'jpg']
"""

path = '/Users/karlzipser/Google_Drive/2015-11/deep net/18Nov2015 LaTex practice 2'

dir_dic,dir_lst=dir_as_dic_and_list(opj(path,'figures'))

figure_dic = {}

for l in dir_lst:
	a = l.split('.')[0].split('-')
	t = l.split('.')[-1]
	print(l.split('.')[0])
	if len(l.split('.')[0].split('__')) > 1:
		print('HERE!!!!!!!')
		w = np.float(l.split('.')[0].split('__')[-1])
	else:
		w = 30
	if t == 'png' or t == 'jpg':
		s = a[1]
		n = int(a[0])
		print((a,n,s,t))
		if n not in figure_dic:
			figure_dic[n] = {}
			figure_dic[n]['subfigures'] = {}
		figure_dic[n]['subfigures'][s] = {}
		figure_dic[n]['subfigures'][s]['filename'] = l
		figure_dic[n]['subfigures'][s]['width'] = np.float(w/100.0)

for l in dir_lst:
	a = l.split('.')
	t = a[-1]
	if t == 'txt':
		n = int(a[0])
		txt = txt_file_to_list_of_strings(opj(path,'figures',l))
		main_txt = []
		for tx in txt:
			txs = tx.split('|')
			print txs
			if len(txs) > 1:
				figure_dic[n]['subfigures'][txs[1]]['txt'] = txs[2]
			else:
				main_txt.append(tx)
		figure_dic[n]['txt'] = main_txt

print(figure_dic)



a = """
\\documentclass[11pt, oneside]{article}   	% use "amsart" instead of "article" for AMSLaTeX format
\\usepackage{geometry}                		% See geometry.pdf to learn the layout options. There are lots.
\\geometry{letterpaper,margin=1.2in}                   		% ... or a4paper or a5paper or ... 
\\usepackage[margin=0.5in]{caption}
%\\geometry{landscape}                		% Activate for rotated page geometry
\\usepackage[parfill]{parskip}    		% Activate to begin paragraphs with an empty line rather than an indent
\\usepackage{graphicx}				% Use pdf, png, jpg, or eps with pdflatex; use eps in DVI mode
\\usepackage[font=normal,skip=6pt]{caption}
\\usepackage{subcaption}
\\graphicspath{ {.}}
								% TeX will automatically convert eps --> pdf in pdflatex		
\\usepackage{amssymb}

%SetFonts
\\renewcommand*\\rmdefault{phv}

%SetFonts
\\title{\\vspace{-2cm}\\textbf{Convolutional Deep Neural Networks -- A Contradiction in Terms, with Important Implications for Contextual Specificity}}

\\author{Karl Zipser et al.}
%\\date{}							% Activate to display a given date or no date

\\begin{document}
\\maketitle

%%%%%%%%%%%%%%%%%%%
%
\\begin{abstract}
\\it
"""
txt = txt_file_to_list_of_strings(opj(path,'text','abstract.txt'))
for t in txt:
	a += t
a = a +"""\\end{abstract}
%
%%%%%%%%%%%%%%%%%%%
"""

sections = ['introduction','methods','results','discussion']

for s in sections:
	a = a + """
%%%%%%%%%%%%%%%%%%%
%
\\section*{"""+s[0].upper()+s[1:]+"""}

"""
	txt = txt_file_to_list_of_strings(opj(path,'text',s+'.txt'))
	for t in txt:
		a += t + "\n"
	a = a + """
%
%%%%%%%%%%%%%%%%%%%
"""

#a=""""""
ns = sorted(figure_dic.keys())
for n in ns:
	caption = ""
	for c in figure_dic[n]['txt']:
		caption += c + "\n"
	a = a + """
%%%%%%%%%%%%%%%%%%%%%%%%%
%
\\begin{figure}[!tbp]"""
	if len(figure_dic[n]['subfigures'].keys()) > 1:
		for s in sorted(figure_dic[n]['subfigures'].keys(),key=natural_keys):
			print(n,s)
			if 'txt' in figure_dic[n]['subfigures'][s]:
				sub_caption = figure_dic[n]['subfigures'][s]['txt']
			else:
				sub_caption = ""
			a = a + """
  \\begin{subfigure}{"""+str(figure_dic[n]['subfigures'][s]['width'])+"""\\textwidth}
    \\includegraphics[width=\\textwidth]{figures/"""+figure_dic[n]['subfigures'][s]['filename']+"""}
    \\caption{"""+sub_caption+"""}
    \\label{fig:"""+str(n)+s+"""}
  \\end{subfigure}"""
	else:
		s = figure_dic[n]['subfigures'].keys()[0]
		a = a + """
    \\includegraphics[width="""+str(figure_dic[n]['subfigures'][s]['width'])+"""\\textwidth]{figures/"""+figure_dic[n]['subfigures'][s]['filename']+"""}"""
  	a = a + """
  \\centering
  \\caption{"""+caption+"""}
  \\label{fig:"""+str(n)+"""}
\end{figure}
%
%%%%%%%%%%%%%%%%%%%%%%%%%
"""

a = a + """
\\end{document} 
"""
#print(a)

list_of_strings_to_txt_file(opj(path,'main.tex'),[a])
#unix(d2s('open',opj(path,'main.tex')))



