from random import sample, shuffle, seed
from math import floor
import numpy as np
from utils import build_quick_routes


class lns_class(object):
	"""
	This class implements the Large Neighbourhood Search algorithm by Pisinger, D., & Ropke, S. (2010)
	"""

	def __init__(self, puzzle, routes, lns_destroy_frac, seed_value):
		self.stop_list = routes.stop_list  # current route
		self.num_stops = routes.num_stops  # number of stops in the current route
		self.lns_destroy_nb = int(floor(lns_destroy_frac * self.num_stops))  # number of stops to remove in the destroy step
		self.puzzle = puzzle  # puzzle object
		self.depot_id = puzzle.depot_id  # identifier of the depot

		seed(seed_value)

	def rnd_destroy(self):
		"""
		This function performs the random destroy operator: it removes "lns_destroy_nb" stops from the current route.
		"""
		stop_list_no_depot = [stop for stop in self.stop_list if stop not in self.depot_id]
		idx_removed = sample(range(0, self.num_stops), self.lns_destroy_nb)
		self.stop_removed = [stop_list_no_depot[i] for i in idx_removed]
		self.partial_stop_list = [stop for stop in self.stop_list if stop not in self.stop_removed]

	def compute_insert_array(self):
		"""
		This function calculates the cost of inserting the selected stop at every possible position in the partial stop list
		"""
		outward_array = self.puzzle.time_mtx.loc[
			self.insert_stop, self.partial_stop_list[1:] + [self.depot_id] ].values  # from insert_dp to part
		inward_array = self.puzzle.time_mtx.loc[
			self.partial_stop_list, self.insert_stop].T.values  # from part to insert_dp
		current_array = np.diag(
			self.puzzle.time_mtx.loc[self.partial_stop_list, self.partial_stop_list[1:] + [self.depot_id] ])
		self.insert_array = inward_array + outward_array - current_array

	def rnd_repair(self):
		"""
		This function performs the random repair operator: it inserts a random removed stop at its cheapest position in the partial route
		"""
		shuffle(self.stop_removed)
		while self.stop_removed:  # until every dp have been added
			self.insert_stop = self.stop_removed.pop(0)  # insert first dp
			self.compute_insert_array()  # calculate cost of insertion into each possible position
			insertion_idx = np.argmin(self.insert_array) + 1  # index of minimum
			self.partial_stop_list = list(np.insert(self.partial_stop_list, insertion_idx, self.insert_stop))  # insert dp
		self.new_stop_list_repair = self.partial_stop_list

	def run(self):
		"""
		This function run the LNS algorithm and create a new route object.
		"""
		self.rnd_destroy()
		self.rnd_repair()
		new_route = build_quick_routes(self.puzzle, self.new_stop_list_repair)
		return new_route
