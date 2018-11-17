import pickle
import os.path as p

"""

	Unfortunately marshal module apparently does not support 
	fancy modules such as SymPy.

"""

"""
	Saves object to binary file.

	:param obj: object to dump
	:param name: filename
	:type obj: any
	:type name: string
"""
def pickle_in(obj, name: str, dirname: str=""):
	if dirname != "":
		assert p.exists(dirname), "dirname must be a valid existing directory name."
		n = dirname+"/"+name
	else:	
		n = name

	pickle.dump(obj, open(n, "wb"))


"""
	Loads object from binary file.

	:param name: filename
	:type name: string
	:return: unpickled object
	:rtype: pre-pickle object type (universal)
"""
def pickle_out(name: str, dirname: str=""):
	if dirname != "":
		assert p.exists(dirname), "dirname must be a valid existing directory name."
		n = dirname+"/"+name
	else:	
		n = name
	assert p.isfile(n), "File to read should exist."

	return pickle.load(open(n, "rb"))


# testing
if __name__ == '__main__':
	import os
	import sympy as s
	import shutil

	name = "testname.p"
	text = "this is a test name"

	# test 001a
	if p.isfile(name):
		os.remove(name)
	pickle_in(text, name)
	assert p.isfile(name), "Test 001a failure: File does not exist"
	# end of test 001a

	# test 002a
	assert pickle_out(name) == text, "Test 002a failure: File content corrupted"
	os.remove(name)
	# end of test 002a

	# test 001b
	directory = "pickletest"
	if not p.exists(directory):
		os.mkdir(directory)
	if p.isfile(directory+"/"+name):
		os.remove(directory+"/"+name)
	pickle_in(text, name, directory)
	assert p.isfile(directory+"/"+name), "Test 001b failure: File does not exist"
	# end of test 001b

	# test 002b
	assert pickle_out(name, directory) == text, "Test 002b failure: File content corrupted"
	shutil.rmtree(directory)
	# end of test 002b

	# test 003
	name_003 = "sympy_matrix003.p"
	matrix_003 = s.ones(4)

	if p.isfile(name_003):
		os.remove(name_003)
	pickle_in(matrix_003, name_003)
	assert pickle_out(name_003) == matrix_003, "Test 003 failure: sympy matrix not equal"
	os.remove(name_003)
	# end of test 003

	# test 004
	name_004 = "sympy_matrix004.p"
	matrix_004_1 = s.ones(4)
	matrix_004_2 = s.ones(4)
	matrix_004 = matrix_004_1 * matrix_004_2

	if p.isfile(name_004):
		os.remove(name_004)
	pickle_in(matrix_004, name_004)
	assert pickle_out(name_004) == matrix_004, "Test 004 failure: sympy matrix not equal"
	os.remove(name_004)
	# end of test 004

	# test 005
	name_005 = "sympy_symbols005.p"
	symbol_005 = s.Symbol('s')

	if p.isfile(name_005):
		os.remove(name_005)
	pickle_in(symbol_005, name_005)
	assert pickle_out(name_005) == symbol_005, "Test 005 failure: sympy symbol not equal"
	os.remove(name_005)
	# end of test 005

	# test 006
	name_006 = "sympy_symbols006.p"
	s_006 = s.Symbol('s')
	matrix_006 = s.Matrix([[s_006,0,1],[0,2,s_006]])

	if p.isfile(name_006):
		os.remove(name_006)
	pickle_in(matrix_006, name_006)
	assert pickle_out(name_006) == matrix_006, "Test 006 failure: sympy matrix with symbols not equal"
	os.remove(name_006)
	# end of test 005
	
	print("pickle_tools.py: All tests successful!")
