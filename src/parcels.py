import os
import sys
import pandas as pd
import params

class parcel_class(object):

	def __init__(self):
		self.data = None
		self.num_parcels = None
		self.num_stops = None
		self.parcel_per_stop = dict()

		self.load_data()
		self.load_parcel_per_stop()

	def load_data(self):
		sample_path = "../data/input/" + params.depot_name + "/" + params.sample_name
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

		self.data = data_df.loc[data_df.id != 'depot']
		self.data.postcode = self.data.postcode.str.replace(" ","")
		self.stop_list = list(self.data.postcode.unique())
		self.num_parcels = len(list(self.data.postcode))
		self.num_stops = len(list(self.data.postcode.unique()))

	def load_parcel_per_stop(self):
		counts = dict()
		parcel_list = list(self.data.postcode)
		for i in parcel_list:
			counts[i] = counts.get(i, 0) + 1
		self.parcel_per_stop = counts

		print("\nNumber of Parcels:", self.num_stops)
		print("Number of Stops:  ", self.num_parcels)
		print("\nList of Delivery Points:\n")
		print(self.data)
