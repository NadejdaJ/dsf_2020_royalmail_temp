import os
import sys
import pandas as pd
import params


class depot_class(object):

	def __init__(self):
		self.depot_name = params.depot_name
		self.sample_name = params.sample_name
		self.postcode = None
		self.latitude = None
		self.longitude = None
		self.num_stops = None
		self.num_parcels = None
		self.num_vans = params.max_vans
		self.max_duty = params.max_duty
		self.service_time = params.service_time

		self.build()

	def build(self):
		sample_path = "../data/input/" + self.depot_name + "/" + self.sample_name
		suffix = "parcels.csv"

		if not os.path.exists(sample_path):
			sys.exit("\nCAUTION: input path not found...\n\n%s\n" % sample_path)
		for fname in os.listdir(sample_path):
			if fname.endswith(suffix):
				filename = os.path.join(sample_path, fname)
				data_df = pd.read_csv(filename, sep=",", index_col=0)
				break
		else:
			sys.exit("\nCAUTION: postcode input file not found...\n")

		self.postcode = data_df.loc[0].postcode#.values[0]
		self.latitude = data_df.loc[0].latitude#.values[0]
		self.longitude = data_df.loc[0].longitude#.values[0]

		print("\n\t Depot Name:       %s\t" % self.depot_name)
		print("\t Depot Postcode:   %s\t" % self.postcode)
		print("\t Depot Latitude:   %s\t" % self.latitude)
		print("\t Depot Longitude:  %s\t" % self.longitude)
		print("\t Depot Fleet Size: %s\t" % self.num_vans)
		print("\t Depot Max Duty:   %s [min]\t\n" % self.max_duty)

