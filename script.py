import robotics as robo
import pickle_tools as pt
import sympy as sym
import numbers
import os
import finger as f

"""
	First of all, one should run 'hand_model.py', which defines the model of the hand
	and saves it to files.
"""

if __name__ == '__main__':
	directory = 'pickles'
	fingers = []

	for i in range(0,4):
		fingers.append(f.Finger(i, directory))

	# list_dir = os.listdir(directory)
	# l_bcoord = [x for x in list_dir if x[0] == 'V']
	# l_transf = [x for x in list_dir if x[0] == 'K']

	# print (l_bcoord)
	# print (l_transf)

	# variables = {}
	# base_coords = {}
	# transformations = {}

	# V0 = pt.pickle_out('V0', directory)

	# for variable in [x for x in V0.atoms() if isinstance(x, sym.Symbol)]:
	# 	print(str(variable))

	# print(robo.m_evaluate(V0, [(sym.Symbol('b_{0y}'), 1)]))