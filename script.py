import robotics as robo
import pickle_tools as pt
import sympy as sym
import numbers

"""
	First of all, one should run 'hand_model.py', which defines the model of the hand
	and saves it to files.
"""

if __name__ == '__main__':
	directory = 'pickles'

	V0 = pt.pickle_out('V0', directory)

	print([x for x in V0.atoms() if isinstance(x, sym.Symbol)])

	print(robo.m_evaluate(V0, [(sym.Symbol('b_{0y}'), 1)]))