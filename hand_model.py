from pcontrol import robotics as robo
from pcontrol import pickle_tools as pt
import sympy as sym
import shutil
import os
import os.path as p
import time

# DEFINITION OF THE HAND



def initialization():
	"""
	Carries out all required calculations in order to create assumed model of a hand prosthetic. 
	Matrices are then pickled up into binary files and saved in the *pickles* directory.
	"""
	print("Begin script.")
    
	t_start = time.time()
	print("Running hand model initialization. . . ")

	dirname = "pickles"
	if p.exists(dirname):
		shutil.rmtree(dirname)
	os.mkdir(dirname)

	"""
	POSITIONS AND ORIENTATIONS
		described by translation matrix Bi and rotation matrix Ri
	"""

	# thumb
	b0x, b0y, b0z = sym.symbols("b_{0x}, b_{0y}, b_{0z}") 
	B0 = robo.m_coord(b0x, b0y, b0z)
	R0 = sym.Matrix([[0,0,1,0],[0,-1,0,0],[-1,0,0,0],[0,0,0,1]]) #robo.m_transformation(0,0,-15,-90) * robo.m_transformation(90, 0, 0, 90)
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

	pt.pickle_in(V0, "V0", dirname)
	pt.pickle_in(V1, "V1", dirname)
	pt.pickle_in(V2, "V2", dirname)
	pt.pickle_in(V3, "V3", dirname)

	"""
		TRANSFORMATIONS
			each joint is described by transformation matrix Aijk
			final transformation is described by the matrix Ki
	"""
	d1, L0, L1, L2, L3 = sym.symbols("d_1, L_0, L_1, L_2, L_3")
	PI = 3.14159

	# thumb
	print('thumb...')
	T00, T01, T02, T03 = sym.symbols("\Theta_{00}, \Theta_{01}, \Theta_{02}, \Theta_{03}")
	A010 = robo.m_transformation(T00,  0,  0,  PI/4, use_degrees=False)
	A021 = robo.m_transformation(T01, -d1, L1, PI/2, use_degrees=False)
	A032 = robo.m_transformation(T02,  0,  L2, 0)
	A043 = robo.m_transformation(T03,  0,  L3, 0)
	K00 = robo.m_process(A010)
	K01 = robo.m_process(K00 * A021)
	K02 = robo.m_process(K01 * A032)
	K03 = robo.m_process(K02 * A043)
	# K_inv00 = robo.m_inverse_SE3(K00)
	# K_inv01 = robo.m_inverse_SE3(K01)
	# K_inv02 = robo.m_inverse_SE3(K02)
	# K_inv03 = robo.m_inverse_SE3(K03)

	print('first...')
	# first finger
	T10, T11, T12, T13 = sym.symbols("\Theta_{10}, \Theta_{11}, \Theta_{12}, \Theta_{13}")
	A110 = robo.m_transformation(T10, 0, L0, PI/2, use_degrees=False)
	A121 = robo.m_transformation(T11, 0, L1, 0)
	A132 = robo.m_transformation(T12, 0, L2, 0)
	A143 = robo.m_transformation(T13, 0, L3, 0)
	K10 = robo.m_process(A110)
	K11 = robo.m_process(K10 * A121)
	K12 = robo.m_process(K11 * A132)
	K13 = robo.m_process(K12 * A143)
	# K_inv10 = robo.m_inverse_SE3(K10)
	# K_inv11 = robo.m_inverse_SE3(K11)
	# K_inv12 = robo.m_inverse_SE3(K12)
	# K_inv13 = robo.m_inverse_SE3(K13)

	print('second...')
	# second finger
	T20, T21, T22, T23 = sym.symbols("\Theta_{20}, \Theta_{21}, \Theta_{22}, \Theta_{23}")
	A210 = robo.m_transformation(T20, 0, L0, PI/2, use_degrees=False)
	A221 = robo.m_transformation(T21, 0, L1, 0)
	A232 = robo.m_transformation(T22, 0, L2, 0)
	A243 = robo.m_transformation(T23, 0, L3, 0)
	K20 = robo.m_process(A210)
	K21 = robo.m_process(K20 * A221)
	K22 = robo.m_process(K21 * A232)
	K23 = robo.m_process(K22 * A243)
	# K_inv20 = robo.m_inverse_SE3(K20)
	# K_inv21 = robo.m_inverse_SE3(K21)
	# K_inv22 = robo.m_inverse_SE3(K22)
	# K_inv23 = robo.m_inverse_SE3(K23)

	print('third...')
	# third finger
	T30, T31, T32, T33 = sym.symbols("\Theta_{30}, \Theta_{31}, \Theta_{32}, \Theta_{33}")
	A310 = robo.m_transformation(T30, 0, L0, PI/2, use_degrees=False)
	A321 = robo.m_transformation(T31, 0, L1, 0)
	A332 = robo.m_transformation(T32, 0, L2, 0)
	A343 = robo.m_transformation(T33, 0, L3, 0)
	K30 = robo.m_process(A310)
	K31 = robo.m_process(K30 * A321)
	K32 = robo.m_process(K31 * A332)
	K33 = robo.m_process(K32 * A343)
	# K_inv30 = robo.m_inverse_SE3(K30)
	# K_inv31 = robo.m_inverse_SE3(K31)
	# K_inv32 = robo.m_inverse_SE3(K32)
	# K_inv33 = robo.m_inverse_SE3(K33)

	print('pickleizing...')
	# pickleize all transformation matrices
	pt.pickle_in(K00, "K00", dirname)
	pt.pickle_in(K01, "K01", dirname)
	pt.pickle_in(K02, "K02", dirname)
	pt.pickle_in(K03, "K03", dirname)
	# pt.pickle_in(K_inv00, "K_inv00", dirname)
	# pt.pickle_in(K_inv01, "K_inv01", dirname)
	# pt.pickle_in(K_inv02, "K_inv02", dirname)
	# pt.pickle_in(K_inv03, "K_inv03", dirname)

	pt.pickle_in(K10, "K10", dirname)
	pt.pickle_in(K11, "K11", dirname)
	pt.pickle_in(K12, "K12", dirname)
	pt.pickle_in(K13, "K13", dirname)

	# pt.pickle_in(K_inv10, "K_inv10", dirname)
	# pt.pickle_in(K_inv11, "K_inv11", dirname)
	# pt.pickle_in(K_inv12, "K_inv12", dirname)
	# pt.pickle_in(K_inv13, "K_inv13", dirname)

	pt.pickle_in(K20, "K20", dirname)
	pt.pickle_in(K21, "K21", dirname)
	pt.pickle_in(K22, "K22", dirname)
	pt.pickle_in(K23, "K23", dirname)

	# pt.pickle_in(K_inv20, "K_inv20", dirname)
	# pt.pickle_in(K_inv21, "K_inv21", dirname)
	# pt.pickle_in(K_inv22, "K_inv22", dirname)
	# pt.pickle_in(K_inv23, "K_inv23", dirname)

	pt.pickle_in(K30, "K30", dirname)
	pt.pickle_in(K31, "K31", dirname)
	pt.pickle_in(K32, "K32", dirname)
	pt.pickle_in(K33, "K33", dirname)

	# pt.pickle_in(K_inv30, "K_inv30", dirname)
	# pt.pickle_in(K_inv31, "K_inv31", dirname)
	# pt.pickle_in(K_inv32, "K_inv32", dirname)
	# pt.pickle_in(K_inv33, "K_inv33", dirname)

	print("done!")
	t_end = time.time()

	print("End script.")
	print("Time elapsed: {0:.5f} seconds".format(t_end - t_start))

if __name__ == '__main__':
	initialization()
"""
	Now we've got position-orientation matrices Vi, describing the base of each finger,
	as well as matrices Aijk, describing transformation at each joint, and Ki, defining total transformation.

	At this point a complete basic model of the hand is complete (constraints are yet to be defined).
"""