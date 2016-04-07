# from kzpy3.caf2.state_menu import *
from kzpy3.utils import *



state_names = ['action','capture','deep drive','trim','init','quit']
states = {}

def init_states():
	global states
	for s in state_names:
		states[s] = False

def display_states():
	ctr = 0
	for s in state_names:
		print(d2n(ctr,') ',s,':\t',states[s]))
		ctr += 1




def menu_choice(load=True):
	global states
	if load:
		states = load_obj(opjD('states'))
		print states
	else:
		init_states()
	#while True:#states['quit'] == False:
	display_states()
	i = input(">> ")
	if type(i) in [tuple,list]:
		sn = state_names[i[0]]
		states[sn] = i[1]
	else:
		sn = state_names[i]
		if sn == 'quit':
			return
		states[sn] = not states[sn]
	if states['init']:
		init_states()
	save_obj(states,opjD('states'))

def menu():
	while True:
		menu_choice()

#menu_choice()