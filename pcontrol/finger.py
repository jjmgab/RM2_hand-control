from pcontrol import pickle_tools as pt
import os
import os.path as p

class Finger:

	directory = ''

	def __init__(self, number: int, njoints: int, fdir: str = directory):
		assert p.exists(fdir), "An existing directory must be provided."

		self.directory = fdir
		self.fNumber = number

		assert 'V{0}'.format(self.fNumber) in [x for x in os.listdir(self.directory) if x[0] == 'V'], "There is no data for base of finger number {0}.".format(self.fNumber)

		self.V = pt.pickle_out('V{0}'.format(self.fNumber), self.directory)
		print("Finger {0}: base coordinates ready".format(self.fNumber))

		# transformation matrices
		self.K = []

		for i in range(0,njoints):
			assert 'K{0}{1}'.format(self.fNumber, i) in [x for x in os.listdir(self.directory) if x[0:2] == 'K{0}'.format(self.fNumber)], "There is no data for transformation matrix number {0} of finger {1}.".format(i, self.fNumber)			
			self.K.append(pt.pickle_out('K{0}{1}'.format(self.fNumber, i), self.directory))
			print("Finger {2}: transformation {0}->{1} ready.".format(i, i+1, self.fNumber))

		print("Finger {0} ready.".format(self.fNumber))