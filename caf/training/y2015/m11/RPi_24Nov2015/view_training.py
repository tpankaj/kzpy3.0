
from kzpy3.vis import *
CS_('''
*** 
''')

ns = txt_file_to_list_of_strings(opjD('train_log.txt'))
st = 'Train net output #90: loss = '
train_loss = []
for n in ns:
    if st in n:
        train_loss.append(float(n.split(st)[1].split()[0]))
        
plot(train_loss[1:],'.-');


