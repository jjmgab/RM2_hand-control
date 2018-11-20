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

    # print("Begin script.")
    #
    # t_start = time.time()
    #
    for i in range(0, 4):
        fingers.append(f.Finger(i, 4, directory))

    print(fingers[0].K[2])

    pprint(fingers[0].K_inv[0])
    # t_end = time.time()

    print("End script.")
    # print("Time elapsed: {0:.5f} seconds".format(t_end - t_start))
