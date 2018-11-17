import marshal
import os.path as p

"""
	Binary dumps created using marshal module are
	independent on the architecture.
"""

"""
	Saves object to binary file.

	:param obj: object to dump
	:param name: filename
	:type obj: any
	:type name: string
"""
def marshal_in(obj, name: str):
	marshal.dump(obj, open(name, "wb"))

def marshal_out(name: str):
	assert p.isfile(name), "File to read should exist."
	return marshal.load(open(name, "rb"))

# testing
if __name__ == '__main__':
	import os

	name = "testname.p"
	text = "this is a test name"

	# test 001
	if p.isfile(name):
		os.remove(name)
	marshal_in(text, name)
	assert p.isfile(name), "Test 001 failure: File does not exist"

	# test 002
	assert marshal_out(name) == text, "Test 002 failure: File content corrupted"

	os.remove(name)
	print("marshal_tools.py: All tests successful!")
