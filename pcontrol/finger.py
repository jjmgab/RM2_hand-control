from pcontrol import pickle_tools as pt
from sympy import Point3D
import os
import os.path as p


class Finger:
    """
        Defines a finger of a prosthetic hand, a manipulator consisting of n joints.
    """

    class Joint():
        def __init__(self, jointcoordinates=None) -> None:
            if jointcoordinates is not None:
                self.coordinates = jointcoordinates

        @property
        def coordinates(self) -> Point3D:
            """
                3Dcoordinations of joint.
            """
            return self.coordinates

        @coordinates.setter
        def coordinates(self, value: Point3D):
            self.joints_coordinations = value

    def __init__(self, number: int, njoints: int, fdir: str):
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

        assert 'V{0}' \
                   .format(self.fNumber) in [x for x in os.listdir(self.directory) if x[0] == 'V'] \
            , "There is no data for base of finger number {0}.".format(self.fNumber)

        self.V = pt.pickle_out('V{0}'.format(self.fNumber), self.directory)
        print("Finger {0}: base coordinates ready".format(self.fNumber))

        # transformation matrices
        self.K = []
        self.K_inv = []
        self.joints = []

        for i in range(0, njoints):
            self.joints.append(self.Joint())
            assert 'K{0}{1}'.format(self.fNumber, i) in [x for x in os.listdir(self.directory) if x[0:2] == 'K{0}'.format(self.fNumber)] \
                , "There is no data for transformation matrix number {0} of finger {1}.".format(i, self.fNumber)
            assert 'K_inv{0}{1}'.format(self.fNumber, i) in [x for x in os.listdir(self.directory) if x[0:2] == 'K_inv{0}'.format(self.fNumber)] \
                , "There is no data for transformation matrix number {0} of finger {1}.".format(i, self.fNumber)

            self.K.append(pt.pickle_out('K{0}{1}'.format(self.fNumber, i), self.directory))
            self.K_inv.append(pt.pickle_out('K_inv{0}{1}'.format(self.fNumber, i), self.directory))

            print("Finger {2}: transformation {0}->{1} and {1}->{0} ready .".format(i, i + 1, self.fNumber))

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

    @property
    def K(self):
        """
            A list of transformations between neighboring joints.
        """
        return self._K

    @K.setter
    def K(self, value):
        self._K = value

    @property
    def K_inv(self):
        """
            A list of inverse transformations between neighboring joints.
        """
        return self._K_inv

    @K_inv.setter
    def K_inv(self, value):
        self._K_inv = value
