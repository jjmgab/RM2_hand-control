import sys
import time
from signal import SIGINT, signal
from typing import IO
import finger_coordinates
import hand_model
from pcontrol import robotics as robo
from pcontrol import pickle_tools as pt
from pcontrol import finger as f
from gnuplot import pyplotter
import sympy as sym
from numpy import pi
import PyGnuplot as gplot

directory = 'pickles'

finger0: IO = None
finger1: IO = None
finger2: IO = None
finger3: IO = None

# ====================================================================
# ====================================================================
# ====================================================================
# ====================================================================
# ====================================================================

parameters = finger_coordinates.initialization()

T10, T11, T12, T13 = sym.symbols("\Theta_{10}, \Theta_{11}, \Theta_{12}, \Theta_{13}")
d1, L0, L1, L2, L3 = sym.symbols("d_1, L_0, L_1, L_2, L_3")
th00, th01, th02, th03 = sym.symbols('\Theta_{00} \Theta_{01} \Theta_{02} \Theta_{03}')
th10, th11, th12, th13 = sym.symbols('\Theta_{10} \Theta_{11} \Theta_{12} \Theta_{13}')
th20, th21, th22, th23 = sym.symbols('\Theta_{20} \Theta_{21} \Theta_{22} \Theta_{23}')
th30, th31, th32, th33 = sym.symbols('\Theta_{30} \Theta_{31} \Theta_{32} \Theta_{33}')

theta0 = [-pi / 16,
          3 * pi / 4,
          0,
          0]

theta1 = [0,
          2 * pi / 5,
          pi / 8,
          pi / 8]

theta2 = [0,
          pi / 4,
          pi / 4,
          0]

theta3 = [0,
          2 * pi / 5,
          pi / 8,
          pi / 8]

vars01 = [(th01, theta0[1]), (th00, -theta0[0])]
vars02 = [(th02, theta0[2])] + vars01
vars03 = [(th03, theta0[3])] + vars02

vars10 = [(th10, theta1[0])]
vars11 = [(th11, theta1[1])] + vars10
vars12 = [(th12, theta1[2])] + vars11
vars13 = [(th13, theta1[3])] + vars12

vars20 = [(th20, theta2[0])]
vars21 = [(th21, theta2[1])] + vars20
vars22 = [(th22, theta2[2])] + vars21
vars23 = [(th23, theta2[3])] + vars22

vars30 = [(th30, theta3[0])]
vars31 = [(th31, theta3[1])] + vars30
vars32 = [(th32, theta3[2])] + vars31
vars33 = [(th33, theta3[3])] + vars32


def finger_number(name):
    assert type(name) == str, "Finger name must be string"
    if name == 'thumb':
        return 0
    elif name == 'first':
        return 1
    elif name == 'second':
        return 2
    elif name == 'third':
        return 3
    else:
        print("Wrong name")


def finger_name(number):
    assert type(number) == int, "Finger number must be int"
    if number == 0:
        return 'thumb'
    elif number == 1:
        return 'first'
    elif number == 2:
        return 'second'
    elif number == 3:
        return 'third'
    else:
        print("Wrong number")


def vars(number):
    if number == 0:
        vars1 = [(th01, theta0[1]), (th00, -theta0[0])]
        vars2 = [(th02, theta0[2])] + vars1
        vars3 = [(th03, theta0[3])] + vars2
        return [vars1, vars2, vars3]

    elif number == 1:
        vars0 = [(th10, theta1[0])]
        vars1 = [(th11, theta1[1])] + vars0
        vars2 = [(th12, theta1[2])] + vars1
        vars3 = [(th13, theta1[3])] + vars2
        return [vars0, vars1, vars2, vars3]
    elif number == 2:
        vars0 = [(th20, theta2[0])]
        vars1 = [(th21, theta2[1])] + vars0
        vars2 = [(th22, theta2[2])] + vars1
        vars3 = [(th23, theta2[3])] + vars2
        return [vars0, vars1, vars2, vars3]
    elif number == 3:
        vars0 = [(th30, theta3[0])]
        vars1 = [(th31, theta3[1])] + vars0
        vars2 = [(th32, theta3[2])] + vars1
        vars3 = [(th33, theta3[3])] + vars2
        return [vars0, vars1, vars2, vars3]


###########################################################################################3
#           INIT

coords0 = [pt.pickle_out("co00", directory), pt.pickle_out("co01", directory),
           pt.pickle_out("co02", directory), pt.pickle_out("co03", directory)]

coords1 = [pt.pickle_out("co10", directory), pt.pickle_out("co11", directory),
           pt.pickle_out("co12", directory), pt.pickle_out("co13", directory)]

coords2 = [pt.pickle_out("co20", directory), pt.pickle_out("co21", directory),
           pt.pickle_out("co22", directory), pt.pickle_out("co23", directory)]

coords3 = [pt.pickle_out("co30", directory), pt.pickle_out("co31", directory),
           pt.pickle_out("co32", directory), pt.pickle_out("co33", directory)]

coords0_eval = [robo.m_process(coords0[0]),
                robo.m_process(robo.m_evaluate(coords0[1], vars01)),
                robo.m_process(robo.m_evaluate(coords0[2], vars02)),
                robo.m_process(robo.m_evaluate(coords0[3], vars03))]

coords1_eval = [robo.m_process(robo.m_evaluate(coords1[0], vars10)),
                robo.m_process(robo.m_evaluate(coords1[1], vars11)),
                robo.m_process(robo.m_evaluate(coords1[2], vars12)),
                robo.m_process(robo.m_evaluate(coords1[3], vars13))]

coords2_eval = [robo.m_process(robo.m_evaluate(coords2[0], vars10)),
                robo.m_process(robo.m_evaluate(coords2[1], vars11)),
                robo.m_process(robo.m_evaluate(coords2[2], vars12)),
                robo.m_process(robo.m_evaluate(coords2[3], vars13))]

coords3_eval = [robo.m_process(robo.m_evaluate(coords3[0], vars10)),
                robo.m_process(robo.m_evaluate(coords3[1], vars11)),
                robo.m_process(robo.m_evaluate(coords3[2], vars12)),
                robo.m_process(robo.m_evaluate(coords3[3], vars13))]


########################################################################################3

def signal_handler(sig, Frame):
    if finger0 is not None:
        finger0.close()
    if finger1 is not None:
        finger0.close()
    if finger2 is not None:
        finger0.close()
    if finger3 is not None:
        finger0.close()
    print("Successfull exit!")
    sys.exit(0)


signal(SIGINT, signal_handler)


def changeCoords(coordinations_eval, coords, confs, numberOfFinger, numberOfJoint=0):
    for jointNumber in range(numberOfJoint, len(coordinations_eval)):
        if numberOfFinger == 0 and jointNumber == 0:
            coordinations_eval[jointNumber] = robo.m_process(confs[jointNumber])
        else:
            coordinations_eval[jointNumber] = robo.m_process(robo.m_evaluate(coords[jointNumber], confs[jointNumber]))
        changeCoords(coordinations_eval, coords, confs, numberOfFinger, numberOfJoint + 1)
        fingers[finger_name(numberOfFinger)].joints[numberOfJoint].coordinates = coordinations_eval[jointNumber]


def apply_changes():
    finger0 = open('data/finger0.dat', 'w')
    finger0.write('{0} {1} {2}\n'.format(coords0_eval[0][0, 0], coords0_eval[0][1, 0], coords0_eval[0][2, 0]))
    finger0.write('{0} {1} {2}\n'.format(coords0_eval[1][0, 0], coords0_eval[1][1, 0], coords0_eval[1][2, 0]))
    finger0.write('{0} {1} {2}\n'.format(coords0_eval[2][0, 0], coords0_eval[2][1, 0], coords0_eval[2][2, 0]))
    finger0.write('{0} {1} {2}\n'.format(coords0_eval[3][0, 0], coords0_eval[3][1, 0], coords0_eval[3][2, 0]))
    finger0.close()

    finger1 = open('data/finger1.dat', 'w')
    finger1.write('{0} {1} {2}\n'.format(coords1_eval[0][0, 0], coords1_eval[0][1, 0], coords1_eval[0][2, 0]))
    finger1.write('{0} {1} {2}\n'.format(coords1_eval[1][0, 0], coords1_eval[1][1, 0], coords1_eval[1][2, 0]))
    finger1.write('{0} {1} {2}\n'.format(coords1_eval[2][0, 0], coords1_eval[2][1, 0], coords1_eval[2][2, 0]))
    finger1.write('{0} {1} {2}\n'.format(coords1_eval[3][0, 0], coords1_eval[3][1, 0], coords1_eval[3][2, 0]))
    finger1.close()

    finger2 = open('data/finger2.dat', 'w')
    finger2.write('{0} {1} {2}\n'.format(coords2_eval[0][0, 0], coords2_eval[0][1, 0], coords2_eval[0][2, 0]))
    finger2.write('{0} {1} {2}\n'.format(coords2_eval[1][0, 0], coords2_eval[1][1, 0], coords2_eval[1][2, 0]))
    finger2.write('{0} {1} {2}\n'.format(coords2_eval[2][0, 0], coords2_eval[2][1, 0], coords2_eval[2][2, 0]))
    finger2.write('{0} {1} {2}\n'.format(coords2_eval[3][0, 0], coords2_eval[3][1, 0], coords2_eval[3][2, 0]))
    finger2.close()

    finger3 = open('data/finger3.dat', 'w')
    finger3.write('{0} {1} {2}\n'.format(coords3_eval[0][0, 0], coords3_eval[0][1, 0], coords3_eval[0][2, 0]))
    finger3.write('{0} {1} {2}\n'.format(coords3_eval[1][0, 0], coords3_eval[1][1, 0], coords3_eval[1][2, 0]))
    finger3.write('{0} {1} {2}\n'.format(coords3_eval[2][0, 0], coords3_eval[2][1, 0], coords3_eval[2][2, 0]))
    finger3.write('{0} {1} {2}\n'.format(coords3_eval[3][0, 0], coords3_eval[3][1, 0], coords3_eval[3][2, 0]))
    finger3.close()


# ====================================================================
# ====================================================================
# ====================================================================
# ====================================================================
# ====================================================================

transformationsAndKinematics = hand_model.initialization()

fingers = {'first': f.Finger(1, 4, directory, verbose=False),
           'second': f.Finger(2, 4, directory, verbose=False),
           'third': f.Finger(3, 4, directory, verbose=False),
           'thumb': f.Finger(0, 4, directory, verbose=False)}

fingers_names = ['first', 'second', 'third', 'thumb']

for name in fingers_names:
    for joint in fingers[name].joints:
        joint.A = transformationsAndKinematics[name]['A']
        joint.K = transformationsAndKinematics[name]['K']


def newCooords(number):
    if number == 0:
        changeCoords(coords0_eval, coords0, [coords0[0]] + vars(0), 0)
    elif number == 1:
        changeCoords(coords1_eval, coords1, vars(1), 1)
    elif number == 2:
        changeCoords(coords2_eval, coords2, vars(2), 2)
    elif number == 3:
        changeCoords(coords3_eval, coords3, vars(3), 3)


def updateConfigs():
    for joint in fingers['first'].joints:
        joint.q = theta1[fingers['first'].joints.index(joint)]
    for joint in fingers['second'].joints:
        joint.q = theta2[fingers['second'].joints.index(joint)]
    for joint in fingers['third'].joints:
        joint.q = theta3[fingers['third'].joints.index(joint)]
    for joint in fingers['thumb'].joints:
        joint.q = theta0[fingers['thumb'].joints.index(joint)]


changeCoords(coords0_eval, coords0, [coords0[0]] + vars(0), 0)
changeCoords(coords1_eval, coords1, vars(1), 1)
changeCoords(coords2_eval, coords2, vars(2), 2)
changeCoords(coords3_eval, coords3, vars(3), 3)
updateConfigs()


class NewtonAlgorithmParameters(object):
    def __init__(self, min_step_size=pi/200, max_step_size=pi/40, epsilon=10, max_iterations=100):
        self.min_step_size = min_step_size
        self.max_step_size = max_step_size
        self.epsilon = epsilon
        self.max_iterations = max_iterations


def inv_kinematics_newton_algorithm(finger: f.Finger, stop_coords,theta , parameters: NewtonAlgorithmParameters):
    """
    Implementation of Newton algorithm for inverse kinematics.

    """
    assert type(stop_coords) == list and len(stop_coords) == len(finger.joints) \
        , 'stop_coords must be list with length equal number of joints in finger'

    errorsForJoints = []
    for jointNr in range(len(finger.joints)):
        x, y, z = sym.symbols('x y z')
        j_x, j_y, j_z = sym.symbols('j_x j_y j_z')
        stop = [(x, stop_coords[jointNr][0]), (y, stop_coords[jointNr][1]), (z, stop_coords[jointNr][2])]
        current = [(j_x, finger.joints[jointNr].coordinates[0]), (j_y, finger.joints[jointNr].coordinates[0]),
                   (j_z, finger.joints[jointNr].coordinates[0])]
        errorsForJoints.append(robo.m_evaluate(robo.m_coord(x, y, z)-robo.m_coord(j_x, j_y, j_z),
                               stop + current).col(3).norm())

    step = [parameters.max_step_size for i in finger.joints]
    done = [False for i in finger.joints]
    iteration = 0

    while False in done and iteration < parameters.max_iterations:
        print("iteracja "+str(iteration))

        for jointNumber in range(len(finger.joints)):
            if True \
                    and iteration < parameters.max_iterations \
                    and errorsForJoints[jointNumber] > parameters.epsilon \
                    and abs(step[jointNumber]) >= parameters.min_step_size:
                theta[jointNr] += step[jointNumber]

                newCooords(finger.fNumber)
                updateConfigs()
                apply_changes()
                pyplotter.replot()

                x, y, z = sym.symbols('x y z')
                j_x, j_y, j_z = sym.symbols('j_x j_y j_z')
                stop = [(x, stop_coords[jointNumber][0]), (y, stop_coords[jointNumber][1]),
                        (z, stop_coords[jointNumber][2])]
                current = [(j_x, finger.joints[jointNumber].coordinates[0]),
                           (j_y, finger.joints[jointNumber].coordinates[0]),
                           (j_z, finger.joints[jointNumber].coordinates[0])]

                newError = robo.m_evaluate(robo.m_coord(x, y, z)-robo.m_coord(j_x, j_y, j_z),
                               stop + current).col(3).norm()
                print("New error " + str(newError) + " old error " + str(errorsForJoints[jointNumber]))

                if newError >= errorsForJoints[jointNumber]:
                    step[jointNumber] = -step[jointNumber] / 4
                elif newError == errorsForJoints[jointNumber]:
                    step[jointNumber] = step[jointNumber] / 4

                errorsForJoints[jointNumber] = newError
                if newError <= parameters.epsilon:
                    done[jointNumber] = True
        iteration += 1
    print(done)

pyplotter.plot('data/')
number = 1
up = True
# while True:
#     newCooords(0)
#     newCooords(1)
#     newCooords(2)
#     newCooords(3)
#
#     updateConfigs()
#     apply_changes()
#     pyplotter.replot()
#
#     theta02 = number * pi / 80
#     theta11 = number * pi / 64
#     theta21 = number * pi / 64
#     theta31 = number * pi / 64
#
#     if up:
#         number += 1
#         if number == 20:
#             up = False
#     else:
#         number -= 1
#         if number == 0:
#             up = True

stop_theta1 = [0,
               3 * pi / 5,
               pi / 4,
               pi / 4]
stop_vars0 = [(th10, stop_theta1[0])]
stop_vars1 = [(th11, stop_theta1[1])] + stop_vars0
stop_vars2 = [(th12, stop_theta1[2])] + stop_vars1
stop_vars3 = [(th13, stop_theta1[3])] + stop_vars2

stop_coords1 = [robo.m_process(robo.m_evaluate(coords1[0], stop_vars0)),
                robo.m_process(robo.m_evaluate(coords1[1], stop_vars1)),
                robo.m_process(robo.m_evaluate(coords1[2], stop_vars2)),
                robo.m_process(robo.m_evaluate(coords1[3], stop_vars3))]
inv_kinematics_newton_algorithm(fingers['first'], stop_coords1, theta1, NewtonAlgorithmParameters())
