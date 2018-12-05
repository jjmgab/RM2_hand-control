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

def initialization():
    directory = 'pickles'
    fingers = []

    print("Begin script.")
    
    t_start = time.time()
    
    for i in range(0, 4):
        fingers.append(f.Finger(i, 4, directory, verbose=False))

    parameters = {}

    # sym.pprint(fingers[1].V)
    # sym.pprint(fingers[1].joints[0].K)
    # sym.pprint(robo.m_eom(fingers[1].V * fingers[1].joints[0].K * fingers[1].joints[1].K))
    """
        THUMB
    """

    b0x, b0y, b0z = sym.symbols('b_{0x} b_{0y} b_{0z}')
    d01, L01, L02, L03, pi = sym.symbols('d_1 L_1 L_2 L_3 \pi')

    inits0 = [(b0x, -11.47), (b0y, 0.0), (b0z, 0.0)]
    consts00 = [(pi, 3.14159)] + inits0
    consts01 = [(L01, 20), (d01, 10)] + consts00
    consts02 = [(L02, 40)] + consts01
    consts03 = [(L03, 15)] + consts02
    parameters['thumb'] = [consts00,consts01,consts02,consts03]

    coords00 = robo.m_eom(robo.m_process(robo.m_evaluate(fingers[0].V * fingers[0].joints[0].K, consts00)))
    coords01 = robo.m_eom(robo.m_process(robo.m_evaluate(fingers[0].V * fingers[0].joints[1].K, consts01)))
    coords02 = robo.m_eom(robo.m_process(robo.m_evaluate(fingers[0].V * fingers[0].joints[2].K, consts02)))
    coords03 = robo.m_eom(robo.m_process(robo.m_evaluate(fingers[0].V * fingers[0].joints[3].K, consts03)))

    pt.pickle_in(coords00, "co00", directory)
    pt.pickle_in(coords01, "co01", directory)
    pt.pickle_in(coords02, "co02", directory)
    pt.pickle_in(coords03, "co03", directory)


    """
        INDEX
    """

    b1x, b1y, b1z = sym.symbols('b_{1x} b_{1y} b_{1z}')
    L10, L11, L12, L13, pi = sym.symbols('L_0 L_1 L_2 L_3 \pi')

    inits1 = [(b1x, 0.0), (b1y, 0.0), (b1z, 0.0)]
    consts10 = [(L10, 25), (pi, 3.14159)] + inits1
    consts11 = [(L11, 45)] + consts10
    consts12 = [(L12, 30)] + consts11
    consts13 = [(L13, 15)] + consts12
    parameters['first'] = [consts10, consts11, consts12, consts13]

    coords10 = robo.m_eom(robo.m_process(robo.m_evaluate(fingers[1].V * fingers[1].joints[0].K, consts10)))
    coords11 = robo.m_eom(robo.m_process(robo.m_evaluate(fingers[1].V * fingers[1].joints[1].K, consts11)))
    coords12 = robo.m_eom(robo.m_process(robo.m_evaluate(fingers[1].V * fingers[1].joints[2].K, consts12)))
    coords13 = robo.m_eom(robo.m_process(robo.m_evaluate(fingers[1].V * fingers[1].joints[3].K, consts13)))

    pt.pickle_in(coords10, "co10", directory)
    pt.pickle_in(coords11, "co11", directory)
    pt.pickle_in(coords12, "co12", directory)
    pt.pickle_in(coords13, "co13", directory)
    # sym.pprint(coords10)


    """
        MIDDLE
    """
    b2x, b2y, b2z = sym.symbols('b_{2x} b_{2y} b_{2z}')
    L20, L21, L22, L23, pi = sym.symbols('L_0 L_1 L_2 L_3 \pi')

    inits2 = [(b2x, 11.0), (b2y, 22.0), (b2z, 0.0)]
    consts20 = [(L20, 25), (pi, 3.14159)] + inits2
    consts21 = [(L21, 45)] + consts20
    consts22 = [(L22, 30)] + consts21
    consts23 = [(L23, 15)] + consts22
    parameters['second'] = [consts20, consts21, consts22, consts23]

    coords20 = robo.m_eom(robo.m_process(robo.m_evaluate(fingers[2].V * fingers[2].joints[0].K, consts20)))
    coords21 = robo.m_eom(robo.m_process(robo.m_evaluate(fingers[2].V * fingers[2].joints[1].K, consts21)))
    coords22 = robo.m_eom(robo.m_process(robo.m_evaluate(fingers[2].V * fingers[2].joints[2].K, consts22)))
    coords23 = robo.m_eom(robo.m_process(robo.m_evaluate(fingers[2].V * fingers[2].joints[3].K, consts23)))

    pt.pickle_in(coords20, "co20", directory)
    pt.pickle_in(coords21, "co21", directory)
    pt.pickle_in(coords22, "co22", directory)
    pt.pickle_in(coords23, "co23", directory)


    """
        RING
    """
    b3x, b3y, b3z = sym.symbols('b_{3x} b_{3y} b_{3z}')
    L30, L31, L32, L33, pi = sym.symbols('L_0 L_1 L_2 L_3 \pi')

    inits3 = [(b3x, 0.0), (b3y, 49.0), (b3z, 0.0)]
    consts30 = [(L30, 25), (pi, 3.14159)] + inits3
    consts31 = [(L31, 45)] + consts30
    consts32 = [(L32, 30)] + consts31
    consts33 = [(L33, 15)] + consts32
    parameters['third'] = [consts30, consts31, consts32, consts33]

    coords30 = robo.m_eom(robo.m_process(robo.m_evaluate(fingers[3].V * fingers[3].joints[0].K, consts30)))
    coords31 = robo.m_eom(robo.m_process(robo.m_evaluate(fingers[3].V * fingers[3].joints[1].K, consts31)))
    coords32 = robo.m_eom(robo.m_process(robo.m_evaluate(fingers[3].V * fingers[3].joints[2].K, consts32)))
    coords33 = robo.m_eom(robo.m_process(robo.m_evaluate(fingers[3].V * fingers[3].joints[3].K, consts33)))

    pt.pickle_in(coords30, "co30", directory)
    pt.pickle_in(coords31, "co31", directory)
    pt.pickle_in(coords32, "co32", directory)
    pt.pickle_in(coords33, "co33", directory)


    ##########################################################################

    t_end = time.time()

    print("End script.")
    print("Time elapsed: {0:.5f} seconds".format(t_end - t_start))
    return parameters

if __name__ == '__main__':
    initialization()
