from sympy import *
import mpmath as mp
import robotics as robo

v = robo.matrix_coord(0,0,0)

q1 = Symbol('q_1')
q2 = Symbol('q_2')
A1 = robo.transformation(q1,0,0,90)
A2 = robo.transformation(0,q2,0,90)

print(latex(v*A1))
