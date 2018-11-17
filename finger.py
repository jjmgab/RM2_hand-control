import os
import pickle_tools as pt

class Finger:

	directory = ''

	def __init__(self, number: int, fdir: str = directory):
		self.directory = fdir
		self.fNumber = number

		assert 'V{0}'.format(self.fNumber) in [x for x in os.listdir(self.directory) if x[0] == 'V'], "There is no data for base of finger number {0}.".format(self.fNumber)

		self.V = pt.pickle_out('V{0}'.format(self.fNumber), self.directory)
		print(self.V)