from kzpy3.utils import *

state_names = ['capture','deep drive','trim','quit']
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


init_states()

def menu_choice():
	global states
	while states['quit'] == False:
		display_states()
		i = input(">> ")
		if type(i) in [tuple,list]:
			sn = state_names[i[0]]
			states[sn] = i[1]
		else:
			sn = state_names[i]
			states[sn] = not states[sn]

menu_choice()