from kzpy3.vis import *
a=np.random.randn(10000)
hist(a,100)
plt.show()
############
import objc
import applescript
a = """if application "Google Chrome" is running then
        tell application "Google Chrome" to make new window with properties {mode:"incognito"}
    else
        do shell script "open -a /Applications/Google\\\ Chrome.app --args --incognito"
    end if

    tell application "Google Chrome" to activate
    open location "http://nytimes.com" """
applescript.AppleScript(a).run()

############
def say(t):
    unix('say '+t)
#############
def getClipboardData():
 p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
 retcode = p.wait()
 data = p.stdout.read()
 return data

def setClipboardData(data):
 p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
 p.stdin.write(data)
 p.stdin.close()
 retcode = p.wait()
############
c = load_obj('/tmp/zpy_vars/c')
#c = zload('c')
for d in c:
	if len(d)>0:
		unix('say --interactive=/green -r 200 '+d)
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

