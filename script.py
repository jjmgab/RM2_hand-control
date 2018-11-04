from sympy import *
import mpmath as mp
import robotics as robo

v = robo.matrix_coord(0,0,0)

q1 = Symbol('q_1')
q2 = Symbol('q_2')
q3 = Symbol('q_3')

A1 = robo.transformation(q1,0,0,90)
A2 = robo.transformation(0,q2,0,0)

v_f = v * A1 * A2
v_fs = robo.matrix_evaluate(v_f, [(q1, 90)])

print(latex(v_fs))
