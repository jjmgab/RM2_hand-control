import sympy as sym
import mpmath as mp

def matrix_coord(x,y,z):
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