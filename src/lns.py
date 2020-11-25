from random import sample, shuffle
from math import floor
import numpy as np

class lns_class(object):

	def __init__(self, routes, depot_id, lns_destroy_frac):
		self.depot_id = depot_id
		self.stop_list = routes.stop_list
		self.lns_destroy_frac = lns_destroy_frac
		self.num_stops = routes.num_stops
		self.lns_destroy_nb = int(floor(lns_destroy_frac*self.num_stops))


	def rnd_destroy(self):
		stop_list_no_hub = [item for item in self.stop_list if item not in self.depot_id]
		idx_removed = sample(range(0, self.num_stops), self.lns_destroy_nb)

		stop_removed = [stop_list_no_hub[i] for i in idx_removed]
		stop_list_destroy = [item for item in self.stop_list if item not in self.stop_removed]

		return stop_removed, stop_list_destroy

	def compute_insert_array(self, stop_list_destroy, insert_stop):
		outward_array = self.matrix_cost.loc[insert_stop, stop_list_destroy[1:]+self.depot_id].values  # from insert_dp to part
		inward_array = self.matrix_cost.loc[stop_list_destroy, insert_stop].T.values  # from part to insert_dp
		current_array = np.diag(self.matrix_cost.loc[stop_list_destroy, stop_list_destroy[1:]+self.depot_id])
		insert_array = inward_array + outward_array - current_array
		return insert_array

	def perform_repair_random(self, stop_removed, stop_list_destroy):
		shuffle(stop_removed)
		while stop_removed.any():  # until every dp have been added
			insert_stop = stop_removed.pop(0)  # insert first dp
			insert_array = self.compute_insert_array(stop_list_destroy, insert_stop) # calculate cost of insertion into each possible position
			insertion_idx = np.argmin(insert_array) + 1  # index of minimum
			stop_list_destroy = np.insert(stop_list_destroy, insertion_idx, insert_stop)  # insert dp
		return stop_list_destroy

	def perform_lns(self):
		stop_removed, stop_list_destroy = self.rnd_destroy()
		stop_list_repaired = self.perform_repair_random(stop_removed, stop_list_destroy)














