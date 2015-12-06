c = load_obj('/tmp/zpy_vars/c')
#c = zload('c')
for d in c:
	if len(d)>0:
		unix('say --interactive=/green -r 250 '+d)
		raw_input('...')
############

print opjh()
############

from kzpy3.vis import *
mi(imread(opjh('Pictures/bay2.png')),2)
plt.show()
############

a = 1+1
b = 3
c = a**b
print(c)

############
a = re.split("#+","########### 213 ########")
n = np.int(''.join(a).replace(' ',''))
print(n)
############
import shelve

T='Hiya'
val=[1,2,3]

filename=opjD('shelve.out')
my_shelf = shelve.open(filename,'n') # 'n' for new

for key in dir():
    try:
        my_shelf[key] = globals()[key]
    except TypeError:
        #
        # __builtins__, my_shelf, and imported modules can not be shelved.
        #
        print('ERROR shelving: {0}'.format(key))
my_shelf.close()

############

############

############

