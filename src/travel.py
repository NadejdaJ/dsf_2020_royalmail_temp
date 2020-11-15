import os
import sys
import pandas as pd

import params

class matrix_class(object):

	def __init__(self, locations):
		self.time = pd.DataFrame(index=locations, columns=locations)
		self.dist = pd.DataFrame(index=locations, columns=locations)

		self.read_matrix_from_file()

	def read_matrix_from_file(self):

		sample_path = "../data/input/" + params.depot_name + "/" + params.sample_name
		dist_suffix = 'matrix_distance.csv'
		time_suffix = 'matrix_time.csv'

		if not os.path.exists(sample_path):
			sys.exit("\nCAUTION: Travel Matrices not found ... \n")

		# Loading Time Matrix from file
		for fname in os.listdir(sample_path):
			if fname.endswith(time_suffix):
				file_name = os.path.join(sample_path, fname)
				self.time = pd.read_csv(file_name, sep=",", index_col=0)
				break
		else:
			sys.exit("\nCAUTION: Time Matrix input file not found...\n %s" % sample_path)

		# Loading Distance Matrix from file
		for fname in os.listdir(sample_path):
			if fname.endswith(dist_suffix):
				file_name = os.path.join(sample_path, fname)
				self.dist = pd.read_csv(file_name, sep=",", index_col=0)
				break
		else:
			sys.exit("\nCAUTION: Distance Matrix input file not found...\n %s" % sample_path)
