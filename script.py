import sympy as sym
import robotics as robo


q1, q2, l1, l2 = sym.symbols("q_1 q_2 l_1 l_2")

A10 = robo.m_transformation(q1,0,l1,0)
A21 = robo.m_transformation(q2,0,l2,0)

# v = robo.m_coord(0,0,0)
# v_f = v * A10 * A21
# v_fs = robo.m_evaluate(v_f, [(q1, 90)])

K = robo.m_process(A10 * A21)

print(sym.latex(K))


# x = Symbol('x')
# f = cos(x) + x**2
# print(f)
# print(latex(Derivative(f,x,1)))