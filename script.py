import robotics as robo
import pickle_tools as pt
import sympy as sym
import numbers
import os
import finger as f

import time

"""
	First of all, one should run 'hand_model.py', which defines the model of the hand
	and saves it to files.
"""

if __name__ == '__main__':
	directory = 'pickles'
	fingers = []

	print("Begin script.")

	t_start = time.time()

	for i in range(0,4):
		fingers.append(f.Finger(i, 4, directory))

	t_end = time.time()

	print("End script.")
	print("Time elapsed: {0:.5f} seconds".format(t_end - t_start))

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