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

    print("Begin script.")
    pi = 3.14159
    t_start = time.time()
    
    theta00 = -pi/16
    theta01 = 3*pi/4
    theta02 = 0
    theta03 = 0

    theta10 = 0
    theta11 = 2*pi/5
    theta12 = pi/8
    theta13 = pi/2

    theta20 = 0
    theta21 = 0
    theta22 = 0
    theta23 = 0

    theta30 = 0
    theta31 = 2*pi/5
    theta32 = pi/8
    theta33 = pi/2

    ######################################

    coords00 = pt.pickle_out("co00", directory)
    coords01 = pt.pickle_out("co01", directory)
    coords02 = pt.pickle_out("co02", directory)
    coords03 = pt.pickle_out("co03", directory)

    coords10 = pt.pickle_out("co10", directory)
    coords11 = pt.pickle_out("co11", directory)
    coords12 = pt.pickle_out("co12", directory)
    coords13 = pt.pickle_out("co13", directory)

    coords20 = pt.pickle_out("co20", directory)
    coords21 = pt.pickle_out("co21", directory)
    coords22 = pt.pickle_out("co22", directory)
    coords23 = pt.pickle_out("co23", directory)

    coords30 = pt.pickle_out("co30", directory)
    coords31 = pt.pickle_out("co31", directory)
    coords32 = pt.pickle_out("co32", directory)
    coords33 = pt.pickle_out("co33", directory)

    ######################################
    
    th00, th01, th02, th03 = sym.symbols('\Theta_{00} \Theta_{01} \Theta_{02} \Theta_{03}')
    th10, th11, th12, th13 = sym.symbols('\Theta_{10} \Theta_{11} \Theta_{12} \Theta_{13}')
    th20, th21, th22, th23 = sym.symbols('\Theta_{20} \Theta_{21} \Theta_{22} \Theta_{23}')
    th30, th31, th32, th33 = sym.symbols('\Theta_{30} \Theta_{31} \Theta_{32} \Theta_{33}')

    ######################################

    vars01 = [(th01, theta01), (th00, -theta00)]
    vars02 = [(th02, theta02)] + vars01
    vars03 = [(th03, theta03)] + vars02

    vars10 = [(th10, theta10)]
    vars11 = [(th11, theta11)] + vars10
    vars12 = [(th12, theta12)] + vars11
    vars13 = [(th13, theta13)] + vars12

    vars20 = [(th20, theta20)]
    vars21 = [(th21, theta21)] + vars20
    vars22 = [(th22, theta22)] + vars21
    vars23 = [(th23, theta23)] + vars22

    vars30 = [(th30, theta30)]
    vars31 = [(th31, theta31)] + vars30
    vars32 = [(th32, theta32)] + vars31
    vars33 = [(th33, theta33)] + vars32

    ######################################

    coords00_eval = robo.m_process(coords00)
    coords01_eval = robo.m_process(robo.m_evaluate(coords01, vars01))
    coords02_eval = robo.m_process(robo.m_evaluate(coords02, vars02))
    coords03_eval = robo.m_process(robo.m_evaluate(coords03, vars03))

    coords10_eval = robo.m_process(robo.m_evaluate(coords10, vars10))
    coords11_eval = robo.m_process(robo.m_evaluate(coords11, vars11))
    coords12_eval = robo.m_process(robo.m_evaluate(coords12, vars12))
    coords13_eval = robo.m_process(robo.m_evaluate(coords13, vars13))
    print('---')
    sym.pprint(coords11[2,0])

    coords20_eval = robo.m_process(robo.m_evaluate(coords20, vars20))
    coords21_eval = robo.m_process(robo.m_evaluate(coords21, vars21))
    coords22_eval = robo.m_process(robo.m_evaluate(coords22, vars22))
    coords23_eval = robo.m_process(robo.m_evaluate(coords23, vars23))

    coords30_eval = robo.m_process(robo.m_evaluate(coords30, vars30))
    coords31_eval = robo.m_process(robo.m_evaluate(coords31, vars31))
    coords32_eval = robo.m_process(robo.m_evaluate(coords32, vars32))
    coords33_eval = robo.m_process(robo.m_evaluate(coords33, vars33))

    ######################################

    finger0 = open('data/finger0.dat', 'w')
    finger0.write('{0} {1} {2}\n'.format(coords00_eval[0,0], coords00_eval[1,0], coords00_eval[2,0]))
    finger0.write('{0} {1} {2}\n'.format(coords01_eval[0,0], coords01_eval[1,0], coords01_eval[2,0]))
    finger0.write('{0} {1} {2}\n'.format(coords02_eval[0,0], coords02_eval[1,0], coords02_eval[2,0]))
    finger0.write('{0} {1} {2}\n'.format(coords03_eval[0,0], coords03_eval[1,0], coords03_eval[2,0]))
    finger0.close()

    finger1 = open('data/finger1.dat', 'w')
    finger1.write('{0} {1} {2}\n'.format(coords10_eval[0,0], coords10_eval[1,0], coords10_eval[2,0]))
    finger1.write('{0} {1} {2}\n'.format(coords11_eval[0,0], coords11_eval[1,0], coords11_eval[2,0]))
    finger1.write('{0} {1} {2}\n'.format(coords12_eval[0,0], coords12_eval[1,0], coords12_eval[2,0]))
    finger1.write('{0} {1} {2}\n'.format(coords13_eval[0,0], coords13_eval[1,0], coords13_eval[2,0]))
    finger1.close()

    finger2 = open('data/finger2.dat', 'w')
    finger2.write('{0} {1} {2}\n'.format(coords20_eval[0,0], coords20_eval[1,0], coords20_eval[2,0]))
    finger2.write('{0} {1} {2}\n'.format(coords21_eval[0,0], coords21_eval[1,0], coords21_eval[2,0]))
    finger2.write('{0} {1} {2}\n'.format(coords22_eval[0,0], coords22_eval[1,0], coords22_eval[2,0]))
    finger2.write('{0} {1} {2}\n'.format(coords23_eval[0,0], coords23_eval[1,0], coords23_eval[2,0]))
    finger2.close()

    finger3 = open('data/finger3.dat', 'w')
    finger3.write('{0} {1} {2}\n'.format(coords30_eval[0,0], coords30_eval[1,0], coords30_eval[2,0]))
    finger3.write('{0} {1} {2}\n'.format(coords31_eval[0,0], coords31_eval[1,0], coords31_eval[2,0]))
    finger3.write('{0} {1} {2}\n'.format(coords32_eval[0,0], coords32_eval[1,0], coords32_eval[2,0]))
    finger3.write('{0} {1} {2}\n'.format(coords33_eval[0,0], coords33_eval[1,0], coords33_eval[2,0]))
    finger3.close()

    base = open('data/base.dat', 'w')
    base.write('{0} {1} {2}\n'.format(coords00_eval[0,0], coords00_eval[1,0], coords00_eval[2,0]))
    base.write('{0} {1} {2}\n'.format(coords10_eval[0,0], coords10_eval[1,0], coords10_eval[2,0]))
    base.write('{0} {1} {2}\n'.format(coords20_eval[0,0], coords20_eval[1,0], coords20_eval[2,0]))
    base.write('{0} {1} {2}\n'.format(coords30_eval[0,0], coords30_eval[1,0], coords30_eval[2,0]))
    base.write('{0} {1} {2}\n'.format(coords00_eval[0,0], coords30_eval[1,0], coords00_eval[2,0]))
    base.write('{0} {1} {2}\n'.format(coords00_eval[0,0], coords00_eval[1,0], coords00_eval[2,0]))
    base.close()

    ##########################################################################

    t_end = time.time()

    print("End script.")
    print("Time elapsed: {0:.5f} seconds".format(t_end - t_start))
