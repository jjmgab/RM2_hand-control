import sympy as sym
import mpmath as mp
import typing
import numbers
from pcontrol import finger
from sympy import Point3D


def m_coord(x, y, z):
    """
    Defines a SO(4) matrix defining coordinates in space.

    :param x: X-coordinate
    :type x: str
    :param y: Y-coordinate
    :type y: str
    :param z: Z-coordinate
    :type z: str
    :return: evaluated matrix
    :rtype: object inheriting from sym.matrices.MatrixBase
    """

    # checks if parameters ar numbers, symbols or expressions
    assert len([t for v in [x, y, z] for t in [numbers.Number, sym.Symbol, sym.Mul] if
                isinstance(v, t)]) == 3, "All parameters should be numbers, symbols or expressions."

    return sym.N(sym.Matrix([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1, ]
    ]), 5, chop=True)


def m_rot(axis, variable, use_degrees=True):
    """
    Defines a rotation matrix in Denavit-Hartenberg notation.

    :param axis: one of Cartesian coordinate system axes (x, y, z)
    :param variable: variable defining rotation
    :param use_degrees: uses degrees if True, uses rads otherwise
    :type axis: char
    :type variable: numbers.Number or sympy.Symbol
    :type use_degrees: bool
    :return: evaluated matrix
    :rtype: object inheriting from sym.matrices.MatrixBase
    """

    # check if axis provided is correct
    ax = axis.lower()
    assert ax in ['x', 'y', 'z'], "Invalid axis provided."

    # checks if variable is a Symbol or a number
    assert len([t for t in [numbers.Number, sym.Symbol, sym.Mul] if
                isinstance(variable, t)]) == 1, "'variable' should be a sympy.Symbol, a number or an expression."

    # convert to degrees if set to true
    if not isinstance(variable, sym.Symbol) and use_degrees:
        var = mp.radians(variable)
    else:
        var = variable

    return sym.N(sym.Matrix([
        [
            {'x': 1}.get(ax, sym.cos(var)),
            {'z': -sym.sin(var)}.get(ax, 0),
            {'y': sym.sin(var)}.get(ax, 0),
            0],
        [
            {'z': sym.sin(var)}.get(ax, 0),
            {'y': 1}.get(ax, sym.cos(var)),
            {'x': -sym.sin(var)}.get(ax, 0),
            0],
        [
            {'y': -sym.sin(var)}.get(ax, 0),
            {'x': sym.sin(var)}.get(ax, 0),
            {'z': 1}.get(ax, sym.cos(var)),
            0],
        [0, 0, 0, 1, ]
    ]), 5, chop=True)


def m_trans(axis, variable):
    """
    Defines a translation matrix in Denavit-Hartenberg notation.

    :param axis: one of Cartesian coordinate system axes (x, y, z)
    :param variable: variable defining translation
    :type axis: char
    :type variable: numbers.Number or sympy.Symbol
    :return: evaluated matrix
    :rtype: object inheriting from sym.matrices.MatrixBase
    """

    # check if axis provided is correct
    ax = axis.lower()
    assert ax in ['x', 'y', 'z'], "Invalid axis provided."

    # checks if variable is a Symbol or a number
    assert len([t for t in [numbers.Number, sym.Symbol, sym.Mul] if
                isinstance(variable, t)]) == 1, "'variable' should be a sympy.Symbol, a number or an expression."

    var = variable

    return sym.N(sym.Matrix([
        [1, 0, 0, {'x': var}.get(ax, 0)],
        [0, 1, 0, {'y': var}.get(ax, 0)],
        [0, 0, 1, {'z': var}.get(ax, 0)],
        [0, 0, 0, 1, ]
    ]), 5, chop=True)


def m_transformation(Rz, Tz, Tx, Rx, use_degrees=True, simplify=True):
    """
    Defines a transformation in Denavit-Hartenberg notation.

    :param Rz: variable used in z-rotation matrix
    :param Tz: variable used in z-translation matrix
    :param Tx: variable used in x-translation matrix
    :param Rx: variable used in x-rotation matrix
    :param use_degrees: uses degrees if True, uses rads otherwise
    :param simplify: simplifies expression if True, does not simplify otherwise
    :type Rz: numbers.Number or sympy.Symbol
    :type Tz: numbers.Number or sympy.Symbol
    :type Tx: numbers.Number or sympy.Symbol
    :type Rx: numbers.Number or sympy.Symbol
    :type use_degrees: bool
    :type simplify: bool
    :return: evaluated matrix
    :rtype: object inheriting from sym.matrices.MatrixBase
    """
    K = m_rot('z', Rz, use_degrees) * m_trans('z', Tz) * m_trans('x', Tx) * m_rot('x', Rx, use_degrees)
    if simplify:
        K = sym.simplify(K)
    return K


def m_eom(matrix):
    """
    Returns equations of motion of an SO(4) matrix in terms of Cartesian coordinate system.

    :param matrix: evaluated matrix
    :type matrix: object inheriting from sym.matrices.MatrixBase
    :return: equations of motion of the matrix
    :rtype: object inheriting from sym.matrices.MatrixBase
    """

    # check if one would like to evaluate a matrix
    assert issubclass(matrix.__class__, sym.matrices.MatrixBase), "Cannot evaluate non-matrix."
    # check if matrix is square and 4x4
    assert (matrix.shape)[0] == 4 and (matrix.shape)[1] == 4, "Matrix must be square and 4x4."

    return matrix.col(-1).row_del(3)


def m_jacobian_from_eom(eom, var_prefix=['']):
    """
    Calculates analytical Jacobian from given equations of motion.

    :param eom: vector of equations of motion
    :param var_prefix: list of prefixes of variables considered as configuration
    :type eom: object inheriting from sym.matrices.MatrixBase
    :type var_prefix: list of one-character strings
    :return: analytical Jacobian
    :rtype:	object inheriting from sym.matrices.MatrixBase
    """

    # check if one would like to evaluate a matrix
    assert issubclass(eom.__class__, sym.matrices.MatrixBase), "Cannot evaluate non-matrix."
    # check if matrix is 1x3 (SymPy Matrix.shape returns a tuple in format (y,x)!)
    assert (eom.shape)[0] == 3 and (eom.shape)[1] == 1, "Matrix must be 1x3."
    # check if subs is a list of tuples with non-zero length
    assert isinstance(var_prefix, typing.List) and len(var_prefix) > 0 and isinstance(var_prefix[0],
                                                                                      str), "'subs' must be a list of strings."
    # check if prefixes are single letters
    for vp in var_prefix:
        assert len(vp) == 0 or (
                len(vp) == 1 and (vp[0]).isalpha()), "'var_prefix' must contain single letters at maximum."

    # gets all sympy.Symbols defined by 'var_prefix' from the matrix
    syms = [elem for elem in eom.atoms() if isinstance(elem, sym.Symbol) and str(elem)[0] in var_prefix]

    # sort in ascending order with respect to index
    sorted(syms, key=lambda elem: str(elem)[2:], reverse=True)

    # calculate partial derivatives
    M = sym.Matrix([[], [], []])
    for symb in syms:
        M = M.col_insert(-1, sym.diff(eom, symb, 1))

    return M


def m_evaluate(matrix, subs):
    """
    Evaluates the matrix over chosen variable(s).

    :param matrix: evaluated matrix
    :param subs: list of symbol-value tuples
    :type matrix: object inheriting from sym.matrices.MatrixBase
    :type subs: list of tuples
    :return: evaluated matrix
    :rtype: object inheriting from sym.matrices.MatrixBase
    """

    # check if subs is a list of tuples with non-zero length
    assert isinstance(subs, typing.List) and len(subs) > 0 and isinstance(subs[0],
                                                                          typing.Tuple), "'subs' must be a list of tuples with non-zero length."
    # check if one would like to substitute for existing elements
    assert not False in [element[0] in matrix.atoms() for element in
                         subs], "Cannot substitute for elements not present in given expression."
    # check if one would like to evaluate a matrix
    assert issubclass(matrix.__class__, sym.matrices.MatrixBase), "Cannot evaluate non-matrix."
    # check if matrix is square and 4x4
    assert (matrix.shape)[0] == 4 and (matrix.shape)[1] == 4, "Matrix must be square and 4x4."

    return sym.N(matrix.subs(subs), 5, chop=True)


def m_process(matrix, simplify=True):
    """
    Processes the matrix.

    :param matrix: processed matrix
    :param simplify: simplifies expression if True, does not simplify otherwise
    :type matrix: object inheriting from sym.matrices.MatrixBase
    :type simplify: bool
    :return: evaluated matrix
    :rtype: object inheriting from sym.matrices.MatrixBase
    """

    # check if one would like to evaluate a matrix
    assert issubclass(matrix.__class__, sym.matrices.MatrixBase), "Cannot evaluate non-matrix."

    M = matrix

    if simplify:
        M = sym.simplify(M)

    return M


def m_transpose(matrix) -> sym.matrices.MatrixBase:
    """
    Returns transpose of matrix.

    :param matrix: processed matrix
    :return: transposed matrix
    """
    # check if one would like to evaluate a matrix
    assert issubclass(matrix.__class__, sym.matrices.MatrixBase), "Cannot evaluate non-matrix."

    return matrix.T


def m_inverse_SE3(matrix) -> sym.matrices.MatrixBase:
    """
    Return inverse matrix of in:matrix in SE(3).

    :param matrix: processed matrix
    :type: matrix: object inheriting from sym.matrices.MatrixBase
    :return: inverse matrix
    :rtype: object inheriting from sym.matrices.MatrixBase
    """
    # check if one would like to evaluate a matrix
    assert issubclass(matrix.__class__, sym.matrices.MatrixBase), "Cannot evaluate non-matrix."

    # check if matrix is square and 4x4
    assert (matrix.shape)[0] == 4 and (matrix.shape)[1] == 4, "Matrix must be square and 4x4."

    assert sym.det(matrix) != 0, "Determinant of matrix cannot be equal to zero"

    return matrix ** -1


class NewtonAlgorithmParameters(object):
    def __init__(self, min_step_size, max_step_size, epsilon, max_iterations):
        self.min_step_size = min_step_size
        self.max_step_size = max_step_size
        self.epsilon = epsilon
        self.max_iterations = max_iterations


def inv_kinematics_newton_algorithm(start_stop, joints_transformations, newton_alg_parameters):
    """
    Implementation of Newton algorithm for inverse kinematics.

    :param start_stop:
    :type: tuple of 2 elements of type sympy.Point3D
    :param transformations:
    :type: list of lists - [[joint],[joint],[joint]]
    :param ssize: size step to algorithm
    :type:
    :param joints: vector of joints that calculation is needed for
    :type:
    :return:
    """

    # check if start_stop is a tuple with length 2
    assert type(start_stop) == tuple and len(start_stop) == 2, "start_stop  have to be tuple with length 2"
    # check if coords are vectors in R^3
    assert isinstance(start_stop[0], Point3D) and isinstance(start_stop[1],
                                                             Point3D), "Coords have to be of type sympy.vector.CoordSys3D"

    trajectory = []
    for transformation in joints_transformations:
        e = start_stop[0].distance(start_stop[1])
        currentPosition = start_stop[0]
        iteration = 0
        step = newton_alg_parameters.max_step_size
        joint_moves = []
        while True \
                and e > newton_alg_parameters.epsilon \
                and iteration < newton_alg_parameters.max_iterations \
                and step >= newton_alg_parameters.min_step_size:

            newStart = Point3D()
            newEpsilon = newStart.distance(start_stop[1])

            if newEpsilon < e:
                e = newEpsilon
                currentPosition = newStart
            else:
                # bisection of step
                step /= 2

            iteration += 1

        trajectory.append(joint_moves)

    return trajectory
