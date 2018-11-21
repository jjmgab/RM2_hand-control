from pcontrol import robotics as robo
from pcontrol import pickle_tools as pt
from pcontrol import finger as f
import sympy as sym
import numbers
import os
from sympy import pprint, sin, cos

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
    
    for i in range(0, 4):
        fingers.append(f.Finger(i, 4, directory, verbose=False))
    
    # sym.pprint(fingers[0].joints[0].K)
    eom = robo.m_eom(fingers[0].joints[1].K)
    print(eom.atoms())

    # todo: zamiast listy prefixow podajemy liste symboli, problem z niekwadratowym jakobianem wypada

    jacobian = robo.m_jacobian_from_input(eom, [sym.Symbol('\Theta_{00}'), sym.Symbol('\Theta_{01}'), sym.Symbol('\Theta_{02}'), sym.Symbol('\Theta_{03}')])
    print("wymiary jakobianu:", jacobian.shape)
    print("wiersze jakobianu != 0:", [1 if x != 0 else 0 for x in jacobian])
    # sym.pprint(jacobian)

    t_end = time.time()

    print("End script.")
    print("Time elapsed: {0:.5f} seconds".format(t_end - t_start))
