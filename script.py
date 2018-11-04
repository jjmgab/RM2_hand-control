from sympy import *
import mpmath as mp
import robotics as robo


q1 = Symbol('q_1')
q2 = Symbol('q_2')
A1 = robo.transformation(q1,0,0,90)
A2 = robo.transformation(0,q2,0,90)

print(latex(A1 * A2))
