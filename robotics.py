import sympy as sym
import mpmath as mp
import typing
import numbers

# defines a SO(4) matrix defining coordinates in space
def matrix_coord(x,y,z):
	# checks if parameters ar numbers
	assert isinstance(z, numbers.Number) and isinstance(y, numbers.Number) and isinstance(z, numbers.Number), "All parameters should be numbers."
	
	return sym.N(sym.Matrix([
	[ 1,0,0,x ],
	[ 0,1,0,y ],
	[ 0,0,1,z ],
	[ 0,0,0,1,]
	]), 5, chop=True)

# defines a rotation matrix in Denavit-Hartenberg notation
def matrix_rot(axis, variable, use_degrees=True):
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

# defines a translation matrix in Denavit-Hartenberg notation
def matrix_trans(axis, variable, use_degrees=True):
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
	[ 1,0,0,{'x':var}.get(ax, 0) ],
	[ 0,1,0,{'y':var}.get(ax, 0) ],
	[ 0,0,1,{'z':var}.get(ax, 0) ],
	[ 0,0,0,1,]
	]), 5, chop=True)

# defines a Denavit-Hartenberg transformation
def transformation(Rz, Tz, Tx, Rx, use_degrees=True):
	return matrix_rot('z', Rz, use_degrees) * matrix_trans('z', Tz, use_degrees) * matrix_trans('x', Tx, use_degrees) * matrix_rot('x', Rx, use_degrees)

# evaluates the matrix
# to perform multiple substitutions at once, pass a list of (old, new) pairs to subs
def matrix_evaluate(matrix, subs):
	# check if subs is a list of tuples with non-zero length
	assert isinstance(subs, typing.List) and len(subs) > 0 and isinstance(subs[0], typing.Tuple), "'subs' must be a list of tuples with non-zero length."
	# check if one would like to substitute for existing elements
	assert not False in [element[0] in matrix.atoms() for element in subs], "Cannot substitute for elements not present in given expression."
	# check if one would like to evaluate a matrix
	assert issubclass(matrix.__class__, sym.matrices.MatrixBase), "Cannot evaluate non-matrix."

	return sym.N(matrix.subs(subs), 5, chop=True)
