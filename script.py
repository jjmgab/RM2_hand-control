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
        fingers.append(f.Finger(i, 4, directory))

    print(fingers[0].K[2])

    theta = sym.symbols("\Theta")
    mat = sym.Matrix([[cos(theta), -sin(theta), 0, 0],
                      [sin(theta), cos(theta), 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])

    transposed = robo.m_transpose(mat)
    inversed = robo.m_inverse_SE3(mat)

    t_end = time.time()

    print("End script.")
    print("Time elapsed: {0:.5f} seconds".format(t_end - t_start))
