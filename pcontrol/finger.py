from pcontrol import pickle_tools as pt
from sympy import Point3D
import os
import os.path as p


class Finger:
    """
        Defines a finger of a prosthetic hand, a manipulator consisting of n joints.
    """

    class Joint():
        """
            Defines a joint of a finger,
        """
        def __init__(self, jointcoordinates: Point3D, K, K_inv = None) -> None:
            assert jointcoordinates is not None, "Joint coordinates must be a valid Point3D object."
            self.coordinates = jointcoordinates
            self.K = K
            self.K_inv = K_inv

        @property
        def coordinates(self) -> Point3D:
            """
                3Dcoordinations of a joint.
            """
            return self.coordinates

        @coordinates.setter
        def coordinates(self, value: Point3D):
            self.joints_coordinations = value

        @property
        def K(self):
            """
                A transformation related to a joint.
            """
            return self._K

        @K.setter
        def K(self, value):
            self._K = value

        @property
        def K_inv(self):
            """
                A inverse of a transformation related to a joint.
            """
            return self._K_inv

        @K_inv.setter
        def K_inv(self, value):
            self._K_inv = value


    def __init__(self, number: int, njoints: int, fdir: str, verbose=True):
        """
            Class constructor. Unpickles and loads base coordinate matrix and transformation matrices defining corresponding joints.
            :param number: finger number
            :param njoints: number of joints of the manipulator
            :param fdir: directory, where pickled objects are contained
            :type number: int
            :type njoints: int
            :type fdir: str
        """
        assert p.exists(fdir), "An existing directory must be provided."

        self.directory = fdir
        self.fNumber = number

        assert 'V{0}'.format(self.fNumber) in [x for x in os.listdir(self.directory) if x[0] == 'V'], "There is no data for base of finger number {0}.".format(self.fNumber)

        self.V = pt.pickle_out('V{0}'.format(self.fNumber), self.directory)
        
        if verbose:
            print("Finger {0}: base coordinates ready".format(self.fNumber))

        # transformation matrices
        self.joints = []

        for i in range(0, njoints):
            assert 'K{0}{1}'.format(self.fNumber, i) in [x for x in os.listdir(self.directory) if x[0:2] == 'K{0}'.format(self.fNumber)] \
                , "There is no data for transformation matrix number {0} of finger {1}.".format(i, self.fNumber)
            # assert 'K_inv{0}{1}'.format(self.fNumber, i) in [x for x in os.listdir(self.directory) if x[0:6] == 'K_inv{0}'.format(self.fNumber)] \
            #     , "There is no data for inverse transformation matrix number {0} of finger {1}.".format(i, self.fNumber)

            K = pt.pickle_out('K{0}{1}'.format(self.fNumber, i), self.directory)
            # K_inv = pt.pickle_out('K_inv{0}{1}'.format(self.fNumber, i), self.directory)

            self.joints.append(self.Joint(Point3D(), K)) #, K_inv))

            if verbose:
                print("Finger {2}: transformation {0}->{1} and {1}->{0} ready .".format(i, i + 1, self.fNumber))

        if verbose:
            print("Finger {0} ready.".format(self.fNumber))

    @property
    def V(self):
        """
            An SO(4) matrix defining initial manipulator coordinates and orientation.
        """
        return self._V

    @V.setter
    def V(self, value):
        self._V = value
