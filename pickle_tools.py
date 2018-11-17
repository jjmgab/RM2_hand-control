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
def pickle_in(obj, name: str):
	pickle.dump(obj, open(name, "wb"))

def pickle_out(name: str):
	assert p.isfile(name), "File to read should exist."
	return pickle.load(open(name, "rb"))

# testing
if __name__ == '__main__':
	import os
	import sympy as s

	name = "testname.p"
	text = "this is a test name"

	# test 001
	if p.isfile(name):
		os.remove(name)
	pickle_in(text, name)
	assert p.isfile(name), "Test 001 failure: File does not exist"
	# end of test 001

	# test 002
	assert pickle_out(name) == text, "Test 002 failure: File content corrupted"
	os.remove(name)
	# end of test 002

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

	
	print("pickle_tools.py: All tests successful!")
