import sympy as sym
import mpmath as mp
import typing
import numbers


"""
	Defines a SO(4) matrix defining coordinates in space.
	
		:param x: X-coordinate
		:param y: Y-coordinate
		:param z: Z-coordinate
		:return: evaluated matrix
		:rtype: object inheriting from sym.matrices.MatrixBase
"""
def m_coord(x,y,z):
	# checks if parameters ar numbers
	assert isinstance(z, numbers.Number) and isinstance(y, numbers.Number) and isinstance(z, numbers.Number), "All parameters should be numbers."
	
	return sym.N(sym.Matrix([
	[ 1,0,0,x ],
	[ 0,1,0,y ],
	[ 0,0,1,z ],
	[ 0,0,0,1,]
	]), 5, chop=True)


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
def m_rot(axis, variable, use_degrees=True):
	# check if axis provided is correct
	ax = axis.lower()
	assert ax in ['x','y','z'], "Invalid axis provided."

	# checks if variable is a Symbol or a number
	assert isinstance(variable, sym.Symbol) or isinstance(variable, numbers.Number), "'variable' should be a sympy.Symbol or a number."

	# convert to degrees if set to true
	if not isinstance(variable, sym.Symbol) and use_degrees:
		var = mp.radians(variable)
	else:
		var = variable

	return sym.N(sym.Matrix([
	[
	{'x': 1       }.get(ax, sym.cos(var)),
	{'z':-sym.sin(var)}.get(ax, 0),
	{'y': sym.sin(var)}.get(ax, 0),
	0],
	[
	{'z': sym.sin(var)}.get(ax, 0),
	{'y': 1       }.get(ax, sym.cos(var)),
	{'x':-sym.sin(var)}.get(ax, 0),
	0],
	[
	{'y':-sym.sin(var)}.get(ax, 0),
	{'x': sym.sin(var)}.get(ax, 0),
	{'z': 1       }.get(ax, sym.cos(var)),
	0],
	[0,0,0,1,]
	]), 5, chop=True)


"""
	Defines a translation matrix in Denavit-Hartenberg notation.

		:param axis: one of Cartesian coordinate system axes (x, y, z)
		:param variable: variable defining translation
		:type axis: char
		:type variable: numbers.Number or sympy.Symbol
		:return: evaluated matrix
		:rtype: object inheriting from sym.matrices.MatrixBase
"""
def m_trans(axis, variable):
	# check if axis provided is correct
	ax = axis.lower()
	assert ax in ['x','y','z'], "Invalid axis provided."

	# checks if variable is a Symbol or a number
	assert isinstance(variable, sym.Symbol) or isinstance(variable, numbers.Number), "'variable' should be a sympy.Symbol or a number."

	var = variable

	return sym.N(sym.Matrix([
	[ 1,0,0,{'x':var}.get(ax, 0) ],
	[ 0,1,0,{'y':var}.get(ax, 0) ],
	[ 0,0,1,{'z':var}.get(ax, 0) ],
	[ 0,0,0,1,]
	]), 5, chop=True)


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
def m_transformation(Rz, Tz, Tx, Rx, use_degrees=True, simplify=True):
	K = m_rot('z', Rz, use_degrees) * m_trans('z', Tz, use_degrees) * m_trans('x', Tx, use_degrees) * m_rot('x', Rx, use_degrees)
	if simplify:
		K = sym.simplify(K)
	return K


"""
	Evaluates the matrix over chosen variable(s).
	
	:param matrix: evaluated matrix
	:param subs: list of symbol-value tuples
	:type matrix: object inheriting from sym.matrices.MatrixBase
	:type subs: list of tuples
	:return: evaluated matrix
	:rtype: object inheriting from sym.matrices.MatrixBase
"""
def m_evaluate(matrix, subs):
	# check if subs is a list of tuples with non-zero length
	assert isinstance(subs, typing.List) and len(subs) > 0 and isinstance(subs[0], typing.Tuple), "'subs' must be a list of tuples with non-zero length."
	# check if one would like to substitute for existing elements
	assert not False in [element[0] in matrix.atoms() for element in subs], "Cannot substitute for elements not present in given expression."
	# check if one would like to evaluate a matrix
	assert issubclass(matrix.__class__, sym.matrices.MatrixBase), "Cannot evaluate non-matrix."

	return sym.N(matrix.subs(subs), 5, chop=True)


"""
	Processes the matrix.
	
	:param matrix: processed matrix
	:param simplify: simplifies expression if True, does not simplify otherwise
	:type matrix: object inheriting from sym.matrices.MatrixBase
	:type simplify: bool
	:return: evaluated matrix
	:rtype: object inheriting from sym.matrices.MatrixBase
"""
def m_process(matrix, simplify=True):
	# check if one would like to evaluate a matrix
	assert issubclass(matrix.__class__, sym.matrices.MatrixBase), "Cannot evaluate non-matrix."

	M = matrix

	if simplify:
		M = sym.simplify(M)
	
	return M
