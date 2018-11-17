import sympy as sym
import robotics as robo
import pickle_tools as mt

# DEFINITION OF THE HAND

"""
	POSITIONS AND ORIENTATIONS
		described by translation matrix Bi and rotation matrix Ri
"""

if __name__ == '__name__':
	# thumb
	b0x, b0y, b0z = sym.symbols("b_{0x}, b_{0y}, b_{0z}") 
	B0 = robo.m_coord(b0x, b0y, b0z)
	R0 = sym.eye(4)
	V0 = B0 * R0

	# first finger
	b1x, b1y, b1z = sym.symbols("b_{1x}, b_{1y}, b_{1z}") 
	B1 = robo.m_coord(b1x, b1y, b1z)
	R1 = sym.eye(4)
	V1 = B1 * R1

	# second finger
	b2x, b2y, b2z = sym.symbols("b_{2x}, b_{2y}, b_{2z}") 
	B2 = robo.m_coord(b2x, b2y, b2z)
	R2 = sym.eye(4)
	V2 = B2 * R2

	# third finger
	b3x, b3y, b3z = sym.symbols("b_{3x}, b_{3y}, b_{3z}") 
	B3 = robo.m_coord(b3x, b3y, b3z)
	R3 = sym.eye(4)
	V3 = B3 * R3

	"""
		TRANSFORMATIONS
			each joint is described by transformation matrix Aijk
			final transformation is described by the matrix Ki
	"""
	d1, L0, L1, L2, L3 = sym.symbols("d_1, L_0, L_1, L_2, L_3")

	# thumb
	T00, T01, T02, T03 = sym.symbols("\Theta_{00}, \Theta_{01}, \Theta_{02}, \Theta_{03}")
	A010 = robo.m_transformation(T00,  0,  0,  sym.pi/4)
	A021 = robo.m_transformation(T01, -d1, L1, sym.pi/2)
	A032 = robo.m_transformation(T02,  0,  L2, 0)
	A043 = robo.m_transformation(T03,  0,  L3, 0)
	K0 = robo.m_process(A010 * A021 * A032 * A043)

	# first finger
	T10, T11, T12, T13 = sym.symbols("\Theta_{10}, \Theta_{11}, \Theta_{12}, \Theta_{13}")
	A110 = robo.m_transformation(T10, 0, L0, sym.pi/2)
	A121 = robo.m_transformation(T11, 0, L1, 0)
	A132 = robo.m_transformation(T12, 0, L2, 0)
	A143 = robo.m_transformation(T13, 0, L3, 0)
	K1 = robo.m_process(A110 * A121 * A132 * A143)

	# second finger
	T20, T21, T22, T23 = sym.symbols("\Theta_{20}, \Theta_{21}, \Theta_{22}, \Theta_{23}")
	A210 = robo.m_transformation(T20, 0, L0, sym.pi/2)
	A221 = robo.m_transformation(T21, 0, L1, 0)
	A232 = robo.m_transformation(T22, 0, L2, 0)
	A243 = robo.m_transformation(T23, 0, L3, 0)
	K2 = robo.m_process(A210 * A221 * A232 * A243)

	# third finger
	T30, T31, T32, T33 = sym.symbols("\Theta_{30}, \Theta_{31}, \Theta_{32}, \Theta_{33}")
	A310 = robo.m_transformation(T30, 0, L0, sym.pi/2)
	A321 = robo.m_transformation(T31, 0, L1, 0)
	A332 = robo.m_transformation(T32, 0, L2, 0)
	A343 = robo.m_transformation(T33, 0, L3, 0)
	K3 = robo.m_process(A310 * A321 * A332 * A343)


"""
	Now we've got position-orientation matrices Vi, describing the base of each finger,
	as well as matrices Aijk, describing transformation at each joint, and Ki, defining total transformation.

	At this point a complete basic model of the hand is complete (constraints are yet to be defined).
"""